from django.urls import path
from . import views
from .views import (
    ExperimentListView,
    ExperimentDetailView,
    ExperimentCreateView,
    DeviceCreateView
)

app_name = 'experiments'

urlpatterns = [
    path('', ExperimentListView.as_view(), name='list'),
    path('<int:experiment_id>/', ExperimentDetailView.as_view(), name='detail'),
    path('create_device/', DeviceCreateView.as_view(), name='create_device'),
    path('create_experiment/', ExperimentCreateView.as_view(), name='create_experiment'),
    path('get-models/', views.get_models, name='get-models'),
]
