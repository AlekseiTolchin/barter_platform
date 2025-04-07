from django.urls import path
from .api_views import CreateAdView


urlpatterns = [
    path('ads/', CreateAdView.as_view(), name='create_ad'),
]
