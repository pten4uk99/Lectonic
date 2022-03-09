from rest_framework import serializers

from workroomsapp.models import Customer


class CustomerCreateSerializer(serializers.Serializer):
    domain = serializers.ListField()
    education = serializers.CharField(required=False)
    hall_address = serializers.CharField(max_length=200, required=False)

    class Meta:
        fields = [
            'domain',
            'education',
            'hall_address'
        ]

    def validate_domain(self, domain):
        try:
            validated_domain = list(map(int, domain))
        except ValueError:
            raise serializers.ValidationError('Тематика должна быть числом')

        return validated_domain

    def create(self, validated_data):
        return Customer.objects.create_customer(
            person=self.context['request'].user.person,
            domain=validated_data.get('domain'),
            hall_address=validated_data.get('hall_address'),
            equipment=validated_data.get('equipment'),
        )
