from django.contrib.auth import get_user_model
from django.utils import timezone
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import AdSerializer, UserSerializer


User = get_user_model()


class CreateAdView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=['Объявления'],
        summary='Создать новое объявление',
        description='Создание нового объявления',
        request=AdSerializer,
        responses={
            201: OpenApiResponse(response=AdSerializer, description='Объявление успешно создано'),
            400: OpenApiResponse(description='Неверные данные')
        }
    )

    def post(self, request):
        serializer = AdSerializer(data=request.data)

        if serializer.is_valid():
            ad = serializer.save(user=request.user)
            ad_payload = {
                'id': ad.id,
                'user': UserSerializer(ad.user).data,
                'title': ad.title,
                'image_url': ad.image_url,
                'category': ad.category,
                'message': 'Объявление успешно создано'
            }
            return Response(ad_payload, status=201)
        return Response(serializer.errors, status=400)
