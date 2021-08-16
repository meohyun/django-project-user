from django.shortcuts import render
from django.views.generic import ListView,CreateView,DetailView
from django.urls import reverse
from trade.models import Post
from trade.forms import PostForm
from allauth.account.views import PasswordChangeView

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
    

class CreateZokboView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'trade/form.html'

    def get_success_url(self):
        return reverse('detail',kwargs={'pk':self.object.id})
        
    