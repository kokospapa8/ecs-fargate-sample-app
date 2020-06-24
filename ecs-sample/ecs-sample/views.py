from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

class HealthCheckView(GenericAPIView):
    _ignore_model_permissions = True

    def get(self, request, *args, **kwargs):
        return Response({}, status=status.HTTP_200_OK)