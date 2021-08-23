from django import forms
from .models import User,Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["class_name","professor_name","grade","upload_files",'content']
        widgets = {
            'grade' : forms.RadioSelect
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'nickname',
            'profile_pic',
            'intro'
        ]
        widgets = {
            'intro':forms.Textarea
        }
        
        
