from abc import ABC, abstractmethod
from typing import Any

from graphql import GraphQLResolveInfo


class ClientIDMutationMixin(ABC):

    def __call__(self, obj: Any, info: GraphQLResolveInfo, **data):
        client_mutation_id = data['input'].pop('clientMutationId', None)
        response = self.mutate(obj, info, **data)
        if client_mutation_id:
            response['clientMutationId'] = client_mutation_id
        return response

    @abstractmethod
    def mutate(self, obj: Any, info: GraphQLResolveInfo, **data):
        raise NotImplementedError
