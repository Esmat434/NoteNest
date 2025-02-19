from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser,Profile,Auth_Token
# Register your models here.

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = [
        "id",
        "email",
        "username",
        "is_superuser",
        "is_staff",
        "is_active"
    ]

    fieldsets = (
        (None, {"fields": ("username","email",'phone_number',"password")}),
        ("Personal info", {"fields": ("first_name", "last_name",'country','city','picture','address','birth_date')}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username",'email','phone_number', "password1", "password2"),
            },
        ),
    )

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id','user','is_enable','created_time','updated_time']
    list_filter = ['is_enable']
    search_fields = ['user']

@admin.register(Auth_Token)
class Auth_TokenAdmin(admin.ModelAdmin):
    list_display = ['key','user','created_at']