from rest_framework import status
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.response import Response

from .jobs import rq_test


class HealthCheckView(GenericAPIView):
    _ignore_model_permissions = True

    def get(self, request, *args, **kwargs):
        return Response({}, status=status.HTTP_200_OK)

class RqTestView(GenericAPIView):
    _ignore_model_permissions = True


    def get(self, request, *args, **kwargs):
        rq_test.delay()
        return Response({}, status=status.HTTP_201_CREATED)
