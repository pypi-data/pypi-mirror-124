# # -*- coding: utf-8 -*-
# # Python imports
#
# # Django imports
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.utils.decorators import classonlymethod
# from django.views.decorators.csrf import csrf_exempt
#
# # 3rd Party imports
# from graphene_django.views import GraphQLView as BaseView
# from rest_framework.request import Request
# from rest_framework.settings import api_settings
#
#
# # App imports
#
#
# class MrMGraphQLViewMixin(LoginRequiredMixin):
#     def parse_body(self, request):
#         content_type = self.get_content_type(request)
#         if content_type in ['application/x-www-form-urlencoded', 'multipart/form-data']:
#             return {}
#         return super(MrMGraphQLViewMixin, self).parse_body(request)
#
#     @classonlymethod
#     def as_view(cls, **initkwargs):
#         fn = super(MrMGraphQLViewMixin, cls).as_view(**initkwargs)
#         return csrf_exempt(fn)
#
#     def authenticate(self, request):
#         rq = Request(request)
#         for auth in api_settings.DEFAULT_AUTHENTICATION_CLASSES:
#             try:
#                 (user, token) = auth().authenticate(rq)
#                 request.user = user
#             except Exception as e:
#                 pass
#
#     def dispatch(self, request, *args, **kwargs):
#         self.authenticate(request)
#         return super(MrMGraphQLViewMixin, self).dispatch(request, *args, **kwargs)
#
#
# class GraphQLView(MrMGraphQLViewMixin, BaseView):
#     pass
