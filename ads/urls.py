from django.urls import path
from .views import AdCreateView, AdListView, AdDetailView, AdUpdateView, AdDeleteView, ExchangeProposalCreateView, ExchangeProposalUpdateView

app_name = 'ads'

urlpatterns = [
    path('', AdListView.as_view(), name='ad_list' ),
    path('create/', AdCreateView.as_view(), name='ad_form'),
    path('ads/<int:pk>/', AdDetailView.as_view(), name='ad_detail'),
    path('<int:pk>/edit/', AdUpdateView.as_view(), name='update_ad'),
    path('<int:pk>/delete/', AdDeleteView.as_view(), name='delete_ad'),
    path('proposals/create/', ExchangeProposalCreateView.as_view(), name='proposal_create'),
    path('proposal/<int:pk>/update/', ExchangeProposalUpdateView.as_view(), name='proposal_update'),
]
