import re
import requests
from django.core.mail import send_mail
from config.settings import EMAIL_HOST_USER, BOT_TOKEN
from smtplib import SMTPException


def is_valid_email(email) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def send_email(subject, message_body, email) -> str:
    status = 'successfully'
    try:
        send_mail(
            subject,
            message_body,
            EMAIL_HOST_USER,
            [email],
            fail_silently=False
        )
    except SMTPException:
        status = 'unsuccessfully'
    return status


def send_telegram_message(text, recepient) -> str:
    chat_id = recepient
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/"
    url += f"sendMessage?chat_id={chat_id}&text={text}"
    answer = requests.get(url).json()
    status = answer.get('ok')
    if status:
        return 'successfully'
    else:
        return 'unsuccessfully'


def send_message(text, recepient) -> str:
    """
    Отправка сообщения на email или в телеграм
    """
    # Определяем, куда будем отправлять в зависимости от получателя
    if recepient.isdigit():
        # Если в адресе все числа,то в телеграм
        status = send_telegram_message(text, recepient)
    elif is_valid_email(recepient):
        # Если это email, то на почту
        status = send_email(text, text, recepient)
    else:
        status = "Адрес указан неверно"
    return status
