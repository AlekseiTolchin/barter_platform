from django.contrib import admin

from .models import Ad, ExchangeProposal


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at']


@admin.register(ExchangeProposal)
class ExchangeProposal(admin.ModelAdmin):
    pass
