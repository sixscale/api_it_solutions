from . import exceptions
from ..api.serializers import AdvertisementSerializer
from ..models import AuthorAdvertisement, Advertisement
from rest_framework.response import Response
from rest_framework import status


def get_or_create_author(ad_author: str) -> int:
    author, created = AuthorAdvertisement.objects.get_or_create(author_title=ad_author)
    if created:
        return author.id
    return author.id


def get_data_for_query_params(request):
    params = request.query_params.dict()

    allowed_filters = ['ad_title', 'ad_id', 'ad_author', 'ad_views', 'ad_position']
    filtered_params = {key: value for key, value in params.items() if key in allowed_filters}

    if filtered_params:
        try:
            filtered_params['ad_views'] = int(filtered_params['ad_views'])
            filtered_params['ad_id'] = int(filtered_params['ad_id'])
            filtered_params['ad_position'] = int(filtered_params['ad_position'])
            filtered_params['ad_author'] = int(filtered_params['ad_author'])
        except ValueError:
            return {"error": "ad_views, ad_id, ad_position и ad_author должны быть целыми числами."}
    advertisements = Advertisement.objects.filter(**filtered_params)

    serializer = AdvertisementSerializer(advertisements, many=True)

    return serializer.data
