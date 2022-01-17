from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *
from .forms import CustomUserCreationForm, CustomUserChangeForm


class UserProfileAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = UserProfile
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(UserProfile, UserProfileAdmin)


@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    pass
