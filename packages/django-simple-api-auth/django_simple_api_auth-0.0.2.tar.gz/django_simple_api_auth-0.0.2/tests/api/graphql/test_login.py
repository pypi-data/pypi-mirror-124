import json

import pytest
from django.contrib.auth import get_user_model
from rest_framework import status

from django_simple_api_auth.business_logic.user_create import UserCreate
from tests.api.graphql.common import BaseGrapheneQLTestCase, BaseAriadneQLTestCase

User = get_user_model()


class LoginMixin:
    def test_login(self):
        data = {
            "username": "test@test.com",
            "password": User.objects.make_random_password(),
        }
        UserCreate(**data).execute()
        mutation = '''
            mutation userLogin($input: UserLoginMutationInput!){
                userLogin(input: $input){
                    ok,
                    errors,
                }
            }
        '''
        operation_name = 'userLogin'
        response = self.query(mutation, operation_name=operation_name, input_data=data)
        assert response.status_code == status.HTTP_200_OK
        content = json.loads(response.content)
        assert 'errors' not in content
        assert 'csrftoken' in response.cookies.keys()
        assert 'sessionid' in response.cookies.keys()


@pytest.mark.django_db
class TestLoginGraphene(LoginMixin, BaseGrapheneQLTestCase):
    pass


@pytest.mark.django_db
class TestLoginAriadne(LoginMixin, BaseAriadneQLTestCase):
    pass
