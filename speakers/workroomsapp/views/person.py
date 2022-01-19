from django.db import transaction
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from workroomsapp.models import City, Person
from workroomsapp.serializers.person import *


class PersonAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
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

        return Response(
            data={
                "person": {**serializer.validated_data},
                "status": "created"
            }, status=201
        )

    def get(self, request):
        person = Person.objects.filter(user=request.user).first()

        if not person:
            raise serializers.ValidationError({"detail": "Данного профиля не существует"})

        serializer = PersonGetPatchSerializer(person)
        return Response(serializer.data)

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
            raise serializers.ValidationError({"detail": "Данного профиля не существует"})

        person_serializer = PersonGetPatchSerializer(person, data=request.data, partial=True)
        person_serializer.is_valid(raise_exception=True)
        person_serializer.save()

        return Response(data={"patched": {**person_serializer.data}})
