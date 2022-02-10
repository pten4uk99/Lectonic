from django.db import transaction
from rest_framework import permissions
from rest_framework.views import APIView

from workroomsapp.models import City, Person
from workroomsapp.serializers.person_serializers import *
from workroomsapp.utils.responses import person_responses


class PersonAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        if Person.objects.filter(user=request.user).first():
            return person_responses.profile_is_existing()

        serializer = PersonSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        serializer.validated_data.pop('user')
        city = serializer.validated_data.pop('city')

        return person_responses.created(data={**serializer.validated_data, 'city': city.name})

    def get(self, request):
        person = Person.objects.filter(user=request.user).first()

        if not person:
            return person_responses.profile_does_not_exist()

        serializer = PersonSerializer(person)

        return person_responses.success({
            **serializer.data,
            'city': City.objects.get(id=serializer.data['city']).name
        })

    def patch(self, request):
        person = Person.objects.filter(user=request.user).first()

        if not person:
            return person_responses.profile_does_not_exist()

        serializer = PersonSerializer(person, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        city = serializer.validated_data.pop('city')

        return person_responses.created(data={**serializer.validated_data, 'city': city.name})


class CityAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = CitySerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)

        cities = City.objects.filter(name__icontains=serializer.data['name'])

        if not cities:
            return person_responses.empty()

        cities_ser = CitySerializer(cities, many=True)

        return person_responses.success(cities_ser.data)
