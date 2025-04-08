from django.contrib.auth.models import User
from django.urls import reverse

import pytest

from ads.models import Ad, ExchangeProposal


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


@pytest.mark.django_db
def test_ad_create_view(client_logged_in):
    """Тест создания объявления через AdCreateView."""
    url = reverse('ads:ad_form')
    data = {
        'title': 'New Ad',
        'description': 'This is a new ad.',
        'condition': 'new',
        'category': 'some'
    }
    response = client_logged_in.post(url, data)

    assert response.status_code == 302
    assert response.url == reverse('ads:ad_list')
    assert Ad.objects.filter(title='New Ad').exists()


@pytest.mark.django_db
def test_ad_list_view(client, ad_sender):
    """Тест просмотра списка объявлений через AdListView."""
    url = reverse('ads:ad_list')
    response = client.get(url)
    assert response.status_code == 200
    assert 'Sender Ad' in response.content.decode()


@pytest.mark.django_db
def test_ad_detail_view(client, ad_sender):
    """Тест просмотра объявления через AdDetailView."""
    url = reverse('ads:ad_detail', args=[ad_sender.id])
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_ad_update_view(client_logged_in, ad_sender):
    """Тест обновления объявления через AdUpdateView."""
    url = reverse('ads:update_ad', args=[ad_sender.id])
    data = {
        'title': 'Updated Ad',
        'description': 'Updated Description',
        'condition': 'new',
        'category': 'some'
    }
    response = client_logged_in.post(url, data)
    assert response.status_code == 302
    ad_sender.refresh_from_db()
    assert ad_sender.title == 'Updated Ad'


@pytest.mark.django_db
def test_ad_delete_view(client_logged_in, ad_sender):
    """Тест удаления объявления через AdDeleteView."""
    url = reverse('ads:delete_ad', args=[ad_sender.id])
    response = client_logged_in.post(url)
    assert response.status_code == 302
    assert not Ad.objects.filter(id=ad_sender.id).exists()


@pytest.mark.django_db
def test_exchange_proposal_update_view(client_logged_in, ad_sender):
    """Тест обновления предложения обмена через ExchangeProposalUpdateView."""
    proposal = ExchangeProposal.objects.create(
        ad_sender=ad_sender,
        ad_receiver=ad_sender,
        status='pending',
    )
    url = reverse('ads:proposal_update', args=[proposal.id])
    data = {
        'status': 'accepted',
    }
    response = client_logged_in.post(url, data)
    assert response.status_code == 302
    proposal.refresh_from_db()
    assert proposal.status == 'accepted'


@pytest.mark.django_db
def test_exchange_proposal_delete_view(client_logged_in, ad_sender):
    """Тест удаления предложения обмена через ExchangeProposalDeleteView."""
    proposal = ExchangeProposal.objects.create(
        ad_sender=ad_sender,
        ad_receiver=ad_sender,
        comment='Test comment'
    )
    url = reverse('ads:proposal_delete', args=[proposal.id])
    response = client_logged_in.post(url)
    assert response.status_code == 302
    assert not ExchangeProposal.objects.filter(id=proposal.id).exists()


@pytest.mark.django_db
def test_exchange_proposal_create_view(client_logged_in, ad_sender, ad_receiver):
    """Тест создания предложения обмена через ExchangeProposalCreateView."""
    url = reverse('ads:proposal_create')
    data = {
        'ad_sender': ad_sender.id,
        'ad_receiver': ad_receiver.id,
        'comment': 'Test comment',
    }
    response = client_logged_in.post(url, data)
    assert response.status_code == 302
    assert ExchangeProposal.objects.filter(comment='Test comment').exists()


@pytest.mark.django_db
def test_exchange_proposal_list_view(client, ad_sender, ad_receiver):
    """Тест просмотра списка предложений обмена через ExchangeProposalListView."""
    ExchangeProposal.objects.create(
        ad_sender=ad_sender,
        ad_receiver=ad_receiver,
        comment='Test comment',
    )
    url = reverse('ads:proposal_list')
    response = client.get(url)
    assert response.status_code == 200
