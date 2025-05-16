from django.db import models
from config.settings import NULLABLE


class Message(models.Model):
    """
    Класс сообщений, отправляемых пользователям.
    - text - текст сообщения
    - recepient - адрес получателя
    - daytime_for_send - запланированные время и дата отправки
    """
    text = models.CharField(
        max_length=1024,
        verbose_name="Текст сообщения",
    )
    recepient = models.CharField(
        max_length=150,
        verbose_name="Получатель",
        **NULLABLE
    )
    daytime_for_send = models.DateTimeField(
        verbose_name="Дата и время отправки",
        **NULLABLE
    )

    def __str__(self) -> str:
        text = f'{self.text} Получатель: {self.recepient} '
        text += f'Дата и время отправки: {self.daytime_for_send}'
        return text


class LogMessage(models.Model):
    """
    Класс логов об отправке сообщений.
    - message- объект класса Message
    - daytime_send - дата и время попытки отправки сообщения
    - status - статус отправки ('Не отправлено'/'Отправлено')
    """
    STATUS_SENDING = [
        ('N', 'Не отправлено'),
        ('S', 'Отправлено'),
    ]
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        **NULLABLE,
        verbose_name="Текст сообщения",
    )
    daytime_send = models.DateTimeField(
        verbose_name="Дата и время попытки отправки",
        **NULLABLE
    )
    status = models.CharField(
        max_length=13,
        verbose_name="Статус отправки",
        choices=STATUS_SENDING,
        default='N',
        **NULLABLE,
    )

    def __str__(self) -> str:
        text = f'{self.message} Статус: {self.status} '
        text += f'Дата и время отправки: {self.daytime_send}'
        return text
