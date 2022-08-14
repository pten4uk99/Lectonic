from rest_framework import serializers


class LecturesListGetParamsSerializer(serializers.Serializer):
    city = serializers.CharField(default=None)
    domain = serializers.CharField(default=None)


class LectureGetParamsSerializer(LecturesListGetParamsSerializer):
    user_id = serializers.IntegerField(
        help_text='Пользователь, чью лекцию берем. По умолчанию - пользователь, делающий запрос.',
        default=None)
    
