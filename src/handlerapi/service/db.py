from django.conf import settings
from rest_framework.request import Request

from ..api.serializers import AdvertisementSerializer
from ..models import AuthorAdvertisement, Advertisement
from typing import List, Dict, Union, Any


def get_all_ads() -> List[Dict[str, Any]]:
    all_ad = Advertisement.objects.all()
    serializer = AdvertisementSerializer(all_ad, many=True)
    return serializer.data


def get_or_create_author(ad_author: str) -> int:
    author, created = AuthorAdvertisement.objects.get_or_create(author_title=ad_author)
    return author.id


def get_data_for_query_params(request: Request) -> Union[Dict[str, Any], Dict[str, str]]:
    params = request.query_params.dict()

    allowed_filters = settings.ALLOWED_FILTERS
    filtered_params = {key: value for key, value in params.items() if key in allowed_filters}

    if filtered_params:
        try:
            params_to_convert = settings.PARAMS_TO_CONVENT
            for param in params_to_convert:
                if param in filtered_params:
                    filtered_params[param] = int(filtered_params[param])
        except ValueError:
            return {"error": "ad_views, ad_id, ad_position и ad_author должны быть целыми числами."}

    advertisements = Advertisement.objects.filter(**filtered_params)

    if not advertisements.exists():
        return {"error": "Объявления не найдены с такими параметрами."}

    serializer = AdvertisementSerializer(advertisements, many=True)
    return serializer.data


def get_ad_for_editing(**kwargs: Any) -> Union[Advertisement, Dict[str, str]]:
    ad_id = kwargs.get('id')
    try:
        advertisement = Advertisement.objects.get(id=ad_id)
        return advertisement
    except Advertisement.DoesNotExist:
        return {"error": "Объявление не найдено с таким id."}
