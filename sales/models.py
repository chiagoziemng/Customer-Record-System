from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model

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

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})" # String representation for queries

# Model for logging user actions in the system
class SessionLog(models.Model):
    user = models.CharField(max_length=255) # Username or identifier of the user
    action = models.TextField() # Description of the performed action
    timestamp = models.DateTimeField(auto_now_add=True) # Timestamp of the action

    def __str__(self):
        return f"{self.user} - {self.timestamp}" # String representation for logs

# Model representing a sales agent in the system
class SaleAgent(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)
    location = models.CharField(max_length=255)
    bank_details = models.TextField()
    start_date = models.DateField()

    def __str__(self):
        return self.name  # String representation for the admin panel and queries
    

User = get_user_model()    
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


    # String representation for the admin panel and queries
    def __str__(self):
        return self.business_name

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
