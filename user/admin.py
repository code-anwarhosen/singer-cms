from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from user.models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # Show these fields in the admin user list
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    
    # Add custom fields to the user edit form
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('avatar', 'bio')}),
    )

    # Add custom fields to the user creation form
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('avatar', 'bio')}),
    )
