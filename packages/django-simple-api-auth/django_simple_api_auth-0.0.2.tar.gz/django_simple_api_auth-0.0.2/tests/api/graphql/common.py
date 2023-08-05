import pytest
from graphene_django.utils.testing import graphql_query, GraphQLTestCase


class BaseGrapheneQLTestCase(GraphQLTestCase):
    GRAPHQL_URL = '/s/graphene-graphql/'


class BaseAriadneQLTestCase(GraphQLTestCase):
    GRAPHQL_URL = '/s/ariadne-graphql/'
