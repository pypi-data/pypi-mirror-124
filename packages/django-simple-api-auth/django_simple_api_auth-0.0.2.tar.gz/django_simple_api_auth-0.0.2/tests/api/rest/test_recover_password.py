import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from django_simple_api_auth.business_logic.user_create import UserCreate

User = get_user_model()

@pytest.mark.django_db
class TestRecoverPassword(APITestCase):
    def setUp(self):
        self.url = reverse('api:v1.0:users-password-recovery')

    def test_recover_password(self):
        username = "test@test.com"
        data = {
            "email": username
        }
        create_data = {
            "username": username,
            "password": User.objects.make_random_password(),
        }
        UserCreate(**create_data).execute()
        response = self.client.post(self.url, data=data, format='json')
        assert response.status_code == status.HTTP_200_OK
