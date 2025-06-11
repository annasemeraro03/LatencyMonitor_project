from django.urls import path
from . import views

app_name = 'issues'

urlpatterns = [
    path('', views.pending_issues_view, name='list'),  # unica view che mostra tutto
    path("pending/", views.pending_issues_view, name="pending_issues"),
    path("approve/<int:issue_id>/", views.approve_issue, name="approve"),
    path("reject/<int:issue_id>/", views.reject_issue, name="reject"),
]
