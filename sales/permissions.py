from django.contrib.auth.models import Permission


def create_permissions():
    permissions = [
        ('view_saleagent_dashboard', 'Can view SaleAgent dashboard'),
        ('view_manager_dashboard', 'Can view Manager dashboard'),
    ]
    for codename, name in permissions:
        Permission.objects.get_or_create(codename=codename, name=name)