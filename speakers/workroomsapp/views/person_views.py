from django.db import transaction
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions
from rest_framework.parsers import MultiPartParser, FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView

from authapp.models import User
from workroomsapp.docs.docs import person_docs
from workroomsapp.models import City, Person
from workroomsapp.serializers.person_serializers import *
from workroomsapp.utils.responses import person_responses


class PersonAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(**person_docs.PersonCreationView)
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

    @swagger_auto_schema(**person_docs.PersonGetView)
    def get(self, request):
        person = Person.objects.filter(user=request.user).first()

        if not person:
            return person_responses.profile_does_not_exist()

        serializer = PersonSerializer(person)

        return person_responses.success({
            **serializer.data,
            'city': City.objects.get(pk=serializer.data['city']).name
        })

    @swagger_auto_schema(**person_docs.PersonPatchView)
    def patch(self, request):
        person = Person.objects.filter(user=request.user).first()

        if not person:
            return person_responses.profile_does_not_exist()

        if not request.data:
            return person_responses.no_data_in_request()

        serializer = PersonSerializer(person, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        if 'city' in serializer.validated_data:
            serializer.validated_data['city'] = serializer.validated_data['city'].name

        return person_responses.patched(data={**serializer.validated_data})


class ImageAPIView(APIView):
    def post(self, request):
        print(request.data['photo'].file)
        # serializer = ImageSerializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # serializer.save()
        return Response(200)


class DocumentImageCreateAPIVIew(APIView):
    parser_classes = [MultiPartParser, FileUploadParser]

    def post(self, request):
        print(request.data)
        serializer = DocumentImageSerializer(
            data=request.data,
            context={'request': {'person': {'user': User.objects.first()}}}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(200)


class CityAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(**person_docs.CityGetView)
    def get(self, request):
        serializer = CitySerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)

        cities = City.objects.filter(name__icontains=serializer.data['name'])

        if not cities:
            return person_responses.empty()

        cities_ser = CitySerializer(cities, many=True)

        return person_responses.success(cities_ser.data)
