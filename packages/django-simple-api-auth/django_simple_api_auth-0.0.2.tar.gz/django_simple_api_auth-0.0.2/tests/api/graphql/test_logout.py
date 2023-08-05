import json

import pytest
from django.contrib.auth import get_user_model
from rest_framework import status

from django_simple_api_auth.business_logic.user_create import UserCreate
from tests.api.graphql.common import BaseGrapheneQLTestCase, BaseAriadneQLTestCase

User = get_user_model()


@pytest.mark.django_db
class LogoutMixin:

    def test_logout(self):
        data = {
            "username": "test@test.com",
            "password": User.objects.make_random_password(),
        }
        user = UserCreate(**data).execute()
        self.client.force_login(user)

        mutation = '''
            mutation userLogout($input: UserLogoutMutationInput!){
                userLogout(input: $input){
                    ok,
                    errors,
                }
            }
        '''
        operation_name = 'userLogout'
        data = {
            "clientMutationId": "id",
        }
        response = self.query(mutation, operation_name=operation_name, input_data=data)
        assert response.status_code == status.HTTP_200_OK
        content = json.loads(response.content)
        assert 'errors' not in content
        assert not response.cookies.get('sessionid').value


@pytest.mark.django_db
class TestLogoutGraphene(LogoutMixin, BaseGrapheneQLTestCase):
    pass


@pytest.mark.django_db
class TestLogoutAriadne(LogoutMixin, BaseAriadneQLTestCase):
    pass
