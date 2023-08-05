# # -*- coding: utf-8 -*-
# # Python imports
#
# # Django imports
#
# # 3rd Party imports
# import graphene
#
#
# # App imports
#
#
# class MrMCountableConnectionMixin(object):
#     total_count = graphene.Int()
#
#     def resolve_total_count(self, info):
#         if hasattr(self, 'iterable_total_count'):
#             return self.iterable_total_count
#         return self.iterable.count()
