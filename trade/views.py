from django.http.response import Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
    TemplateView,
)
from django.urls import reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from trade.models import Post,User,Comment
from trade.forms import PostForm,ProfileForm,CommentForm
from allauth.account.views import PasswordChangeView
from allauth.account.models import EmailAddress
from braces.views import LoginRequiredMixin,UserPassesTestMixin
from .functions import confirmation_required_redirect

import os

# Create your views here.

def index(request):
    return render(request,'trade/index.html')

class IndexView(ListView):
    model = Post 
    template_name = 'trade/index.html'
    

class ListZokboView(ListView):
    model = Post
    context_object_name = 'posts'
    paginate_by = 4
    ordering = ['-dt_created']
    

class DetailZokboView(DetailView):
    model = Post
    template_name = 'trade/detail.html'

    
class CreateZokboView(LoginRequiredMixin,UserPassesTestMixin,CreateView):
    model = Post
    form_class = PostForm
    template_name = 'trade/form.html'

    redirect_unauthenticated_users = True
    raise_exception = confirmation_required_redirect

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('detail',kwargs={'pk':self.object.id})

    def test_func(self,user):
        return EmailAddress.objects.filter(user=user,verified=True).exists()
    
    def upload_file(request):
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                # file is saved
                form.save()
                return HttpResponseRedirect('detail')
        else:
            form = PostForm()
        return render(request, 'detail.html', {'form': form})
        
class UpdateZokboView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'trade/form.html'

    raise_exception = True

    def get_success_url(self):
        return reverse('detail',kwargs={'pk':self.object.id})
    
    def test_func(self,user):
        review = self.get_object()
        return review.author == user

class DeleteZokboView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Post
    template_name = 'trade/detail_confirm_delete.html'

    raise_exception = True

    def get_success_url(self):
        return reverse('index')

    def test_func(self,user):
        review = self.get_object()
        return review.author == user

class ProfileView(DetailView):
    model = User
    template_name = 'trade/profile.html'
    pk_url_kwarg = 'user_id'
    context_object_name = 'profile_user'

    # overriding
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.kwargs.get('user_id')
        context['user_posts'] = Post.objects.filter(author_id=user_id).order_by('-dt_created')[:4]
        return context

class UserReviewListView(ListView):
    model = Post
    template_name = 'trade/user_review_list.html'
    context_object_name = 'user_posts'
    paginate_by = 4

    # overriding
    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        return Post.objects.filter(author_id=user_id).order_by('-dt_created')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile_user']= get_object_or_404(User,id=self.kwargs.get('user_id'))
        return context

class ProfileSetView(LoginRequiredMixin,UpdateView):
    model = User
    form_class = ProfileForm
    template_name = 'trade/profile_set_form.html'

    def get_object(self,queryset=None):
        return self.request.user
    
    def get_success_url(self):
        return reverse('index')

class ProfileUpdateView(LoginRequiredMixin,UpdateView):
    model = User
    form_class = ProfileForm
    template_name = 'trade/profile_update_form.html'

    def get_object(self,queryset=None):
        return self.request.user
    
    def get_success_url(self):
        return reverse('profile',kwargs=({'user_id':self.request.user.id}))

class CustomPasswordChangeView(LoginRequiredMixin,PasswordChangeView):
    def get_success_url(self):
        return reverse('profile',kwargs={'user_id':self.request.user.id})



# comment 
def comment_new(request,post_pk):
    post = get_object_or_404(Post,pk=post_pk)

    if request.method == 'POST':
        form = CommentForm(request.POST,request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('detail', post.pk)
    else:
        form = CommentForm()
    return render(request,'trade/comment.html',{'form':form})

def comment_update(request,post_pk,pk):
    comment = get_object_or_404(Comment,pk=pk)
    post = get_object_or_404(Post,pk=post_pk)

    if request.method == 'POST':
        form = CommentForm(request.POST,request.FILES,instance=comment)
        if form.is_valid():
            comment = form.save()
            return redirect('detail', post.pk)
    else:
        form = CommentForm(instance=comment)
    return render(request,'trade/comment.html',{'form':form})

def comment_delete(request,post_pk,pk):
    comment = get_object_or_404(Comment,pk=pk)

    if request.method == 'POST':
        comment.delete()
        return redirect('detail',comment.post.pk)
       
    return render(request,'trade/comment_confirm_delete.html',{'comment':comment})


def download(request,path):
    file_path = os.path.join(settings.MEDIA_ROOT,path)
    if os.path.exists(file_path):
        with open(file_path,'rb') as fh:
            response = HttpResponse(fh.read(),content_type="application/upload_files")
            response['Content-Disposition']= 'inline;filename='+ os.path.basename(file_path)
            return response
    raise Http404


def search(request):
    posts = Post.objects.all().order_by('-id')

    q = request.POST.get('q', "") 

    if q:
        posts = posts.filter(class_name__icontains=q)
        return render(request, 'trade/search.html', {'posts' : posts, 'q' : q})
    
    else:
        return render(request, 'trade/search.html')

def signout(request):
    if request.method == 'POST':
        request.user.delete()
        return redirect('index')

    else:
        return render(request, 'account/signout.html')
   
def post_like(request,post_id):
    post = get_object_or_404(Post,id=post_id)
    current_user = request.user
    like_user = User.objects.get(pk=current_user.pk)

    check_like = like_user.like_posts.filter(id=post_id)

    if check_like.exists():
        like_user.like_posts.remove(post)
        post.like_count -= 1
        post.save()
    else:
        like_user.like_posts.add(post)
        post.like_count += 1
        post.save()

    return redirect('detail',post_id)


