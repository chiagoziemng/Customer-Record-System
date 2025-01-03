from django.urls import path
from .views import CustomLoginView, ClientRecordListView, client_record_detail, sale_agent_dashboard,  super_admin_dashboard, manager_dashboard

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('client-records/', ClientRecordListView.as_view(), name='client-records'),
    path('client-records/<int:pk>/', client_record_detail, name='client-record-detail'),
    path('client-records/<int:id>/', client_record_detail, name='client_record_detail'),

    path('sale_agent_dashboar/', sale_agent_dashboard, name='sale_agent_dashboard'),
    path('manager_dashboard/', manager_dashboard, name='manager'),
    path('super_admin_dashboard/', super_admin_dashboard, name='super_admin_dashboard'),

]