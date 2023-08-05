import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from django_simple_api_auth.business_logic.user_create import UserCreate

User = get_user_model()


@pytest.mark.django_db
class TestMe(APITestCase):
    def setUp(self):
        self.url = reverse('api:v1.0:users-me')

    def test_me(self):
        data = {
            "username": "test@test.com",
            "password": User.objects.make_random_password(),
        }
        user = UserCreate(**data).execute()
        self.client.force_login(user)
        response = self.client.get(self.url, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == user.id
