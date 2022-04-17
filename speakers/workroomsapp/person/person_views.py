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

        serializer.validated_data.pop('user')
        city = serializer.validated_data.pop('city')

        if 'photo' in serializer.validated_data:
            serializer.validated_data.pop('photo')

        return person_responses.created([{
            **serializer.validated_data,
            'city': city.name,
            'user_id': request.user.pk
        }])

    @swagger_auto_schema(**person_docs.PersonGetDoc)
    def get(self, request):
        person = Person.objects.filter(user=request.user).first()

        if not person:
            return person_responses.profile_does_not_exist()

        serializer = PersonSerializer(person)

        photo_serializer = PersonPhotoGetSerializer(
            person,
            context={'request': request}
        )
        if 'photo' in serializer.data:
            serializer.data.pop('photo')

        return person_responses.success([{
            **serializer.data,
            **photo_serializer.data
        }])

    @swagger_auto_schema(**person_docs.PersonPatchDoc)
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

        if 'photo' in serializer.validated_data:
            serializer.validated_data.pop('photo')

        photo_serializer = PersonPhotoGetSerializer(person, context={'request': request})
        return person_responses.patched([{
            **serializer.validated_data,
            **photo_serializer.data
        }])



class DocumentImageAPIVIew(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(**person_docs.DocumentImageCreateDoc)
    def post(self, request):
        serializer = DocumentImageCreateSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return person_responses.photo_created()

    @swagger_auto_schema(**person_docs.DocumentImageGetDoc)
    def get(self, request):
        document_image = DocumentImage.objects.filter(person=request.user.person).first()

        if not document_image:
            return person_responses.document_image_does_not_exist()

        serializer = DocumentImageGetSerializer(
            document_image,
            context={'request': request})
        return person_responses.success([serializer.data])


class CityGetAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(**person_docs.CityGetDoc)
    def get(self, request):
        serializer = CitySerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)

        cities = City.objects.filter(name__icontains=serializer.data['name'])

        if not cities:
            return person_responses.empty()

        cities_ser = CitySerializer(cities, many=True)

        return person_responses.success(cities_ser.data)


class DomainGetAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(**person_docs.DomainGetDoc)
    def get(self, request):
        serializer = DomainGetSerializer(Domain.objects.all(), many=True)
        return person_responses.success(serializer.data)
