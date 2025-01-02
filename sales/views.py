from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.urls import reverse_lazy
from django.shortcuts import render

# Custom login view
class CustomLoginView(LoginView):
    template_name = 'sales/login.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        # Check if the user role is authorized
        user = form.get_user()
        if user.role in ['sale_agent', 'manager', 'super_admin']:
            return super().form_valid(form)
        else:
            # Logout unauthorized users and show an error
            logout(self.request)
            form.add_error(None, "You are not authorized to log in.")
            return self.form_invalid(form)
