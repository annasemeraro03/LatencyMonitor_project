from django.urls import path
from .views import LoginStatsView

app_name = 'analytics'

urlpatterns = [
    path('', LoginStatsView.as_view(), name='list'),
]
