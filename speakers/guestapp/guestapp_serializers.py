from rest_framework import serializers
from workroomsapp.models import City, Person

from workroomsapp.models import Domain, Lecture, User


class GuestCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = [
            'name',
            'country',
        ]


class GuestDomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domain
        fields = [
            'name',
        ]


# class GuestLectureHallSerializer(serializers.ModelSerializer):
#     city = GuestCitySerializer()
#
#     class Meta:
#         model = LectureHall
#         fields = [
#             'city',
#             'address',
#             'latitude',
#             'longitude',
#         ]


class GuestPersonSerializer(serializers.ModelSerializer):
    domain = GuestDomainSerializer()

    class Meta:
        model = Person
        fields = (
            'first_name',
            'last_name',
            'rating',
            'grade',
            'description',
            'domain',
        )


class GuestUserSerializer(serializers.ModelSerializer):
    person = GuestPersonSerializer()

    class Meta:
        model = User
        fields = (
            'person',
        )


class GuestLectureSerializer(serializers.ModelSerializer):
    lecture_id = serializers.IntegerField(source='id')
    lecturers = GuestUserSerializer(many=True, required=False)
    # hall = GuestLectureHallSerializer(required=False)
    domain = GuestDomainSerializer(many=True, required=False)

    class Meta:
        model = Lecture
        fields = [
            'lecture_id',
            'name',
            'date',
            'duration',
            'description',
            'lecturer_name',
            'lecturers',
            'hall',
            'domain',
        ]
