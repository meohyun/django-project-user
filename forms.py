from django import forms
from .models import User,Post

class UserForm(forms.ModelForm):
  class Meta:
    model = User
    fields = ['nickname','student_number']
    
    def signup(self,request,user):
      user.nickname = self.cleaned_data["nickname"]
      user.student_number = self.cleaned_data["student_number"]
      user.save()
      
class PostForm(forms.ModelForm):
  class Meta:
    model = Post
    fields = ["class_name","professor_name","grade","file",'content']

    def create_post(self,request,post):
      post.class_name = self.class_name['class_name']
      post.professor_name = self.class_name['professor_name']
      post.grade = self.class_name['grade']
      post.file = self.class_name['file']
      post.content = self.class_name['content']
            
    
