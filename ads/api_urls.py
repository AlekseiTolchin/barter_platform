from django.urls import path
from .api_views import CreateAdView, UpdateAdView


urlpatterns = [
    path('ads/', CreateAdView.as_view(), name='create_ad'),
    path('ads/<int:pk>/', UpdateAdView.as_view(), name='update_ad'),
]
