from django.urls import path
from .views import DashboardView, DeviceDetailView

app_name = 'dashboard'

urlpatterns = [
    path('', DashboardView.as_view(), name='view'),
    path('device/<int:pk>/', DeviceDetailView.as_view(), name='device_detail'),
]
