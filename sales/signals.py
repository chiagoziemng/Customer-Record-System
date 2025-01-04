from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from .models import ClientRecord
from .models import Notification

User = get_user_model()  # Get the custom user model

# Signal to send notification when a client record is approved
@receiver(post_save, sender=ClientRecord)
def send_approval_notification(sender, instance, created, **kwargs):
    # Only trigger on update, not creation
    if not created and instance.approval_status == 'approved':
        # Send email notifaication to the manager
        #send_approval_email(instance)

        # Optionally, create an in-app notification for the manager
        create_inapp_notification(instance)

def send_approval_email(client_record):
    # Example: Send a email to the first manager
    manager = User.objects.filter(groups__name='Manager').first() # Assuming 'Manager' group exists
    if manager:
        send_mail(
            'Client Record Approved',
            f'The client record for {client_record.business_name} has been approved.'
            'from@example.com', # Sender email address
            [manager.email], # Recipient email address
            fail_silently=False,
        )

def  create_inapp_notification(client_record):
    # Optionally create an in-app notification
    manager = User.objects.filter(groups__name='Manager').first()
    if manager:
        Notification.objects.create(
            user=manager,
            message=f'The client record for {client_record.business_name} has been approved.'
        )