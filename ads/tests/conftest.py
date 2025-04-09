from django.contrib.auth.models import User

import pytest

from ads.models import Ad


@pytest.fixture
def user_sender(db):
    """Создание пользователя-отправителя для тестов."""
    return User.objects.create_user(username='sender_user', password='senderpass')

@pytest.fixture
def user_receiver(db):
    """Создание пользователя-получателя для тестов."""
    return User.objects.create_user(username='receiver_user', password='receiverpass')

@pytest.fixture
def ad_sender(db, user_sender):
    """Создание объявления отправителя."""
    return Ad.objects.create(title='Sender Ad', description='Sender Ad Description', user=user_sender)

@pytest.fixture
def ad_receiver(db, user_receiver):
    """Создание объявления получателя."""
    return Ad.objects.create(title='Receiver Ad', description='Receiver Ad Description', user=user_receiver)

@pytest.fixture
def client_logged_in(client, user_sender):
    """Логиним клиента как отправителя для использования в тестах."""
    client.login(username='sender_user', password='senderpass')
    return client