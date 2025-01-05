from django.shortcuts import render
from django.contrib.auth import get_user_model
from axes.models import AccessAttempt
from django.utils.translation import gettext_lazy as _

from .models import Notification


def send_suspension_notification(user):
    """Send a notification to the manager when a user's account is suspended."""
    try:
        # Get the first manager (you may want to handle this logic differently if you have more managers)
        manager = get_user_model().objects.filter(groups__name="Manager").first()
        if manager:
            # Create the notification
            message = f"User {user.username} has been suspended due to multiple failed login attempts."
            notification = Notification.objects.create(
                message=message,
                user=manager
            )
            print(f"Notification created: {notification.message}")
        else:
            print("No manager found.")
    except Exception as e:
        print(f"Error sending notification: {e}")



def custom_lockout_response(request, context):
    """
    Custom response for lockout to update user status and show lockout message.
    """
    # Get the locked-out username from context
    username = context.get('username', 'Unknown user')

    try:
        # Retrieve the user instance
        user = get_user_model().objects.get(username=username)
        
        # Mark the user account as inactive
        user.is_active = False
        user.save()

        # Send suspension notification to the manager
        send_suspension_notification(user)

        # Optionally, you can log the lockout event or handle additional logic here
    except get_user_model().DoesNotExist:
        user = None  # Handle case where user doesn't exist

    return render(
        request,
        'axes/lockout.html',
        {
            'support_email': 'support@example.com',
            'locked_user': user.username if user else 'Unknown user',
            'message': _('Your account has been locked due to multiple failed login attempts. Please contact support for assistance.')
        }
    )
