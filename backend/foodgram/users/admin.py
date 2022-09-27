from django.contrib import admin

from .models import Follow, User

admin.site.register(Follow)


class UserAdmin(admin.ModelAdmin):
    """Настройка отображенения модели User в админ-панели"""
    list_display = ('email', 'first_name', 'last_name', 'username', )
    list_filter = ('username', 'email')


admin.site.register(User, UserAdmin)
