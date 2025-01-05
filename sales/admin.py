from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, ClientRecord, Notification, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(ClientRecord)
class ClientRecordAdmin(admin.ModelAdmin):
    list_display = ['business_name', 'location', 'owner_name', 'category', 'contact_info', 'status_indicator']
    list_filter = ['category','status_indicator']
    search_fields = ['business_name', 'owner_name']
    actions = ['approve_records', 'reject_records']
# @admin.register(ClientRecord)
# # class ClientRecordAdmin(admin.ModelAdmin):
# #     list_display = ['field1', 'field2', 'field3']
# #     search_fields = ['field1', 'field2']
# #     list_filter = ['field4']

# Custom user admin panel
class CustomUserAdmin(UserAdmin):
    models = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        ('Role Information', {'fields': ('role', 'phone', 'failed_login_attempts')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Role Information', {'fields': ('role', 'phone', 'failed_login_attempts')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Notification)