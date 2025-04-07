from django.urls import path

from .api_views import RegisterAPIView

urlpatterns = [
    path('registration/', RegisterAPIView.as_view(), name='registration'),
]
