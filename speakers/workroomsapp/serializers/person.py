from datetime import date

from rest_framework import serializers

from workroomsapp.models import City, Domain


class PersonCreateSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    middle_name = serializers.CharField(max_length=100)
    birth_date = serializers.DateField(null=False, blank=False, default=date.today)
    city = serializers.PrimaryKeyRelatedField(queryset=City.objects.all())
    address = serializers.CharField(max_length=200, null=True, blank=True)
    rating = serializers.IntegerField(default=0, null=True, blank=True)
    photo = serializers.CharField(max_length=200, null=True, blank=True)
    user = serializers.PrimaryKeyRelatedField()
    is_lecturer = serializers.BooleanField(default=False)
    is_project_admin = serializers.BooleanField(default=False)
    is_customer = serializers.BooleanField(default=False)
    is_verified = serializers.BooleanField(default=False) # Флаг для проверки модератором документов
    grade = serializers.CharField(max_length=300, null=True, blank=True, default='')
    description = serializers.CharField(null=True, blank=True)
    domain = serializers.PrimaryKeyRelatedField(queryset=Domain.objects.all())
    latitude = serializers.DecimalField(
        max_digits=10, decimal_places=7, null=True, blank=True,default='')
    longtitude = serializers.DecimalField(
        max_digits=10, decimal_places=7, null=True, blank=True, default='')

    class Meta:
        fields = [
            'first_name',
            'last_name',
            'middle_name',
            'birth_date',
            'city',
            'address',
            'rating',
            'photo',
            'user',
            'is_lecturer',
            'is_project_admin',
            'is_customer',
            'is_verified',
            'grade',
            'description',
            'domain',
            'latitude',
        ]

