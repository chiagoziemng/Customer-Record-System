from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, ClientRecord


# @admin.register(ClientRecord)
# # class ClientRecordAdmin(admin.ModelAdmin):
# #     list_display = ['field1', 'field2', 'field3']
# #     search_fields = ['field1', 'field2']
# #     list_filter = ['field4']

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
admin.site.register(ClientRecord)