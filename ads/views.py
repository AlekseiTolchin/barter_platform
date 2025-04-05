from django.views.generic.edit import CreateView
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Ad
from .forms import AdForm

class AdCreateView(LoginRequiredMixin, CreateView):
    model = Ad  # Модель, для которой создаётся объект
    form_class = AdForm  # Форма, используемая для ввода данных
    template_name = 'ads/ad_list.html'  # HTML-шаблон
    success_url = reverse_lazy('ad_list')  # Перенаправление при успешном создании

    def form_valid(self, form):
        # Привязка объявления к текущему пользователю
        form.instance.user = self.request.user  # Указываем текущего пользователя как автора
        return super().form_valid(form)  # Сохраняем объект в базе данных


class AdListView(ListView):
    template_name = 'ads/ad_list.html'
    context_object_name = 'ads'

    def get_queryset(self):
        ads = Ad.objects.all()
        return ads


class AdDetailView(DetailView):
    model = Ad
    template_name = 'ads/ad_detail.html'
    context_object_name = 'ad'



