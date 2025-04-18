from django.urls import path

from .api_views import (
    AdUpdateDeleteView,
    AdListCreateView,
    ExchangeProposalListCreate,
    ExchangeProposalDeleteUpdate,
)


urlpatterns = [
    path('ads/', AdListCreateView.as_view(), name='ads_list_create'),
    path('ads/<int:pk>/', AdUpdateDeleteView.as_view(), name='ad_update_delete'),
    path('proposals/', ExchangeProposalListCreate.as_view(), name='proposals_list_create'),
    path('proposals/<int:pk>/', ExchangeProposalDeleteUpdate.as_view(), name='proposal_delete_update')
]
