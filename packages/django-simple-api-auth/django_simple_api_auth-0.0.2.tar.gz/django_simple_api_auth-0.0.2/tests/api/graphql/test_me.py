import json

import pytest
from django.contrib.auth import get_user_model
from graphql_relay import from_global_id
from rest_framework import status

from django_simple_api_auth.business_logic.user_create import UserCreate
from tests.api.graphql.common import BaseGrapheneQLTestCase, BaseAriadneQLTestCase

User = get_user_model()


@pytest.mark.django_db
class MeMixin:

    def test_me(self):
        data = {
            "username": "test@test.com",
            "password": User.objects.make_random_password(),
        }
        user = UserCreate(**data).execute()
        self.client.force_login(user)
        query = '''
            query getMe{
                getMe{
                    id,
                }
            }
        '''
        operation_name = 'getMe'
        response = self.query(query, operation_name=operation_name)
        assert response.status_code == status.HTTP_200_OK
        content = json.loads(response.content)
        assert 'errors' not in content
        id = content['data'][operation_name]['id']
        assert int(id) == user.id


@pytest.mark.django_db
class TestMeGraphene(MeMixin, BaseGrapheneQLTestCase):
    pass


@pytest.mark.django_db
class TestMeAriadne(MeMixin, BaseAriadneQLTestCase):
    pass
