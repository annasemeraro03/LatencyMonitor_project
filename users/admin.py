from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        ('Extra info', {'fields': ('is_researcher', 'is_approved', 'birth_date', 'profile_image')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
