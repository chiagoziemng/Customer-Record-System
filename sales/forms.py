from django import forms
from .models import CustomUser

# Form for creating a new user
class CustomUserCreationForm(forms.ModelForm):
    class Meta:
        models = CustomUser
        fields = ['username', 'email', 'role', 'phone', 'password']

# Form for updating an existing user
class CustomUserChangeForm(forms.ModelsForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'role', 'phone']