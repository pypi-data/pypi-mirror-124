import os

from ariadne import make_executable_schema, gql, load_schema_from_path
import django_simple_api_auth.api.graphql.ariadne
from django_simple_api_auth.api.graphql.ariadne.mutations import mutation
from django_simple_api_auth.api.graphql.ariadne.queries import query

auth_types_graphql_dirname = os.path.dirname(django_simple_api_auth.api.graphql.ariadne.__file__)
auth_type_defs = gql(load_schema_from_path(f"{auth_types_graphql_dirname}"))

type_defs_list = [
    auth_type_defs,
]
schema = make_executable_schema([*type_defs_list], [mutation, query])
