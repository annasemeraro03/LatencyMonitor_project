from django.urls import path
from . import views

app_name = 'issues' 

urlpatterns = [
    path('', views.list_issues, name='list'),
]
