from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions
from rest_framework.views import APIView

from workroomsapp.person.docs import person_docs
from workroomsapp.person.person_serializers import *
from workroomsapp.person import person_responses


class PersonAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(**person_docs.PersonCreationDoc)
    def post(self, request):
        if Person.objects.filter(user=request.user).first():
            return person_responses.profile_is_existing()

        serializer = PersonSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return person_responses.created([{
            **serializer.validated_data,
            'user_id': request.user.pk
        }])

    @swagger_auto_schema(**person_docs.PersonGetDoc)
    def get(self, request):
        person = Person.objects.filter(user=request.user).first()

        if not person:
            return person_responses.profile_does_not_exist()

        serializer = PersonGetSerializer(person, context={'request': request})
        return person_responses.success([serializer.data])

    @swagger_auto_schema(**person_docs.PersonPatchDoc)
    def patch(self, request):
        person = Person.objects.filter(user=request.user).first()

        if not person:
            return person_responses.profile_does_not_exist()

        if not request.data:
            return person_responses.no_data_in_request()

        serializer = PersonPatchSerializer(person, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return person_responses.patched([serializer.data])


class CityGetAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    def filter(name):
        return City.objects.filter(name__icontains=name)

    @swagger_auto_schema(**person_docs.CityGetDoc)
    def get(self, request):
        name = request.GET.get('name')
        cities = self.filter(name)
        serializer = CitySerializer(cities, many=True)
        return person_responses.success(serializer.data)


class DomainGetAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(**person_docs.DomainGetDoc)
    def get(self, request):
        serializer = DomainGetSerializer(Domain.objects.all(), many=True)
        return person_responses.success(serializer.data)
