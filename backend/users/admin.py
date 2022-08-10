from django.contrib import admin

from .models import User, Subscription


class UserAdmin(admin.ModelAdmin):
    ordering = ('username',)
    list_display = ('username',
                    'first_name',
                    'last_name',
                    'email',)
    list_filter = ('username', 'email',)


class SubscribtionAdmin(admin.ModelAdmin):
    list_display = ('user', 'author',)
    search_fields = ('user',)


admin.site.register(User, UserAdmin)
admin.site.register(Subscription, SubscribtionAdmin)
