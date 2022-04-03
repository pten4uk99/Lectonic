from rest_framework import serializers

from workroomsapp.models import Customer, Domain


class CustomerCreateSerializer(serializers.Serializer):
    domain = serializers.ListField()
    company_name = serializers.CharField(required=False)
    company_description = serializers.CharField(required=False)
    company_site = serializers.CharField(required=False)
    education = serializers.CharField(required=False)
    hall_address = serializers.CharField(max_length=200, required=False)

    class Meta:
        fields = [
            'domain',
            'company_name',
            'company_description',
            'company_site',
            'education',
            'hall_address'
        ]

    def validate_domain(self, domain):
        for name in domain:
            if not Domain.objects.filter(name=name).exists():
                raise serializers.ValidationError('Данной тематики не существует')
        return domain

    def create(self, validated_data):
        return Customer.objects.create_customer(
            person=self.context['request'].user.person,
            domain=validated_data.get('domain'),
            company_name=validated_data.get('company_name'),
            company_description=validated_data.get('company_description'),
            company_site=validated_data.get('company_site'),
            hall_address=validated_data.get('hall_address'),
            equipment=validated_data.get('equipment'),
        )
