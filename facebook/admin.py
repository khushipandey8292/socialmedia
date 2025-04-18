from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('id','username', 'email', 'user_type', 'is_verified', 'is_staff', 'is_superuser')
    list_filter = ('user_type', 'is_verified', 'is_staff')
    search_fields = ('username', 'email')
    ordering = ('username',)

    fieldsets = UserAdmin.fieldsets + (
        ('Extra Info', {'fields': ('user_type', 'is_verified', 'phone', 'address')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
