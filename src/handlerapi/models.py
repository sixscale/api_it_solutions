from django.db import models


class AuthorAdvertisement(models.Model):
    author_title = models.CharField(max_length=255)


class Advertisement(models.Model):
    ad_title = models.CharField(max_length=255)
    ad_id = models.IntegerField()
    ad_author = models.ForeignKey(AuthorAdvertisement, on_delete=models.CASCADE, related_name='advertisements')
    ad_views = models.IntegerField()
    ad_position = models.IntegerField()

