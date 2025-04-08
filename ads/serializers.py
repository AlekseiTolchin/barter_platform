from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Ad, ExchangeProposal


class AdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = ['id', 'user', 'title', 'description', 'image_url', 'category', 'condition', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']


class ExchangeProposalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeProposal
        fields = ['id', 'ad_sender', 'ad_receiver', 'comment', 'status', 'created_at']
        read_only_fields = ['created_at']


class SpecialExchangeProposalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeProposal
        fields = ['status']
