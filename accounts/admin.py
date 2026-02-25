from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Profile

# Define an inline admin descriptor for Profile model
# This will be displayed within the User admin page
class ProfileInline(admin.StackedInline): # Use StackedInline or TabularInline
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'

# Extend the default UserAdmin
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)

# Re-register the User model with the custom UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)