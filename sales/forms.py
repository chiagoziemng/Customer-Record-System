from django import forms
from .models import CustomUser, ClientRecord

# Form for creating a new user
class CustomUserCreationForm(forms.ModelForm):
    class Meta:
        models = CustomUser
        fields = ['username', 'email', 'role', 'phone', 'password']

# Form for updating an existing user
class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'role', 'phone']

class ClientRecordForm(forms.ModelForm):
    class Meta:
        model = ClientRecord
        fields = [
            'business_name', 'location', 'owner_name', 'contact_info',
            'whatsapp_validity', 'social_media_accounts', 'discussion_review',
            'deal_status', 'status_indicator'
        ]