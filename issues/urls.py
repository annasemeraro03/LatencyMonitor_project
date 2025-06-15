from django.urls import path
from . import views

app_name = 'issues'

urlpatterns = [
    path('', views.PendingIssuesView.as_view(), name='list'),
    path('pending/', views.PendingIssuesView.as_view(), name='pending_issues'),
    path('approve/<int:issue_id>/', views.ApproveIssueView.as_view(), name='approve'),
    path('reject/<int:issue_id>/', views.RejectIssueView.as_view(), name='reject'),
    path('create/', views.CreateIssueView.as_view(), name='create_issue'),
    path('get-models/', views.get_models, name='get_models'),
    path('get-experiments/', views.get_experiments, name='get_experiments'),
    path('<int:issue_id>/resolve/', views.ResolveIssueView.as_view(), name='resolve_issue'),
]
