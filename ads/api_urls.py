from django.urls import path

from .api_views import (
    UpdateAdView,
    DeleteAdView,
    AdListCreateView,
    ExchangeProposalListCreate,
    ExchangeProposalDeleteUpdate,
)


urlpatterns = [
    path('ads/', AdListCreateView.as_view(), name='ads_list_create'),
    path('ads/<int:pk>/', UpdateAdView.as_view(), name='update_ad'),
    path('ads/<int:pk>/', DeleteAdView.as_view(), name='delete_ad'),
    path('proposals/', ExchangeProposalListCreate.as_view(), name='proposals_list_create'),
    path('proposals/<int:pk>/', ExchangeProposalDeleteUpdate.as_view(), name='proposal_delete_update')
]
