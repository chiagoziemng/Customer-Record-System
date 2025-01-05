from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.timezone import now
import json


# Custom user model with roles for SaleAgent, Manager, and SuperAdmin
class CustomUser(AbstractUser):
    # Choices for the user roles
    ROLE_CHOICES = [
        ('sale_agent', 'Sale Agent'),
        ('manager', 'Manager'),
        ('super_admin', 'Super Admin'),
    ]

    role = models.CharField(max_length=15, choices=ROLE_CHOICES) #Role of the user
    phone = models.CharField(max_length=15, blank=True, null=True) # Optional phone number
    failed_login_attempts = models.IntegerField(default=0)  # Track failed login attempts

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})" # String representation for queries




User = get_user_model()  
# Model representing a sales agent in the system
class SaleAgent(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)
    location = models.CharField(max_length=255)
    bank_details = models.TextField()
    start_date = models.DateField()
    allowed_days = models.JSONField(default=list)  # List of allowed days (e.g., ["Monday", "Tuesday"])
    start_time = models.TimeField(null=True, blank=True)  # Start of allowed access
    end_time = models.TimeField(null=True, blank=True)  # End of allowed access

    def __str__(self):
        return self.name  # String representation for the admin panel and queries
    
class SaleAgentProfile(models.Model):
    # Link to SaleAgent (user profile)
    sale_agent = models.ForeignKey(SaleAgent, on_delete=models.CASCADE, related_name="profile")
    
    # Sale agent personal details
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=50)
    location = models.CharField(max_length=255)
    agent_id = models.CharField(max_length=100, unique=True)
    start_date = models.DateField()

    # Bank details
    bank_name = models.CharField(max_length=255)
    account_number = models.CharField(max_length=100)
    account_type = models.CharField(max_length=50)  # E.g., Checking, Savings

    # Financial tracking
    monthly_payment = models.DecimalField(max_digits=10, decimal_places=2)
    last_payment_date = models.DateField()
    payment_duration_months = models.IntegerField()  # Track how many months they've been employed

    def __str__(self):
        return self.name

    def employment_duration(self):
        # Calculate how long they've been employed
        return (self.start_date - models.DateField.today()).days // 30  # Duration in months

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

# Model representing a client's business record
class ClientRecord(models.Model):
    # Choices for the status indicator
    STATUS_CHOICES = [
        ('new', 'New'),
        ('updated', 'Updated'),
        ('red-flagged', 'Red-flagged'),
    ]

    APPROVAL_CHOICES = [
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    sale_agent = models.ForeignKey(User, on_delete=models.CASCADE, related_name="client_records")
    business_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    owner_name = models.CharField(max_length=100)
    contact_info = models.CharField(max_length=100)
    whatsapp_validity = models.BooleanField(default=False)
    social_media_accounts = models.TextField()
    discussion_review = models.TextField()
    deal_status = models.TextField()
    status_indicator = models.CharField(max_length=15, choices=STATUS_CHOICES, default='new')
    approval_status = models.CharField(max_length=10, choices=APPROVAL_CHOICES, default='pending')

     # Link to Category
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="client_records")


    # String representation for the admin panel and queries
    def __str__(self):
        return self.business_name
    
    def save(self, *args, **kwargs):
        # If the record already exists, compare old and new values to log the changes
        if self.pk:
            original = ClientRecord.objects.get(pk=self.pk)
            changes = {}
            for field in self._meta.get_fields():
                if isinstance(field, models.Field):
                    old_value = getattr(original, field.name)
                    new_value = getattr(self, field.name)
                    if old_value != new_value:
                        changes[field.name] = {
                            'old': old_value,
                            'new': new_value
                        }
            
            # Log the changes in the SessionLog table
            if changes:
                SessionLog.objects.create(
                    user=self.sale_agent,  # Assuming the user is the sale agent
                    record=self,
                    action='update',
                    old_value=json.dumps(changes),  # Log the old values as JSON
                    new_value=json.dumps(changes),  # Log the new values as JSON
                )
        
        super().save(*args, **kwargs)  # Save the current record

# Model representing a manager in the system    
class Manager(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    department = models.CharField(max_length=100)

    def __str__(self):
        return self.name # String representation for the admin panel and queries
    

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username} - {self.message[:50]} at {self.created_at}"
    class Meta:
        ordering = ['-created_at']  # Show the most recent notifications first



# Model for logging user actions in the system
class SessionLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    record = models.ForeignKey(ClientRecord, on_delete=models.CASCADE, null=True)  # Make nullable
    action = models.CharField(max_length=50)
    old_value = models.JSONField(default=dict, blank=True)
    new_value = models.JSONField(default=dict, blank=True)
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.user} - {self.action} - {self.timestamp}"
