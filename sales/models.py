from django.db import models
from django.contrib.auth.models import AbstractUser

# Custom user model for the system's super administrator
class SuperAdmin(AbstractUser):
    # Custom fields can be added here if needed
     # Inherit all fields from Django's default user model
    pass

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
    
# Model representing a client's business record
class ClientRecord(models.Model):
    # Choices for the status indicator
    STATUS_CHOICES = [
        ('new', 'New'),
        ('updated', 'Updated'),
        ('red-flagged', 'Red-flagged'),
    ]

    sale_agent = models.ForeignKey(SaleAgent, on_delete=models.CASCADE)
    business_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    owner_name = models.CharField(max_length=100)
    contact_info = models.CharField(max_length=100)
    whatsapp_validity = models.BooleanField(default=False)
    social_media_accounts = models.TextField()
    discussion_review = models.TextField()
    deal_status = models.TextField()
    status_indicator = models.CharField(max_length=15, choices=STATUS_CHOICES, default='new')

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
    