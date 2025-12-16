from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Role

@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    model = User

    list_display = ('username', 'role', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'role')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('role',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'role', 'password1', 'password2'),
        }),
    )

    search_fields = ('username',)
    ordering = ('username',)

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'level')  # مثال: لو عندك level أو أي field تاني
