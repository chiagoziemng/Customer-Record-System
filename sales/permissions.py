

from django.contrib.auth.models import Permission

def create_permissions():
    # Permissions for SaleAgent and Manager dashboards
    permissions = [
        ('view_saleagent_dashboard', 'Can view SaleAgent dashboard'),
        ('view_manager_dashboard', 'Can view Manager dashboard'),
        ('create_saleagent', 'Can create SaleAgents'),
        ('suspend_saleagent', 'Can suspend SaleAgents'),
        ('approve_client_record', 'Can approve client records'),
    ]
    
    # Create permissions for each entry
    for codename, name in permissions:
        Permission.objects.get_or_create(codename=codename, name=name)
