
from datetime import datetime, time
from django.utils.timezone import localtime
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.http import Http404

User = get_user_model()

class RedirectIfNotFoundMiddleware:
    """Redirect authenticated users to the previous URL if a page doesn't exist."""
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
        except Http404:
            if request.user.is_authenticated:
                # If the page doesn't exist and the user is authenticated, redirect to the same page
                return redirect(request.META.get('HTTP_REFERER', reverse('restricted_access')))  # Default to home if no referrer
            else:
                # For unauthenticated users, redirect to the login page
                return redirect('login')  # Replace 'login' with your actual login URL name
        return response

class RequireAuthenticationMiddleware:
    """Middleware to require user authentication for all pages."""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated and request.path not in [reverse('login'), '/omar']:
            # Add any paths you want to exclude here (e.g., admin login, static files, etc.)
            return redirect('login')  # Replace 'login' with the name of your login URL

        response = self.get_response(request)
        return response

class IdleTimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            last_activity = request.session.get('last_activity')
            now = datetime.now().timestamp()

            # If last activity is older than 30 minutes
            if last_activity and now - last_activity > 1800:
                logout(request)
                return redirect('login')

            # Update last activity timestamp
            request.session['last_activity'] = now

        return self.get_response(request)

# class RestrictAccessMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         # Ensure user is authenticated before accessing request.user
#         if request.user.is_authenticated and hasattr(request.user, 'saleagent'):
#             agent = request.user.saleagent
#             now = localtime()
#             day = now.strftime('%A')  # Current day (e.g., Monday)
#             current_time = now.time()  # Current time

#             # Check if the current day and time are within allowed limits for the agent
#             if day not in agent.allowed_days or not (agent.start_time <= current_time <= agent.end_time):
#                 return redirect('restricted_access')  # Redirect to an access-denied page
        
#         # If not authenticated, allow access or do additional checks
#         return self.get_response(request)

# class RestrictAccessMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         # Check if user is authenticated before using request.user
#         if request.user.is_authenticated:
#             print(f"Authenticated User: {request.user.username}")
#             if hasattr(request.user, 'saleagent'):
#                 agent = request.user.saleagent
#                 now = localtime()
#                 day = now.strftime('%A')  # Current day (e.g., Monday)
#                 current_time = now.time()  # Current time

#                 if day not in agent.allowed_days or not (agent.start_time <= current_time <= agent.end_time):
#                     return redirect('restricted_access')  # Redirect to an access-denied page
#         else:
#             print("Unauthenticated request detected.")
        
#         return self.get_response(request)
class RestrictAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        if user.is_authenticated and hasattr(user, 'saleagent'):
            agent = user.saleagent
            now = localtime()
            day = now.strftime('%A')  # Current day (e.g., Monday)
            time = now.time()  # Current time

            if day not in agent.allowed_days or not (agent.start_time <= time <= agent.end_time):
                return redirect('restricted_access')  # Redirect to an access-denied page

        return self.get_response(request)