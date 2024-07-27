from django.conf import settings

from . import exceptions
from ..api.serializers import AdvertisementSerializer
from ..models import AuthorAdvertisement, Advertisement
from rest_framework.response import Response
from rest_framework import status


def get_all_ads():
    all_ad = Advertisement.objects.all()
    serializer = AdvertisementSerializer(all_ad, many=True)
    return serializer.data


def get_or_create_author(ad_author: str) -> int:
    author, created = AuthorAdvertisement.objects.get_or_create(author_title=ad_author)
    if created:
        return author.id
    return author.id


def get_data_for_query_params(request):
    params = request.query_params.dict()

    allowed_filters = settings.ALLOWED_FILTERS
    filtered_params = {key: value for key, value in params.items() if key in allowed_filters}

    if filtered_params:
        try:
            params_to_convert = settings.PARAMS_TO_CONVENT
            for key in params_to_convert:
                if key in filtered_params:
                    filtered_params[key] = int(filtered_params[key])
        except ValueError:
            return {"error": "ad_views, ad_id, ad_position и ad_author должны быть целыми числами."}

    advertisements = Advertisement.objects.filter(**filtered_params)

    if not advertisements.exists():
        return {"error": "Объявления не найдены с такими параметрами."}

    serializer = AdvertisementSerializer(advertisements, many=True)

    return serializer.data
