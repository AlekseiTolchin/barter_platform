from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Ad
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


class UpdateAdView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=['Объявления'],
        summary='Редактировать объявление',
        description='Редактирование объявления',
        request=AdSerializer,
        responses={
            201: OpenApiResponse(response=AdSerializer, description='Объявление успешно отредактировано'),
            400: OpenApiResponse(description='Неверные данные')
        }
    )

    def patch(self, request, pk):
        try:
            ad = Ad.objects.get(pk=pk)
            if ad.user != request.user:
                return Response(
                    {'detail': 'Вы не можете редактировать чужое объявление.'},
                    status=status.HTTP_403_FORBIDDEN
                )
            serializer = AdSerializer(ad, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Ad.DoesNotExist:
            return Response(
                {'detail': 'Объявление с указанным ID не найдено.'},
                status=status.HTTP_404_NOT_FOUND
            )


class DeleteAdView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=['Объявления'],
        summary='Удалить объявление',
        description='Удаление объявления',
        request=AdSerializer,
        responses={
            201: OpenApiResponse(response=AdSerializer, description='Объявление успешно удалено'),
            400: OpenApiResponse(description='Неверные данные')
        }
    )

    def delete(self, request, pk):
        try:
            ad = Ad.objects.get(pk=pk)

            if ad.user != request.user:
                return Response(
                    {'detail': 'Вы не можете удалить чужое объявление.'},
                    status=status.HTTP_403_FORBIDDEN
                )

            ad.delete()
            return Response(
                {'detail': "Объявление успешно удалено."},
                status=status.HTTP_204_NO_CONTENT
            )

        except Ad.DoesNotExist:
            return Response(
                {'detail': "Объявление с указанным ID не найдено."},
                status=status.HTTP_404_NOT_FOUND
        )


class AdListCreateView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    @extend_schema(
        tags=['Объявления'],
        summary='Получить все объявления',
        description='Получить все объявления',
        request=None,
        responses={
            200: OpenApiResponse(response=AdSerializer(many=True), description='Объявления успешно получены'),
            400: OpenApiResponse(description='Неверные данные')
        }
    )
    def get(self, request):
        paginator = PageNumberPagination()
        paginator.page_size = 5
        ads = Ad.objects.all()
        page = paginator.paginate_queryset(ads, request)
        serializer = AdSerializer(page, many=True)
        return Response(serializer.data)

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
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
