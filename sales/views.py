from django.http import JsonResponse
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import logout
from django.urls import reverse_lazy
from django.shortcuts import render
from django.views.generic import ListView
from .models import ClientRecord
from django.contrib.auth.mixins import LoginRequiredMixin



@login_required
def client_record_detail(request, pk):
    client_record = get_object_or_404(ClientRecord, pk=pk, sale_agent=request.user)
    return JsonResponse({
        "name": client_record.name,
        "email": client_record.email,
        "phone_number": client_record.phone_number,
        "address": client_record.address,
        "created_at": client_record.created_at.strftime("%Y-%m-%d %H:%M:%S")
    })




class ClientRecordListView(LoginRequiredMixin, ListView):
    model = ClientRecord
    template_name = "sales/client_record_list.html"
    context_object_name = "client_records"

    def get_queryset(self):
        return ClientRecord.objects.filter(sale_agent=self.request.user)

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
