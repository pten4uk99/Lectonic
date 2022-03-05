from rest_framework.response import Response
from rest_framework.views import APIView

from authapp.models import User
from workroomsapp.serializers.lecturer_serializers import LecturerCreateSerializer


class LecturerCreateAPIView(APIView):
    def post(self, request):
        print(request.data)
        serializer = LecturerCreateSerializer(
            data=request.data['data'],
            context={
                'request': {
                    'user': User.objects.first()
                }
            }
        )
        print(request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        print(serializer.data)
        return Response(200)