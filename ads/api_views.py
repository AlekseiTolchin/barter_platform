from django.contrib.auth import get_user_model

from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Ad, ExchangeProposal
from .serializers import (
    AdSerializer,
    ExchangeProposalSerializer,
    SpecialExchangeProposalSerializer,
)


User = get_user_model()


class AdListCreateView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    @extend_schema(
        tags=['Объявления'],
        summary='Получить все объявления',
        description='Получение всех объявлений',
        responses={
            200: OpenApiResponse(
                response=AdSerializer(many=True),
                description='Объявления успешно получены'
            ),
        }
    )
    def get(self, request):
        ads = Ad.objects.all().order_by('id')
        if not ads.exists():
            raise NotFound('Объявления не найдены.')
        serializer = AdSerializer(ads, many=True)
        return Response(serializer.data)

    @extend_schema(
        tags=['Объявления'],
        summary='Создать новое объявление',
        description='Только авторизованный пользователь может создать объявление.',
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


class AdUpdateDeleteView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    @staticmethod
    def get_object(pk, user):
        try:
            ad = Ad.objects.get(pk=pk)
            if ad.user != user:
                raise PermissionError('Вы не можете выполнить это действие с чужим объявлением.')
            return ad
        except Ad.DoesNotExist:
            raise Ad.DoesNotExist('Объявление с указанным ID не найдено.')

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
            ad = self.get_object(pk, request.user)
            serializer = AdSerializer(ad, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Ad.DoesNotExist as e:
            return Response({'detail': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except PermissionError as e:
            return Response({'detail': str(e)}, status=status.HTTP_403_FORBIDDEN)

    @extend_schema(
        tags=['Объявления'],
        summary='Удалить объявление',
        description='Удаление объявления',
        responses={
            204: OpenApiResponse(description='Объявление успешно удалено'),
            403: OpenApiResponse(description='Доступ запрещён'),
            404: OpenApiResponse(description='Объявление с указанным ID не найдено')
        }
    )
    def delete(self, request, pk):
        try:
            ad = self.get_object(pk, request.user)
            ad.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Ad.DoesNotExist as e:
            return Response({'detail': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except PermissionError as e:
            return Response({'detail': str(e)}, status=status.HTTP_403_FORBIDDEN)


class ExchangeProposalListCreate(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    @extend_schema(
        tags=['Предложения обмена'],
        summary='Получить все предложения обмена',
        description='Получить все предложения обмена',
        request=None,
        responses={
            200: OpenApiResponse(description='Предложения успешно получены',),
        }
    )
    def get(self, request):
        exchange_proposals = ExchangeProposal.objects.all()
        serializer = ExchangeProposalSerializer(exchange_proposals, many=True)
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
        description='Удалить предложения обмена может пользователь, создавший это предложение',
        request=ExchangeProposalSerializer,
        responses={
            204: OpenApiResponse(description='Предложение успешно удалено'),
            403: OpenApiResponse(description='Доступ запрещён'),
            404: OpenApiResponse(description='Объявление с указанным ID не найдено')
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
        description='Обновить статус предложения может пользователь, получивший предложение',
        request=SpecialExchangeProposalSerializer,
        responses={
            200: OpenApiResponse(description='Статус предложения успешно обновлен'),
            400: OpenApiResponse(description='Неверные данные'),
            404: OpenApiResponse(description='Объявление с указанным ID не найдено'),
            403: OpenApiResponse(description='Доступ запрещён'),

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
