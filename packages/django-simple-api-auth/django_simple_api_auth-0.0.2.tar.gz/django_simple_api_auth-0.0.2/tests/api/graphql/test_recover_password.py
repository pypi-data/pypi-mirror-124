import json

import pytest
from django.contrib.auth import get_user_model
from rest_framework import status

from django_simple_api_auth.business_logic.user_create import UserCreate
from tests.api.graphql.common import BaseGrapheneQLTestCase, BaseAriadneQLTestCase

User = get_user_model()


@pytest.mark.django_db
class RecoverPasswordMixin:

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
        mutation = '''
            mutation userPasswordRecovery($input: UserPasswordRecoveryMutationInput!){
                userPasswordRecovery(input: $input){
                    ok,
                }
            }
        '''
        operation_name = 'userPasswordRecovery'
        response = self.query(mutation, operation_name=operation_name, input_data=data)
        assert response.status_code == status.HTTP_200_OK
        content = json.loads(response.content)
        assert 'errors' not in content


@pytest.mark.django_db
class TestRecoverPasswordGraphene(RecoverPasswordMixin, BaseGrapheneQLTestCase):
    pass


@pytest.mark.django_db
class TestRecoverPasswordAriadne(RecoverPasswordMixin, BaseAriadneQLTestCase):
    pass
