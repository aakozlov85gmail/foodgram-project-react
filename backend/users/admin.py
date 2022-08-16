from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Subscription


@admin.register(User)
class UserAdmin(UserAdmin):
    ordering = ('username',)
    list_display = (
        'username',
        'first_name',
        'last_name',
        'email',
    )
    list_filter = (
        'username',
        'email',
    )


@admin.register(Subscription)
class SubscribtionAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'author',
    )
    search_fields = ('user',)
