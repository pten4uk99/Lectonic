from rest_framework import serializers


class PersonCreateSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    middle_name = serializers.CharField(max_length=100, required=False)
    birth_date = serializers.DateField()
    city = serializers.CharField(max_length=100)  # Пока что ввод города вручную, позже переделать на PrimaryKeyRelatedField()
    # address = serializers.CharField(max_length=200, required=False)
    rating = serializers.IntegerField(default=0, required=False)
    # photo = serializers.CharField(max_length=200, required=False)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    # grade = serializers.CharField(max_length=300, default='', required=False)
    description = serializers.CharField(required=False)
    # domain = serializers.PrimaryKeyRelatedField(queryset=Domain.objects.all(), required=False)
    latitude = serializers.DecimalField(
        max_digits=10,
        decimal_places=7,
        required=False
    )
    longitude = serializers.DecimalField(
        max_digits=10,
        decimal_places=7,
        required=False
    )

    class Meta:
        fields = [
            'first_name',
            'last_name',
            'middle_name',
            'birth_date',
            'city',
            # 'address',
            'rating',
            # 'photo',
            'user',
            # 'grade',
            'description',
            # 'domain',
            'latitude',
            'longitude',
        ]

