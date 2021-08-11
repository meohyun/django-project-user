from django import forms
from .models import User

class UserForm(forms.ModelForm):
  class Meta:
    model = User
    fields = ['nickname']
    
    def signup(self,request,user):
      user.nickname = self.cleaned_data["nickname"]
      user.kakao_id = self.cleaned_data["kakao_id"]
      user.save()
