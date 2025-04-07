from django.urls import path
from .api_views import UpdateAdView, DeleteAdView, AdListCreateView


urlpatterns = [
    path('ads/<int:pk>/', UpdateAdView.as_view(), name='update_ad'),
    path('ads/<int:pk>/', DeleteAdView.as_view(), name='delete_ad'),
    path('ads/', AdListCreateView.as_view(), name='ads_list' )
]
