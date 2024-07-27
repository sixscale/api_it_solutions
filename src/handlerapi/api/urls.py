from django.urls import path

from .views import AdvertisementListApiView, CreateAdvertisementApiView, UpdateAdvertisementApiView, \
    DeleteAdvertisementApiView

urlpatterns = [
    path('advertisement', AdvertisementListApiView.as_view()),
    path('create', CreateAdvertisementApiView.as_view()),
    path('update/<int:id>', UpdateAdvertisementApiView.as_view()),
    path('delete/<int:id>', DeleteAdvertisementApiView.as_view()),
]
