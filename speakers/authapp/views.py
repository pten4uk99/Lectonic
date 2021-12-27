from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (
    UserProfileCreateSerializer,
    UserProfileLoginSerializer
)
from .models import UserProfile


class UserProfileCreationView(APIView):  # Возможно в будущем переделается на дженерик
    def post(self, request):
        serializer = UserProfileCreateSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(status=201)


class UserProfileLoginView(APIView):
    def post(self, request):
        serializer = UserProfileLoginSerializer(data=request.data)
        return Response(status=201)
