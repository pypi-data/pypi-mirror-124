import os

from ariadne import make_executable_schema, gql, load_schema_from_path
import django_simple_api_auth.api.graphql.ariadne
from django_simple_api_auth.api.graphql.ariadne.mutations import mutation as auth_mutations
from django_simple_api_auth.api.graphql.ariadne.queries import query as auth_query
from example.graphqls.ariadne.queries import query

auth_types_graphql_dirname = os.path.dirname(django_simple_api_auth.api.graphql.ariadne.__file__)
auth_mutations_type_defs = gql(load_schema_from_path(f"{auth_types_graphql_dirname}/mutations.graphql"))
auth_queries_type_defs = gql(load_schema_from_path(f"{auth_types_graphql_dirname}/queries.graphql"))
type_defs = gql(load_schema_from_path('./graphqls/ariadne/scheme.graphql'))

type_defs_list = [
    auth_mutations_type_defs,
    auth_queries_type_defs,
    type_defs,
]
schema = make_executable_schema([*type_defs_list], [auth_mutations, auth_query, query])
