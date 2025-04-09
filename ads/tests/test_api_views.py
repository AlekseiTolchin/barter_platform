from django.contrib.auth.models import User

from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from ads.models import Ad, ExchangeProposal


class AdAPITestCase(APITestCase):
    def setUp(self):
        """Настройка тестовой среды."""
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.other_user = User.objects.create_user(username='otheruser', password='password123')

        self.ad = Ad.objects.create(title='Test Ad', description='Test Description', user=self.user)

        self.list_create_url = '/api/ads/'
        self.detail_url = f'/api/ads/{self.ad.id}/'

    def test_get_ads_list_unauthenticated(self):
        """Тест получения списка объявлений без аутентификации."""
        response = self.client.get(self.list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Test Ad', str(response.data))

    def test_create_ad_authenticated(self):
        """Тест создания объявления аутентифицированным пользователем."""
        self.client.force_authenticate(user=self.user)
        payload = {
            'title': 'New Ad',
            'description': 'Ad description',
            'category': 'Ad category',
            'condition': 'new'
        }
        response = self.client.post(self.list_create_url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], payload['title'])

    def test_create_ad_unauthenticated(self):
        """Тест создания объявления неаутентифицированным пользователем."""
        payload = {
            'title': 'New Ad',
            'description': 'Ad description',
            'category': 'Ad category',
            'condition': 'new'
        }
        response = self.client.post(self.list_create_url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_ad_authenticated_owner(self):
        """Тест обновления объявления аутентифицированным владельцем."""
        self.client.force_authenticate(user=self.user)
        payload = {
            'title': 'Updated Title'
        }
        response = self.client.patch(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], payload['title'])

    def test_update_ad_authenticated_non_owner(self):
        """Тест обновления объявления аутентифицированным НЕ владельцем."""
        self.client.force_authenticate(user=self.other_user)
        payload = {
            'title': 'Updated Title'
        }
        response = self.client.patch(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_ad_authenticated_owner(self):
        """Тест удаления объявления аутентифицированным владельцем."""
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Ad.objects.filter(id=self.ad.id).exists())

    def test_delete_ad_authenticated_non_owner(self):
        """Тест удаления объявления аутентифицированным НЕ владельцем."""
        self.client.force_authenticate(user=self.other_user)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ExchangeProposalAPITestCase(APITestCase):
    def setUp(self):
        """Настройка тестовой среды."""
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.other_user = User.objects.create_user(username='otheruser', password='password123')

        self.ad1 = Ad.objects.create(title='Ad 1', description='Description 1', user=self.user)
        self.ad2 = Ad.objects.create(title='Ad 2', description='Description 2', user=self.other_user)

        self.proposal = ExchangeProposal.objects.create(ad_sender=self.ad1, ad_receiver=self.ad2, status='pending')
        self.list_create_url = '/api/proposals/'
        self.detail_url = f'/api/proposals/{self.proposal.id}/'

    def test_get_exchange_proposals(self):
        """Тест получения списка предложений обмена."""
        response = self.client.get(self.list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_exchange_proposal_authenticated(self):
        """Тест создания предложения обмена аутентифицированным пользователем."""
        self.client.force_authenticate(user=self.user)
        payload = {
            'ad_sender': self.ad1.id,
            'ad_receiver': self.ad2.id,
            'comment': 'Test comment',
        }
        response = self.client.post(self.list_create_url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_exchange_proposal_authenticated_sender(self):
        """Тест удаления предложения обмена отправителем."""
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_exchange_proposal_authenticated_non_sender(self):
        """Тест удаления предложения обмена не отправителем."""
        self.client.force_authenticate(user=self.other_user)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_exchange_proposal_status_authenticated_receiver(self):
        """Тест обновления статуса предложения обмена получателем."""
        self.client.force_authenticate(user=self.other_user)
        payload = {'status': 'accepted'}
        response = self.client.patch(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'accepted')

    def test_update_exchange_proposal_status_authenticated_non_receiver(self):
        """Тест обновления статуса предложения обмена НЕ получателем."""
        self.client.force_authenticate(user=self.user)
        payload = {'status': 'accepted'}
        response = self.client.patch(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_exchange_proposal_status_invalid_field(self):
        """Тест попытки обновления недопустимого поля предложения обмена."""
        self.client.force_authenticate(user=self.other_user)
        payload = {'invalid_field': 'value'}
        response = self.client.patch(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Вы можете обновить только поле', str(response.data))
