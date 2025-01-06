from django.http import JsonResponse, HttpResponseForbidden, HttpResponse
from django.contrib.auth.views import LoginView
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth import logout, get_user_model
from django.contrib.auth.models import Group
from django.urls import reverse_lazy
from django.views.generic import ListView
from .models import ClientRecord, Notification, SaleAgent, SessionLog
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import ClientRecordForm , SaleAgentForm, SaleAgentProfileForm

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from io import BytesIO
from openpyxl import Workbook





User = get_user_model()


def sale_agent_profile(request):
    if request.method == 'POST':
        form = SaleAgentProfileForm(request.POST)
        if form.is_valid():
            form.save()  # Save the sale agent profile
            return redirect('sale_agent_list')  # Redirect to a sale agent list or confirmation page
    else:
        form = SaleAgentProfileForm()
    
    return render(request, 'sales/sale_agent_profile.html', {'form': form})

def report_page(request):
    return render(request, 'reports/report_page.html')

def generate_report(request):
    if request.method == 'GET':
        report_type = request.GET.get('type')
        report_category = request.GET.get('category')

        # Check for valid parameters
        if report_category == 'sale_agent':
            return generate_sale_agent_report(report_type)
        elif report_category == 'client_record':
            return generate_client_record_report(report_type)
        elif report_category == 'session_log':
            return generate_session_log_report(report_type)
        else:
            return HttpResponse("Invalid report category. Choose 'sale_agent', 'client_record', or 'session_log'.")

    return render(request, 'generate_report.html')  # Render the report selection page


def generate_sale_agent_report(report_type):
    sale_agents = SaleAgent.objects.all()

    if report_type == 'pdf':
        return generate_pdf(sale_agents, "Sale Agents Report")
    elif report_type == 'excel':
        return generate_excel(sale_agents, "Sale Agents Report")
    return HttpResponse("Invalid report type. Use 'pdf' or 'excel'.")


def generate_client_record_report(report_type):
    client_records = ClientRecord.objects.all()

    if report_type == 'pdf':
        return generate_pdf(client_records, "Client Records Report")
    elif report_type == 'excel':
        return generate_excel(client_records, "Client Records Report")
    return HttpResponse("Invalid report type. Use 'pdf' or 'excel'.")


def generate_session_log_report(report_type):
    session_logs = SessionLog.objects.all()

    if report_type == 'pdf':
        return generate_pdf(session_logs, "Session Logs Report")
    elif report_type == 'excel':
        return generate_excel(session_logs, "Session Logs Report")
    return HttpResponse("Invalid report type. Use 'pdf' or 'excel'.")


def generate_pdf(data, title):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{title}.pdf"'

    p = canvas.Canvas(response, pagesize=letter)
    p.drawString(100, 750, title)

    y_position = 730
    for record in data:
        p.drawString(100, y_position, str(record))  # Customize based on your model fields
        y_position -= 20

    p.showPage()
    p.save()
    return response


def generate_excel(data, title):
    wb = Workbook()
    ws = wb.active
    ws.title = title

    # Add headers dynamically
    ws.append([field.name for field in data.model._meta.fields])

    for record in data:
        ws.append([getattr(record, field.name) for field in data.model._meta.fields])

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="{title}.xlsx"'
    wb.save(response)
    return response


# 

def view_session_logs(request):
    """View to display session logs."""
    logs = SessionLog.objects.all().order_by('-timestamp')
    return render(request, 'sales/session_logs.html', {'logs': logs})



@login_required(login_url='login')
def select_days_and_times(request, agent_id):
    """View for managers to select allowed days and times for a sale agent."""
    try:
        sale_agent = User.objects.get(id=agent_id)
    except SaleAgent.DoesNotExist:
        return render(request, 'sales/error.html', {'error': 'SaleAgent not found.'})

    if request.user.groups.filter(name='Manager').exists() or request.user.is_superuser:
        if request.method == 'POST':
            form = SaleAgentForm(request.POST, instance=sale_agent)
            if form.is_valid():
                form.save()
                return redirect('manage_sale_agents')  # Redirect back to the manage sale agents page
        else:
            form = SaleAgentForm(instance=sale_agent)  # Prepopulate the form with existing data

        return render(request, 'sales/select_days_and_times.html', {
            'form': form,
            'sale_agent': sale_agent
        })

    return HttpResponseForbidden("Permission denied.")



def restricted_access(request):
    """View to display an access restriction message."""
    return render(request, 'sales/restricted_access.html')

@login_required(login_url='login')
def manage_sale_agents(request):
    """View for managers to manage sale agents."""
    if request.user.groups.filter(name='Manager').exists() or request.user.is_superuser:
        sale_agents = User.objects.filter(role='sale_agent')
        return render(request, 'sales/manage_sale_agents.html', {'sale_agents': sale_agents})
    return HttpResponseForbidden("Permission denied.")

@login_required
def create_sale_agent(request):
    """Create a new sale agent."""
    if request.user.groups.filter(name='Manager').exists() or request.user.is_superuser:
        if request.method == 'POST':
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')

            # Create the user as a Sale Agent
            sale_agent = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                role='sale_agent'
            )

            # Add the user to the Sale Agent group
            group = Group.objects.get(name='Agent')
            sale_agent.groups.add(group)

            return redirect('manage_sale_agents')

        return render(request, 'sales/create_sale_agent.html')
    return HttpResponseForbidden("Permission denied.")

@login_required
def suspend_sale_agent(request, user_id):
    """Suspend a sale agent."""
    if request.user.groups.filter(name='Manager').exists() or request.user.is_superuser:
        sale_agent = get_object_or_404(User, id=user_id, role='sale_agent')

        # Prevent suspending SuperAdmin
        if sale_agent.role == 'super_admin':
            return HttpResponseForbidden("Permission denied.")

        # Suspend the user by deactivating the account
        sale_agent.is_active = False
        sale_agent.save()

        return redirect('manage_sale_agents')
    return HttpResponseForbidden("Permission denied.")

@login_required
def activate_sale_agent(request, agent_id):
    """Activate a suspended sale agent."""
    if request.user.groups.filter(name='Manager').exists() or request.user.is_superuser:
        agent = get_object_or_404(User, id=agent_id, role='sale_agent')
        if not agent.is_active:
            agent.is_active = True
            agent.save()
        return redirect('manage_sale_agents')
    return HttpResponseForbidden("Permission denied.")



@staff_member_required
def change_approval_status(request, record_id):
    # Fetch the client record
    client_record = get_object_or_404(ClientRecord, id=record_id)
    
    # Ensure the user is a manager
    if not request.user.groups.filter(name='Manager').exists() and not request.user.is_superuser:
        return HttpResponseForbidden("You do not have permission to change approval status.")
    
    # Get the new approval status from the form submission
    new_status = request.POST.get('approval_status')  # Get the value selected by the manager
    
    # Check if the new status is a valid choice
    valid_statuses = dict(ClientRecord.APPROVAL_CHOICES).keys()
    if new_status in valid_statuses:
        # Update the approval status
        client_record.approval_status = new_status
        client_record.save()

        # Create a notification for the sale agent who entered the record
        notification_message = f"The approval status of your client record for {client_record.business_name} has been changed to {new_status}."
        Notification.objects.create(
            user=client_record.sale_agent,
            message=notification_message
        )

        # Show success message to the manager
        messages.success(request, f"Approval status of {client_record.business_name} changed to {new_status}.")
    else:
        # If an invalid status was provided
        messages.error(request, "Invalid approval status selected.")

    return redirect('manager_dashboard')


@login_required
def dismiss_notification(request, notification_id):
    """Mark a notification as read."""
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    return redirect('sale_agent_dashboard')

# View for adding a client record
def add_client_record(request):
    if request.method == "POST":
        # Create a form instance with POST data
        form = ClientRecordForm(request.POST)
        
        if form.is_valid():
            # Create and save the new client record
            client_record = form.save(commit=False)
            client_record.sale_agent = request.user  # Associate with the logged-in sale agent
            client_record.save()

            # Create a notification for the manager
            manager = User.objects.filter(is_staff=True).first()  # Get the first manager (or modify this as needed)
            if manager:
                Notification.objects.create(
                    user=manager,
                    message=f"A new client record has been added by {request.user.username}.",
                )
            
            # Provide feedback to the user
            messages.success(request, 'Client record added successfully!')
            
            # Redirect to a success page or dashboard
            return redirect('sale_agent_dashboard')  # Adjust this to your desired redirect page

        else:
            # If form is invalid, return the same page with error messages
            messages.error(request, 'There was an error with your form. Please try again.')
            return render(request, 'sales/add_client_record.html', {'form': form})

    else:
        # If GET request, create an empty form
        form = ClientRecordForm()

    return render(request, 'sales/add_client_record.html', {'form': form})


@login_required
def notifications_view(request):
    """Display notifications for the logged-in user."""
    notifications = request.user.notifications.order_by('-created_at')
    unread_count = notifications.filter(is_read=False).count()  # Count unread notifications
    return render(request, 'notifications.html', {'notifications': notifications, 'unread_count': unread_count})


@login_required
def mark_notification_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id)
    notification.is_read = True
    notification.save()

    return redirect('manager_dashboard')




@staff_member_required
def custom_admin_view(request):
    """Redirect to admin dashboard."""
    return redirect('admin:index')


@login_required
def sale_agent_dashboard(request):
    """Dashboard for sale agents."""
    if request.user.groups.filter(name='Agent').exists() or request.user.is_superuser:
        # Fetch notifications for the logged-in sale agent
        notifications = Notification.objects.filter(user=request.user, is_read=False)

        # Fetch all client records
        client_records = ClientRecord.objects.filter()

        return render(
            request, 
            'sales/sale_agent_dashboard.html', 
            {'notifications': notifications, 'client_records': client_records}
        )
    return HttpResponseForbidden("Permission denied.")


@login_required
def manager_dashboard(request):
    """Dashboard for managers."""
    if request.user.groups.filter(name='Manager').exists() or request.user.is_superuser:
        # Fetch unread notifications
        notifications = Notification.objects.filter(is_read=False)

        # Fetch all client records
        client_records = ClientRecord.objects.all()

        # Render the manager dashboard
        return render(request, 'sales/manager_dashboard.html', {
            'notifications': notifications,
            'client_records': client_records
        })
    
    return HttpResponseForbidden("Permission denied.")


@staff_member_required
def super_admin_dashboard(request):
    """Dashboard for super administrators."""
    return render(request, 'sales/super_admin_dashboard.html')


@login_required
def client_record_detail(request, pk):
    """Detail view for a client record."""
    client_record = get_object_or_404(ClientRecord, pk=pk, sale_agent=request.user)
    return JsonResponse({
        "name": client_record.business_name,
        "phone_number": client_record.contact_info,
        "address": client_record.location,
    })


class ClientRecordListView(LoginRequiredMixin, ListView):
    """List view for client records."""
    model = ClientRecord
    template_name = "sales/client_record_list.html"
    context_object_name = "client_records"

    def get_queryset(self):
        return ClientRecord.objects.filter(sale_agent=self.request.user)


class CustomLoginView(LoginView):
    """Custom login view with role-based redirection."""
    template_name = 'sales/login.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        user = form.get_user()
        # Check if the user role is authorized
        if user.role in ['sale_agent', 'manager', 'super_admin']:
            return super().form_valid(form)
        else:
            # Logout unauthorized users and show an error
            logout(self.request)
            form.add_error(None, "You are not authorized to log in.")
            return self.form_invalid(form)

    def get_success_url(self):
        """Redirect users to their respective dashboards based on their role."""
        user = self.request.user
        if user.role == 'sale_agent':
            return reverse_lazy('sale_agent_dashboard')
        elif user.role == 'manager':
            return reverse_lazy('manager_dashboard')
        elif user.role == 'super_admin':
            return reverse_lazy('super_admin_dashboard')
        else:
            return reverse_lazy('login')  # Fallback URL for unexpected cases
