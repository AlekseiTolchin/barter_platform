from django.db.models import Q
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy

from .models import Ad
from .forms import AdForm

class AdCreateView(LoginRequiredMixin, CreateView):
    model = Ad
    form_class = AdForm
    template_name = 'ads/ad_form.html'
    success_url = reverse_lazy('ads:ad_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class AdListView(ListView):
    model = Ad
    template_name = 'ads/ad_list.html'
    context_object_name = 'ads'

    def get_queryset(self):
        queryset = Ad.objects.all()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            )

        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category=category)


        condition = self.request.GET.get('condition')
        if condition:
            queryset = queryset.filter(condition=condition)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        categories = Ad.objects.values_list('category', flat=True).distinct()
        context['categories'] = categories

        return context


class AdDetailView(DetailView):
    model = Ad
    template_name = 'ads/ad_detail.html'
    context_object_name = 'ad'


class AdUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Ad
    fields = ['title', 'description', 'image_url', 'category', 'condition']
    template_name = 'ads/ad_form_update.html'
    success_url = reverse_lazy('ads:ad_list')

    def test_func(self):
        ad = self.get_object()
        return self.request.user == ad.user


class AdDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Ad
    template_name = 'ads/ad_confirm_delete.html'
    success_url = reverse_lazy('ads:ad_list')

    def test_func(self):
        ad = self.get_object()
        return self.request.user == ad.user
