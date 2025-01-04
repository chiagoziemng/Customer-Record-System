from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import activate_sale_agent,suspend_sale_agent, manage_sale_agents, create_sale_agent, CustomLoginView,dismiss_notification,change_approval_status, add_client_record,mark_notification_read, ClientRecordListView,notifications_view, client_record_detail, sale_agent_dashboard,  super_admin_dashboard, manager_dashboard, custom_admin_view

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('client-records/', ClientRecordListView.as_view(), name='client-records'),
    path('client-records/<int:pk>/', client_record_detail, name='client-record-detail'),
    path('client-records/<int:id>/', client_record_detail, name='client_record_detail'),

    path('sale_agent_dashboard/', sale_agent_dashboard, name='sale_agent_dashboard'),
    path('manager_dashboard/', manager_dashboard, name='manager_dashboard'),
    path('super_admin_dashboard/', super_admin_dashboard, name='super_admin_dashboard'),

    path('custom-admin/', custom_admin_view),
    path('notifications/', notifications_view, name='notifications'),
    # path('notifications/read/<int:notification_id>/', mark_notification_as_read, name='mark_notification_as_read'),


    path('logout/', LogoutView.as_view(), name='logout'),
     path('add-client-record/', add_client_record, name='add_client_record'),
      path('mark-notification-read/<int:notification_id>/', mark_notification_read, name='mark_notification_read'),
      path('change-approval-status/<int:record_id>/', change_approval_status, name='change_approval_status'),
    path('dismiss-notification/<int:notification_id>/', dismiss_notification, name='dismiss_notification'),


        path('manage-sale-agents/', manage_sale_agents, name='manage_sale_agents'),
    path('create-sale-agent/', create_sale_agent, name='create_sale_agent'),
    path('suspend-sale-agent/<int:user_id>/', suspend_sale_agent, name='suspend_sale_agent'),
        path('activate-sale-agent/<int:agent_id>/', activate_sale_agent, name='activate_sale_agent'),


]
