from django.urls import path
from . import views
from .views import (
    ExperimentListView,
    ExperimentDetailView,
    ExperimentCreateView,
    DeviceCreateView,
    ExperimentRemoveView,
    EditNotesView,
    SearchExperimentsView,
    DeviceRemoveView
)

app_name = 'experiments'

urlpatterns = [
    path('', ExperimentListView.as_view(), name='list'),
    path('<int:experiment_id>/', ExperimentDetailView.as_view(), name='detail'),
    path('create_device/', DeviceCreateView.as_view(), name='create_device'),
    path('create_experiment/', ExperimentCreateView.as_view(), name='create_experiment'),
    path('get-models/', views.get_models, name='get-models'),
    path('remove/', ExperimentRemoveView.as_view(), name='remove_experiment'),
    path('edit_notes/', EditNotesView.as_view(), name='edit_notes'),
    path('get-experiments/', views.get_experiments_by_device, name='get_experiments'),
    path("get-experiment-notes/", views.get_experiment_notes, name="get_experiment_notes"),
    path('search/', SearchExperimentsView.as_view(), name='experiment_search'),
    path('experiment/<int:pk>/', views.experiment_detail, name='experiment_detail'),
    path('remove-device/', DeviceRemoveView.as_view(), name='remove_device')
]
