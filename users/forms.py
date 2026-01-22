from django import forms
from django.contrib.auth.models import User

# custom signup form based on django users model
class SignupForm(forms.ModelForm):
    password1=forms.CharField(widget=forms.PasswordInput)
    confirm_Password=forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model=User #build in django user model
        fields=['username','email','first_name','last_name']
        
    def clean(self)