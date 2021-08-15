from django import forms
from .models import User

class UserForm(forms.ModelForm):
  class Meta:
    model = User
    fields = ['nickname','student_number']
    
    def signup(self,request,user):
      user.nickname = self.cleaned_data["nickname"]
      user.student_number = self.cleaned_data["student_number"]
      user.save()
