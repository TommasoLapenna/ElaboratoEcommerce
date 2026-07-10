from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

# Per fare in modo che il ruolo sia visibile ed editabile nel pannello di Django
class UserAdmin(BaseUserAdmin):
    list_display = BaseUserAdmin.list_display + ('role',)
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Role', {'fields': ('role',)}),
    )
admin.site.register(User, UserAdmin)
