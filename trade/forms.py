from django import forms
from django.forms import widgets
from .models import User,Post,Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["class_name","professor_name","grade","upload_files",'content',"grade_num","semester"]
        widgets = {
            'grade' : forms.RadioSelect,

        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['nickname','profile_pic','intro','student_number']
        widgets = {
            'intro' : forms.Textarea
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
