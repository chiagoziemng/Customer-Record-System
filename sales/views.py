from django.http import JsonResponse, HttpResponseForbidden
from django.contrib.auth.views import LoginView
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import logout
from django.urls import reverse_lazy
from django.shortcuts import render
from django.views.generic import ListView
from .models import ClientRecord
from django.contrib.auth.mixins import LoginRequiredMixin


@staff_member_required
def custom_admin_view(request):
    if request.user.is_superuser:
        return redirect('admin:index') # Redirect to the admin dashboard
    else:
        return HttpResponseForbidden("You are not authorized to view this page.")


# Dashboard for SaleAgent
@login_required
def sale_agent_dashboard(request):
    if not request.user.has_perm('sales.view_saleagent_dashboard'):
        return redirect('no_permission') # Handle permission denial
    return render(request, 'sales/sale_agent_dashboard.html')

# Dashboard for Manager
@login_required
def manager_dashboard(request):
    if not request.user.has_perm('sales.view_manager_dashboard'):
        return redirect('no_permission')
    return render(request, 'sales/sale_agent_dashboard.html')


# Dashboard for SuperAdmin
@login_required
def super_admin_dashboard(request):
    if not request.user.is_superuser:
        return redirect('no_permission')
    return render(request, 'sales/super_admin_dashboard.html')



def client_record_detail(request, id):
    record = get_object_or_404(ClientRecord, pk=id)
    return render(request, 'client_record_detail.html', {'record': record})


@login_required
def client_record_detail(request, pk):
    client_record = get_object_or_404(ClientRecord, pk=pk, sale_agent=request.user)
    return JsonResponse({
        "name": client_record.business_name,
        "phone_number": client_record.contact_info,
        "address": client_record.location,
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
