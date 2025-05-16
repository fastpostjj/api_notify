from rest_framework import serializers


class MessageRequestSerializer(serializers.Serializer):
    message = serializers.CharField(
        max_length=1024,
        required=True,
    )
    recepient = serializers.ListField(
        child=serializers.CharField(max_length=150),
        allow_empty=False,
        required=True,
    )
    delay = serializers.IntegerField(
        required=True,
    )

    def validate_recepient(self, value):
        if isinstance(value, list):
            if not all(
                isinstance(item, str)
                    and len(item) <= 150
                    for item in value):
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
