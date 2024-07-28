from django.conf import settings
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.request import Request
from typing import Any, Dict

from rest_framework.permissions import IsAuthenticated

from .serializers import AdvertisementSerializer
from ..service.db import get_or_create_author, get_data_for_query_params, get_all_ads, get_ad_for_editing
from users.permissions import IsOwner


class AdvertisementListApiView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = AdvertisementSerializer

    @swagger_auto_schema(operation_description="Получение объявлений.",
                         manual_parameters=settings.AUTHORIZATION + settings.MANUAL_PARAMETERS,
                         security=[{'JWT': []}],)
    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        if request.query_params:
            params_data = get_data_for_query_params(request)
            if isinstance(params_data, dict) and 'error' in params_data:
                return Response(params_data, status=status.HTTP_400_BAD_REQUEST)
            return Response(params_data, status=status.HTTP_200_OK)

        all_ads = get_all_ads()
        return Response(all_ads, status=status.HTTP_200_OK)


class CreateAdvertisementApiView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]

    @swagger_auto_schema(operation_description="Создание нового объявления.",
                         manual_parameters=settings.AUTHORIZATION,
                         security=[{'JWT': []}],
                         request_body=openapi.Schema(type=openapi.TYPE_OBJECT,
                                                     properties=settings.PROPERTIES,
                                                     required=settings.ALLOWED_FILTERS,),)
    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        data = request.data
        data['ad_author'] = get_or_create_author(data['ad_author'])
        serializer = AdvertisementSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateAdvertisementApiView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]

    @swagger_auto_schema(operation_description="Обновление существующего объявления.",
                         manual_parameters=settings.AUTHORIZATION,
                         security=[{'JWT': []}], )
    def put(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        advertisement = get_ad_for_editing(**kwargs)
        if isinstance(advertisement, dict) and 'error' in advertisement:
            return Response(advertisement, status=status.HTTP_400_BAD_REQUEST)

        serializer = AdvertisementSerializer(advertisement, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)

        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


class DeleteAdvertisementApiView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]

    @swagger_auto_schema(operation_description="Удаление существующего объявления.",
                         manual_parameters=settings.AUTHORIZATION,
                         security=[{'JWT': []}], )
    def delete(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        advertisement = get_ad_for_editing(**kwargs)
        if isinstance(advertisement, dict) and 'error' in advertisement:
            return Response(advertisement, status=status.HTTP_400_BAD_REQUEST)
        advertisement.delete()
        return Response(status=status.HTTP_200_OK)
