from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework import permissions

from .serializers import AdvertisementSerializer
from ..models import Advertisement
from ..service.db import get_or_create_author, get_data_for_query_params, get_all_ads, get_ad_for_editing


class AdvertisementListApiView(generics.ListAPIView):
    # permission_classes = [permissions.IsAuthenticated]
    def get(self, request, *args, **kwargs):
        if request.query_params:
            params_data = get_data_for_query_params(request)
            if isinstance(params_data, dict) and 'error' in params_data:
                return Response(params_data, status=status.HTTP_400_BAD_REQUEST)
            return Response(params_data, status=status.HTTP_200_OK)

        all_ads = get_all_ads()
        return Response(all_ads, status=status.HTTP_200_OK)


class CreateAdvertisementApiView(APIView):
    # permission_classes = [permissions.IsAuthenticated]
    def post(self, request, *args, **kwargs):
        data = request.data
        data['ad_author'] = get_or_create_author(data['ad_author'])
        serializer = AdvertisementSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateAdvertisementApiView(APIView):
    # permission_classes = [permissions.IsAuthenticated]
    def put(self, request, *args, **kwargs):
        advertisement = get_ad_for_editing(**kwargs)
        if isinstance(advertisement, dict) and 'error' in advertisement:
            return Response(advertisement, status=status.HTTP_400_BAD_REQUEST)

        data = request.data

        serializer = AdvertisementSerializer(advertisement, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)

        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


class DeleteAdvertisementApiView(APIView):
    # permission_classes = [permissions.IsAuthenticated]
    def delete(self, request, *args, **kwargs):
        advertisement = get_ad_for_editing(**kwargs)
        if isinstance(advertisement, dict) and 'error' in advertisement:
            return Response(advertisement, status=status.HTTP_400_BAD_REQUEST)
        advertisement.delete()
        return Response(status=status.HTTP_200_OK)
