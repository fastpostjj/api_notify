from django.contrib import admin
from api_notify.models import Message, LogMessage


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'text')
    list_display_links = ('id', 'text')
    list_filter = ('id', 'text')
    search_fields = ('id', 'text')


@admin.register(LogMessage)
class LogMessageAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'message',
        'daytime_send',
        'recepient',
        'status'
        )
    list_display_links = (
        'id',
        'message',
        'daytime_send',
        'recepient',
        'status',
        )
    list_filter = (
        'id',
        'message',
        'daytime_send',
        'recepient',
        'status',
        )
    search_fields = (
        'id',
        'message',
        'daytime_send',
        'recepient',
        'status',
        )
