from django.db import transaction
from rest_framework import permissions
from rest_framework.views import APIView

from workroomsapp.models import City, Person
from workroomsapp.serializers.person_serializers import *
from workroomsapp.utils.responses.person_responses import created, success_get_profile, profile_does_not_exist, \
    profile_is_existing


class PersonAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        if Person.objects.filter(user=request.user).first():
            return profile_is_existing()

        serializer = PersonCreateSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        city = serializer.validated_data.pop('city')

        with transaction.atomic():
            Person.objects.create(
                **serializer.validated_data,
                city=City.objects.create(name=city)
            )

        serializer.validated_data.pop('user')

        return created(data=serializer.validated_data)

    def get(self, request):
        person = Person.objects.filter(user=request.user).first()

        if not person:
            return profile_does_not_exist()

        serializer = PersonGetPatchSerializer(person)
        return success_get_profile(serializer.data)

    def patch(self, request):
        person = Person.objects.filter(user=request.user).first()

        if request.data.get('city'):
            city = City.objects.filter(person=person).first()

            if city:
                city_serializer = PersonCityEditSerializer(
                    city,
                    data={'name': request.data['city']},
                    partial=True
                )
                city_serializer.is_valid(raise_exception=True)
                city_serializer.save()

        if not person:
            return profile_does_not_exist()

        person_serializer = PersonGetPatchSerializer(person, data=request.data, partial=True)
        person_serializer.is_valid(raise_exception=True)
        person_serializer.save()

        return created(person_serializer.data)
