from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions
from rest_framework.views import APIView

from workroomsapp.customer.customer_serializers import CustomerCreateSerializer
from workroomsapp.customer import customer_responses
from workroomsapp.customer.docs import customer_docs


class CustomerAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(**customer_docs.CustomerCreateDoc)
    def post(self, request):
        serializer = CustomerCreateSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return customer_responses.customer_created()
