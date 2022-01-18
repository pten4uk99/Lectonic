from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from workroomsapp.serializers.person import PersonCreateSerializer


class PersonCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = PersonCreateSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        print(serializer.validated_data)
        return Response(201)
