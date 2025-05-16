import os
from celery import shared_task
from datetime import timedelta
from config.settings import BASE_DIR
from django.utils.timezone import localtime
from api_notify.models import LogMessage


@shared_task
def send_messages(*args):
    file_name = str(BASE_DIR) + os.sep + "log.txt"
    current_datetime = localtime()
    log_message_objects = LogMessage.objects.filter(status='N')
    for log_message_object in log_message_objects:
        if log_message_object.daytime_send - current_datetime <= \
                timedelta(minutes=1):
            log_message_object.status = 'S'
            log_message_object.save()
            with open(file_name, "a", encoding="UTF-8") as file:
                file.write(f"Send message {log_message_object}\n")
