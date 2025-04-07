from django.urls import path
from .api_views import CreateAdView, UpdateAdView, DeleteAdView


urlpatterns = [
    path('ads/', CreateAdView.as_view(), name='create_ad'),
    path('ads/<int:pk>/', UpdateAdView.as_view(), name='update_ad'),
    path('ads/<int:pk>/', DeleteAdView.as_view(), name='delete_ad'),
]
