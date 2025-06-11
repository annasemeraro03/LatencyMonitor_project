from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from datetime import date

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'birth_date', 'profile_image']

class UserUpdateForm(forms.ModelForm):
    birth_date = forms.DateField(widget=forms.SelectDateWidget(years=range(1900, date.today().year + 1)))
    class Meta:
        model = CustomUser
        fields = ['email', 'birth_date', 'profile_image']
