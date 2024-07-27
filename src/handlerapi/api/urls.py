from django.urls import path

from .views import AdvertisementListApiView, CreateAdvertisementApiView

urlpatterns = [
    path('advertisement', AdvertisementListApiView.as_view()),
    path('create', CreateAdvertisementApiView.as_view()),
]