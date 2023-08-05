from ariadne import QueryType

query = QueryType()


@query.field("getMe")
def resolve_get_me(_, info):
    user = info.context["request"].user
    if user.is_authenticated:
        return info.context["request"].user
    return None
