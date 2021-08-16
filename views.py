from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request,'trade/index.html')

class DetailZokboView(DetailView):
    model = Post
    template_name = 'trade/detail.html'
    

class CreateZokboView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'trade/form.html'

    def get_success_url(self):
        return reverse('detail',kwargs={'pk':self.object.id})
