from django.contrib import admin
from api_notify.models import Message, LogMessage


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'text',
        'daytime_for_send',
        'recepient',
    )
    list_display_links = (
        'id',
        'text',
        'daytime_for_send',
        'recepient',
    )
    list_filter = (
        'id',
        'text',
        'daytime_for_send',
        'recepient',
    )
    search_fields = (
        'id',
        'text',
        'daytime_for_send',
        'recepient',
    )


@admin.register(LogMessage)
class LogMessageAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'message',
        'daytime_send',
        'status'
    )
    list_display_links = (
        'id',
        'message',
        'daytime_send',
        'status',
    )
    list_filter = (
        'id',
        'message',
        'daytime_send',
        'status',
    )
    search_fields = (
        'id',
        'message',
        'daytime_send',
        'status',
    )
