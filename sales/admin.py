from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Custom user admin panel
class CustomUserAdmin(UserAdmin):
    models = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        ('Role Information', {'fields': ('role', 'phone')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Role Information', {'fields': ('role', 'phone')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)