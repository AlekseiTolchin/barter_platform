from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Ad, ExchangeProposal
from .serializers import AdSerializer, UserSerializer, ExchangeProposalSerializer


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
            200: OpenApiResponse(
                response=AdSerializer(many=True),
                description='Объявления успешно получены'
            ),
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


class ExchangeProposalListCreate(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    @extend_schema(
        tags=['Предложения обмена'],
        summary='Получить все предложения обмена',
        description='Получить все предложения обмена',
        request=None,
        responses={
            200: OpenApiResponse(
                response=ExchangeProposalSerializer(many=True),
                description='Предложения успешно получены',
            ),
        }
    )
    def get(self, request):
        paginator = PageNumberPagination()
        paginator.page_size = 5
        exchange_proposals = ExchangeProposal.objects.all()
        page = paginator.paginate_queryset(exchange_proposals, request)
        serializer = ExchangeProposalSerializer(page, many=True)
        return Response(serializer.data)

    @extend_schema(
        tags=['Предложения обмена'],
        summary='Создать новое предложение обмена',
        description='Создание нового предложения обмена',
        request=ExchangeProposalSerializer,
        responses={
            201: OpenApiResponse(response=ExchangeProposalSerializer, description='Предложение успешно создано'),
            400: OpenApiResponse(description='Неверные данные')
        }
    )
    def post(self, request):
        serializer = ExchangeProposalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExchangeProposalDeleteUpdate(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=['Предложения обмена'],
        summary='Удалить предложение обмена',
        description='Удаление предложения обмена',
        request=ExchangeProposalSerializer,
        responses={
            204: OpenApiResponse(response=ExchangeProposalSerializer, description='Предложение успешно удалено'),
        }
    )
    def delete(self, request, pk):
        try:
            exchange_proposal = ExchangeProposal.objects.get(pk=pk)
            if request.user != exchange_proposal.ad_sender.user:
                return Response(
                    {'detail': 'Вы не можете удалить чужое предложение.'},
                    status=status.HTTP_403_FORBIDDEN
                )

            exchange_proposal.delete()
            return Response(
                    status=status.HTTP_204_NO_CONTENT
                )

        except ExchangeProposal.DoesNotExist:
            return Response(
                {'detail': 'Объявление с указанным ID не найдено.'},
                status=status.HTTP_404_NOT_FOUND
            )

    @extend_schema(
        tags=['Предложения обмена'],
        summary='Обновить статус предложение обмена',
        description='Обновление статуса предложения обмена',
        request=ExchangeProposalSerializer,
        responses={
            200: OpenApiResponse(
                response=ExchangeProposalSerializer,
                description='Статус предложения успешно обновлен'
            ),
        }
    )
    def patch(self, request, pk):
        allowed_field = 'status'
        try:
            exchange_proposal = ExchangeProposal.objects.get(pk=pk)
            if request.user != exchange_proposal.ad_receiver.user:
                return Response(
                    {'detail': 'Вы не можете обновить статус предложения.'},
                    status=status.HTTP_403_FORBIDDEN
                )

            if len(request.data) != 1 or allowed_field not in request.data:
                return Response(
                    {'detail': f'Вы можете обновить только поле: {allowed_field}.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            serializer = ExchangeProposalSerializer(exchange_proposal, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except ExchangeProposal.DoesNotExist:
            return Response(
                {'detail': 'Предложение с указанным ID не найдено.'},
                status=status.HTTP_404_NOT_FOUND
            )
