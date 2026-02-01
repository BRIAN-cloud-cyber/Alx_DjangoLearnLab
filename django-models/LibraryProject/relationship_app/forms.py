# forms.py
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# You can extend the UserCreationForm if you want to add more fields
# class CustomUserCreationForm(UserCreationForm):

class UserCreationForm(UserCreationForm):
    class Meta:
        model=User
        fields = ('username','email', 'password1', 'password2')