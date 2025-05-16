from datetime import timedelta
from django.utils.timezone import localtime
from rest_framework import generics, status
from rest_framework.response import Response
from api_notify.serializer import MessageRequestSerializer
from api_notify.models import Message


class MessageCreateAPIView(generics.CreateAPIView):
    """
    create view Message
    """
    serializer_class = MessageRequestSerializer
    queryset = Message.objects.all()

    def post(self, request, *args, **kwargs):
        data = request.data
        recepient_data = data.get('recepient')
        if isinstance(recepient_data, str):
            data['recepient'] = [recepient_data]

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        message_data = request.data.get('message')
        recepients = request.data.get('recepient')
        delay = request.data.get('delay', 0)
        if delay == 0:
            daytime_for_send = localtime()
        elif delay == 1:
            daytime_for_send = localtime() + timedelta(hours=1)
        elif delay == 2:
            daytime_for_send = localtime() + timedelta(days=1)
        try:
            if isinstance(recepients, str):
                message_object = Message(
                    text=message_data,
                    recepient=recepients,
                    daytime_for_send=daytime_for_send,
                )
                message_object.save()

            elif isinstance(recepients, list):
                message_entries = []
                for recepient in recepients:
                    message_object = Message(
                        text=message_data,
                        recepient=recepient,
                        daytime_for_send=daytime_for_send,
                    )
                    message_entries.append(message_object)
                Message.objects.bulk_create(message_entries)
        except Exception as e:
            return Response(
                {"Status": e},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            {"Status": "Successful"},
            status=status.HTTP_201_CREATED
        )
