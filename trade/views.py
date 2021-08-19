from django.shortcuts import render
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
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
        return reverse('index')

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
    
class UpdateZokboView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'trade/form.html'
    
    def get_success_url(self):
        return reverse('detail',kwargs={'pk':self.object.id}

class DeleteZokboView(DeleteView):
    model = Post
    template_name = 'trade/detail_confirm_delete.html'

    def get_success_url(self):
        return reverse('index')

 def download(request,path):
    file_path = os.path.join(settings.MEDIA_ROOT,path)
    if os.path.exists(file_path):
        with open(file_path,'rb',encoding='cp949') as fh:
            response = HttpResponse(fh.read(),content_type="application/upload_files")
            response['Content-Disposition']= 'inline;filename='+ os.path.basename(file_path)
            return response
    raise Http404   
          
    
        
    
