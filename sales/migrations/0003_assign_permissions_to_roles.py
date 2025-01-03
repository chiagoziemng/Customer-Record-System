# Generated by Django 5.1.4 on 2025-01-03 21:09

from django.db import migrations
from django.contrib.auth.models import Group, Permission
from sales.permissions import create_permissions
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from ..models import SaleAgent, Manager

def create_permissions():
    # Get content types for the models
    sale_agent_content_type = ContentType.objects.get_for_model(SaleAgent)
    manager_content_type = ContentType.objects.get_for_model(Manager)

    # Create permissions for SaleAgent model
    Permission.objects.get_or_create(
        codename='view_saleagent_dashboard',
        name='Can view SaleAgent Dashboard',
        content_type=sale_agent_content_type
    )

    # Create permissions for Manager model
    Permission.objects.get_or_create(
        codename='view_manager_dashboard',
        name='Can view Manager Dashboard',
        content_type=manager_content_type
    )


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0002_alter_clientrecord_sale_agent'),
    ]

    operations = [
        
    ]