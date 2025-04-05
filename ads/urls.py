from django.urls import path
from .views import AdCreateView, AdListView, AdDetailView

app_name = 'ads'

urlpatterns = [
    path('create', AdCreateView.as_view(), name='ad_form'),  # Создание объявления
    path('', AdListView.as_view(), name='ad_list' ),
    path('ads/<int:pk>/', AdDetailView.as_view(), name='ad_detail'),
    # path('<int:pk>/edit/', AdUpdateView.as_view(), name='update_ad'),  # Редактирование объявления
    # path('<int:pk>/', AdDetailView.as_view(), name='ad_detail'),  # Детали объявления
    # path('', AdListView.as_view(), name='ad_list'),  # Список объявлений
]