from django import forms
from .models import CustomUser, ClientRecord, SaleAgent, SaleAgentProfile

class SaleAgentProfileForm(forms.ModelForm):
    class Meta:
        model = SaleAgentProfile
        fields = ['sale_agent', 'name', 'title', 'location', 'agent_id', 'start_date', 
                  'bank_name', 'account_number', 'account_type', 'monthly_payment', 
                  'last_payment_date', 'payment_duration_months']
    
    # Add custom initialization to dynamically load available SaleAgent records
    def __init__(self, *args, **kwargs):
        super(SaleAgentProfileForm, self).__init__(*args, **kwargs)
        # Ensure that the sale_agent field is populated with all SaleAgent records
        self.fields['sale_agent'].queryset = SaleAgent.objects.all()
        
class SaleAgentForm(forms.ModelForm):
    class Meta:
        model = SaleAgent
        fields = ['allowed_days', 'start_time', 'end_time']
        widgets = {
            'allowed_days': forms.CheckboxSelectMultiple(choices=[
                ('Monday', 'Monday'),
                ('Tuesday', 'Tuesday'),
                ('Wednesday', 'Wednesday'),
                ('Thursday', 'Thursday'),
                ('Friday', 'Friday'),
                ('Saturday', 'Saturday'),
                ('Sunday', 'Sunday'),
            ]),
        }
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
            'deal_status', 'status_indicator', 'category'
        ]