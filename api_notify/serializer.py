from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from api_notify.models import Message, LogMessage


# class IsStrOrList:
#     def __call__(self, values):
#         """Валидация данных строки recipients. """
#         if isinstance(values, list):
#             for val in values:
#                 if not isinstance(val, str) or len(val) > 150:
#                     raise ValidationError('Recepient должен быть строкой до 150 символов.')(val)
#         elif isinstance(values, str):
#             if not isinstance(values, str) or len(values) > 150:
#                 raise ValidationError('Recepient должен быть строкой до 150 символов.')(values)
#         else:
#             raise ValidationError('Recepient должен быть строкой или списком строк.')


# class MessageSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = Message
#         fields = (
#             'id',
#             'text',
#             )


# class LogMessageSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = LogMessage
#         fields = (
#             'id',
#             'message',
#             'daytime_send',
#             'recepient',
#             'status',
#         )


class MessageRequestSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=1024)
    # recepient = serializers.ListField(
    #     child=serializers.CharField(max_length=150),
    recepient = serializers.CharField(
        max_length=150,
        # validators=[IsStrOrList(), ],
        # child=serializers.CharField(max_length=150),
        # allow_empty=False,
        required=False
    )
    delay = serializers.IntegerField(default=0)

    def validate_recipient(self, value):
        if isinstance(value, list):
            if not all(
                isinstance(
                    item,
                    str
                    ) and len(item) <= 150 for item in value):
                text_error = "Все элементы списка должны быть строками "
                text_error += "длиной до 150 символов."
                raise serializers.ValidationError(text_error)
            return value
        elif isinstance(value, str):
            return [value]
        else:
            text_error = "Значение 'recepient' должно быть строкой "
            text_error += "или списком строк."
            raise serializers.ValidationError(text_error)

    def validate(self, attrs):
        if 'recepient' not in attrs or not attrs['recepient']:
            text_error = "Поле 'recepient' не может быть пустым."
            raise serializers.ValidationError(text_error)
        return attrs

    def validate_delay(self, value):
        if value not in (0, 1, 2):
            text_error = "Значение 'delay' должно быть 0, 1 или 2."
            raise serializers.ValidationError(text_error)
