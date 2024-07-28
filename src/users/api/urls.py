from django.urls import path, include

from .views import UserRegistrationAPIView

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('create', UserRegistrationAPIView.as_view()),
]