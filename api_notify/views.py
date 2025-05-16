from datetime import timedelta
from django.utils.timezone import localtime
from rest_framework import generics, status
from rest_framework.response import Response
from api_notify.services.mailing import send_message
from api_notify.serializer import MessageRequestSerializer
from api_notify.models import Message, LogMessage


class MessageCreateAPIView(generics.CreateAPIView):
    """
    create view Message
    """
    serializer_class = MessageRequestSerializer
    queryset = Message.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message_data = request.data.get('message')
        recepients = request.data.get('recepient')
        delay = request.data.get('delay', 0)
        if delay == 0:
            daytime_send = localtime()
        elif delay == 1:
            daytime_send = localtime() + timedelta(hours=1)
        elif delay == 2:
            daytime_send = localtime() + timedelta(days=1)
        if recepients:
            try:
                message_object = Message(text=message_data)
                message_object.save()

                if isinstance(recepients, str):
                    # send_message(message_data, recepients)
                    log_meassage_object = LogMessage(
                        message=message_object,
                        daytime_send=daytime_send,
                        recepient=recepients,
                        status="N"
                        )
                    log_meassage_object.save()

                elif isinstance(recepients, list):
                    log_entries = []
                    for recepient in recepients:
                        # send_message(message_data, recepient)

                        log_message_object = LogMessage(
                            message=message_object,
                            daytime_send=daytime_send,
                            recepient=recepient,
                            status="N"
                            )
                        # log_message_object.save()
                        log_entries.append(log_message_object)
                    LogMessage.objects.bulk_create(log_entries)
            except Exception as e:
                return Response(
                    {"Status": e},
                    status=status.HTTP_400_BAD_REQUEST
                    )
        else:
            return Response(
                {"Status": "Неверный формат данных"},
                status=status.HTTP_400_BAD_REQUEST
                )

        return Response(
            {"Status": "Successful"},
            status=status.HTTP_201_CREATED
            )
