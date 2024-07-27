from rest_framework import serializers

from .. import models


class AuthorAdvertisementSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AuthorAdvertisement
        fields = '__all__'


class AdvertisementSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Advertisement
        fields = '__all__'

    def update(self, instance, validated_data):
        validated_data.pop('ad_author', None)
        return super().update(instance, validated_data)
