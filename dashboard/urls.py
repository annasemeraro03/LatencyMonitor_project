from django.urls import path
from .views import DashboardView, DeviceDetailView, DevicePrintView

app_name = 'dashboard'

urlpatterns = [
    path('', DashboardView.as_view(), name='view'),
    path('device/<int:pk>/', DeviceDetailView.as_view(), name='device_detail'),
    path('device/<int:pk>/print/', DevicePrintView.as_view(), name='device_print'),
]
