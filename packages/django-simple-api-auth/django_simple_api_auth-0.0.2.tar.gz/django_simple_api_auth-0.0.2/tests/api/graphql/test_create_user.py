import json

import pytest
from django.contrib.auth import get_user_model
from rest_framework import status

from django_simple_api_auth.errors import UserCreateErrors
from tests.api.graphql.common import BaseGrapheneQLTestCase, BaseAriadneQLTestCase


class CreateUserMixin:

    def setUp(self):
        self.mutation = '''
            mutation userCreate($input: UserCreateMutationInput!){
                userCreate(input: $input){
                    ok,
                    errors,
                }
            }
        '''
        self.operation_name = 'userCreate'

    def test_create_user(self):
        data = {
            "username": "test@test.com",
            "password": "Pa$$ssw0ord12345",
        }
        response = self.query(self.mutation, operation_name=self.operation_name, input_data=data)
        assert response.status_code == status.HTTP_200_OK
        content = json.loads(response.content)
        assert 'errors' not in content
        assert get_user_model().objects.count() == 1

    def test_create_user_password_too_short(self):
        data = {
            "username": "test@test.com",
            "password": "asdfg",
        }
        expected_errors = [UserCreateErrors.PASSWORD_TOO_SHORT.value]
        self.check_password_errors(data, expected_errors)

    def test_create_user_password_too_similar(self):
        data = {
            "username": "test@test.com",
            "password": "test@test.com",
        }
        expected_errors = [UserCreateErrors.PASSWORD_TOO_SIMILAR.value]
        self.check_password_errors(data, expected_errors)

    def test_create_user_password_too_common(self):
        data = {
            "username": "test@test.com",
            "password": "password",
        }
        expected_errors = [UserCreateErrors.PASSWORD_TOO_COMMON.value]
        self.check_password_errors(data, expected_errors)

    def test_create_user_password_numeric(self):
        data = {
            "username": "test@test.com",
            "password": "12345678",
        }
        expected_errors = [UserCreateErrors.PASSWORD_ENTIRELY_NUMERIC.value]
        self.check_password_errors(data, expected_errors)

    def check_password_errors(self, data, expected_errors):
        response = self.query(self.mutation, operation_name=self.operation_name, input_data=data)
        assert response.status_code == status.HTTP_200_OK
        content = json.loads(response.content)
        assert not content['data']['userCreate']['ok']
        assert all(error in content['data']['userCreate']['errors'] for error in expected_errors)
        assert get_user_model().objects.count() == 0


@pytest.mark.django_db
class TestCreateUserGraphene(CreateUserMixin, BaseGrapheneQLTestCase):
    pass


@pytest.mark.django_db
class TestCreateUserAriadne(CreateUserMixin, BaseAriadneQLTestCase):
    pass
