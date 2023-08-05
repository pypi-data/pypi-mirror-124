from ariadne import QueryType

query = QueryType()


@query.field("dummy")
def resolve_get_dummy(_, info):
    return "dummy"
