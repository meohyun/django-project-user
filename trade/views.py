from django.shortcuts import render,get_object_or_404
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
    TemplateView,
)
from django.urls import reverse
from trade.models import Post
from trade.forms import PostForm
from allauth.account.views import PasswordChangeView
from allauth.account.models import EmailAddress
from braces.views import LoginRequiredMixin,UserPassesTestMixin
from .functinos import confirmation_required_redirect

# Create your views here.

def index(request):
    return render(request,'trade/index.html')


class CustomPasswordChangeView(PasswordChangeView):
    def get_success_url(self):
        return reverse('profile',kwargs={'user_id':self.request.user.id})

class IndexView(ListView):
    model = Post 
    template_name = 'trade/index.html'
    paginate_by = 8
    ordering = ['-dt_created']
    context_object_name = 'posts'

class DetailZokboView(DetailView):
    model = Post
    template_name = 'trade/detail.html'
    

class CreateZokboView(LoginRequiredMixin,CreateView):
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
        return reverse('detail',kwargs={'pk':self.object.id}
                       
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
    pk_url_kwargs = 'user_id'
    context_object_name = 'profile_user'            
                                    
    def get_context_data(self,**kwargs):
        context = super().get_context(**kwargs)
        user_id = self.kwargs.get(user_id)
        context['user_posts'] = Post.objects.filter(author_id=user_id).order_by('-dt_created')[:4]
        return context
 
class UserReivewListView(ListView):
    model = Post
    template_name = 'trade/user_review_list.html'
    context_object_name = 'user_posts'       
    paginate_by = 4
    
    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        return Post.objects.filter(author_id=user_id).order_by('-dt_created')         
    
    def get_context_data(self,**kwargs):
        context = super().get_context(**kwargs)
        context['profile_user'] = get_object_or_404(User,id= self.kwargs.get('user_id'))
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
                       
                       
 def download(request,path):
    file_path = os.path.join(settings.MEDIA_ROOT,path)
    if os.path.exists(file_path):
        with open(file_path,'rb',encoding='cp949') as fh:
            response = HttpResponse(fh.read(),content_type="application/upload_files")
            response['Content-Disposition']= 'inline;filename='+ os.path.basename(file_path)
            return response
    raise Http404   
          
    
        
    
