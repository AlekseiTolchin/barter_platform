from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserSerializer


class RegisterAPIView(APIView):

    @extend_schema(
        tags=['Регистрация и аутентификация'],
        summary='Зарегистрировать пользователя',
        description='Введите имя пользователя и пароль',
        request=UserSerializer,
        responses={
            201: OpenApiResponse(
                response=UserSerializer,
                description='Пользователь успешно зарегистрирован'
            ),
            400: OpenApiResponse(
                description='Неверные данные'
            )
        }
    )

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            data = {
                'id': user.id,
                'username': user.username,
                'message': 'Пользователь успешно зарегистрирован'
            }
            return Response(data, status=201)
        return Response(serializer.errors, status=400)
