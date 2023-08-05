# # -*- coding: utf-8 -*-
# # Python imports
# from functools import partial
#
# # Django imports
# from django.db.models import QuerySet
#
# # 3rd Party imports
# import graphene
# from graphene import PageInfo
# from graphql_relay.utils import base64, is_str, unbase64
#
#
# # App imports
#
#
# class MrMFilteredField(graphene.relay.ConnectionField):
#     filter_classes = []
#
#     def __init__(self, *args, **kwargs):
#         self.filter_map = {}
#         for f in self.filter_classes:
#             self.filter_map[f.name] = f
#             kwargs.setdefault(f.name, f.type())
#         super(MrMFilteredField, self).__init__(*args, **kwargs)
#
#     @classmethod
#     def resolve_and_filter(cls, root, info, parent_resolver=None, filters=None, **args):
#         iterable = parent_resolver(root, info, **args)
#         if filters and isinstance(iterable, QuerySet):
#             for key in args:
#                 if key in filters:
#                     iterable = filters[key].filter(iterable, args[key])
#
#             pass
#         return iterable
#
#     def get_resolver(self, parent_resolver):
#         resolver = partial(self.resolve_and_filter, parent_resolver=parent_resolver, filters=self.filter_map)
#         return super(MrMFilteredField, self).get_resolver(resolver)
#
#
# class MrMOffsetPaginationQuerysetFieldMixin(object):
#     PREFIX = 'offset:'
#
#     @classmethod
#     def offset_to_cursor(cls, offset):
#         return base64(cls.PREFIX + str(offset))
#
#     @classmethod
#     def cursor_to_offset(cls, cursor):
#         try:
#             return int(unbase64(cursor)[len(cls.PREFIX):])
#         except:
#             return None
#
#     @classmethod
#     def get_offset_with_default(cls, cursor=None, default_offset=0):
#         if not is_str(cursor):
#             return default_offset
#
#         offset = cls.cursor_to_offset(cursor)
#         try:
#             return int(offset)
#         except:
#             return default_offset
#
#     @classmethod
#     def resolve_connection(cls, connection_type, args, resolved):
#         if isinstance(resolved, connection_type):
#             return resolved
#
#         assert isinstance(resolved, QuerySet), (
#             'Resolved value from the connection field have to be a QuerySet or instance of {}. '
#             'Received "{}"'
#         ).format(connection_type, resolved)
#
#         list_length = resolved.count()
#
#         args = args or {}
#
#         slice_start = 0
#
#         before = args.get('before')
#         after = args.get('after')
#         first = args.get('first')
#         last = args.get('last')
#         slice_end = slice_start + list_length
#         before_offset = cls.get_offset_with_default(before, list_length)
#         after_offset = cls.get_offset_with_default(after, -1)
#
#         start_offset = max(
#             slice_start - 1,
#             after_offset,
#             -1
#         ) + 1
#         end_offset = min(
#             slice_end,
#             before_offset,
#             list_length
#         )
#         if isinstance(first, int):
#             end_offset = min(
#                 end_offset,
#                 start_offset + first
#             )
#         if isinstance(last, int):
#             start_offset = max(
#                 start_offset,
#                 end_offset - last
#             )
#
#         offset = max(start_offset - slice_start, 0)
#         limit = list_length - (slice_end - end_offset)
#         items = resolved[offset:limit]
#
#         edges = [
#             connection_type.Edge(
#                 node=node,
#                 cursor=cls.offset_to_cursor(start_offset + i)
#             )
#             for i, node in enumerate(items)
#         ]
#
#         first_edge_cursor = edges[0].cursor if edges else None
#         last_edge_cursor = edges[-1].cursor if edges else None
#         lower_bound = after_offset + 1 if after else 0
#         upper_bound = before_offset if before else list_length
#
#         connection = connection_type(
#             edges=edges,
#             page_info=PageInfo(
#                 start_cursor=first_edge_cursor,
#                 end_cursor=last_edge_cursor,
#                 has_previous_page=isinstance(last, int) and start_offset > lower_bound,
#                 has_next_page=isinstance(first, int) and end_offset < upper_bound
#             )
#         )
#
#         connection.iterable = resolved
#         connection.iterable_total_count = list_length
#         return connection
