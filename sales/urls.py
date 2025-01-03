from django.urls import path
from .views import CustomLoginView, ClientRecordListView, client_record_detail

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('client-records/', ClientRecordListView.as_view(), name='client-records'),
    path('client-records/<int:pk>/', client_record_detail, name='client-record-detail')
]