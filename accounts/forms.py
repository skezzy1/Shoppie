from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['name', 'surname', 'user'] 

    def save(self, commit=True):
        user_profile = super().save(commit=False)
        user_profile.user = self.instance.user 
        if commit:
            user_profile.save()
        return user_profile

class UserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'avatar']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Enter your username'}),
        }
