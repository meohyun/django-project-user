from django import forms
from .models import User,Post


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["nickname",'student_number']

        def signup(self,request,User):
            User.nickname = self.cleaned_data['nickname']
            User.student_number = self.cleaned_data['student_number']
            User.save()

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["class_name","professor_name","grade","file",'content']
        widgets = {
            'grade' : forms.RadioSelect
        }
