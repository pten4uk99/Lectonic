import re

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

errors = {
    'blank': 'Поле не может быть пустым',
    'required': 'Обязательное поле',
    'invalid': 'e-mail введен некорректно'
}


class EmailSerializer(serializers.Serializer):
    email = serializers.CharField(error_messages=errors)

    class Meta:
        fields = (
            'email',
        )

    def validate_email(self, email):
        '''
        Валидация эмейла

        1. В строке может быть только один символ '@' и одна '.'
        2. До '@' могут быть любые буквы, цифры и '.'
        3. После '@' могут быть любые буквы и цифры
        4. После точки может быть от 2-х до 4-х латинских маленьких буквы
        5. В строке не может быть пробелов
        '''

        match = re.findall(r'^[\w.]+@\w+\.[a-z]{2,4}$', email)

        if not match:
            raise ValidationError('Некорректный эмейл')

        return email
