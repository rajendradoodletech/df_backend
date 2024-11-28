from django.contrib import admin
from .models import CustomUser, UserRole
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

# Register your models here.

class UserAdmin(BaseUserAdmin):
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ["email", "is_admin", "role"]
    list_filter = ["is_admin"]
    search_fields = ('email', 'first_name', 'last_name',)
    fieldsets = [
        (None, {"fields": ["email", "password"]}),
        ("Permissions", {"fields": ["is_active", "is_admin", "is_superuser", "role", "user_permissions"]}),
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "password1", "password2", "role"],
            },
        ),
    ]
    search_fields = ["email"]
    ordering = ["email"]
    filter_horizontal = []


admin.site.register(CustomUser, UserAdmin)
admin.site.register(UserRole)
admin.site.unregister(Group)