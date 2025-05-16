import os
from celery import shared_task
from datetime import timedelta
from config.settings import BASE_DIR
from django.utils.timezone import localtime
from django.db.models import Exists, OuterRef
from api_notify.models import LogMessage, Message
from api_notify.services.mailing import send_message


@shared_task
def send_messages(*args):
    file_name = str(BASE_DIR) + os.sep + "log.txt"
    current_datetime = localtime()
    # Подзапрос для проверки существует ли LogMessage
    # со статусом S (Отправлено) для конкретного сообщения
    sent_log_exists = LogMessage.objects.filter(
        message=OuterRef('pk'),
        status='S'
    )

    # Выбираем все сообщения, для которых нет отправленного лога
    message_objects = Message.objects.annotate(
        has_sent_log=Exists(sent_log_exists)
    ).filter(
        has_sent_log=False
    )

    with open(file_name, "a", encoding="UTF-8") as file:
        file.write(f"Сообщений для отправки: {len(message_objects)}\n")

    for message_object in message_objects:
        if (
            message_object.daytime_for_send < current_datetime
            or message_object.daytime_for_send - current_datetime <= timedelta(
                minutes=1
            )
        ):
            log_message_object = LogMessage(
                message=message_object,
                daytime_send=current_datetime,
                status="N"
            )
            log_message_object.save()
            try:
                status, server_answer = send_message(
                    message_object.text,
                    message_object.recepient
                )
                if status == 'successfully':
                    log_message_object.status = 'S'
                    log_message_object.save()
                    with open(file_name, "a", encoding="UTF-8") as file:
                        text = f"Send message status={status}, "
                        text += f"server_answer={server_answer}, "
                        text += f"{message_object}\n"
                        file.write(text)
                else:
                    with open(file_name, "a", encoding="UTF-8") as file:
                        text = f"Unsuccessfully {message_object}\n"
                        file.write(text)

            except Exception as e:
                with open(file_name, "a", encoding="UTF-8") as file:
                    file.write(f"Error {e} {message_object}\n")
