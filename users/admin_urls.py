from django.urls import path
from . import views_admin 

app_name = 'admin'  # namespace diverso per admin

urlpatterns = [
    path('login/', views_admin.AdminLoginView.as_view(), name='login'),
    path('users_approval/', views_admin.AdminUserApprovalView.as_view(), name='users_approval'),
    path('user_details/<int:user_id>/', views_admin.AdminUserDetails.as_view(), name='user_details_api'),
    #path('dashboard/', views.AdminDashboardView.as_view(), name='dashboard'),
]
