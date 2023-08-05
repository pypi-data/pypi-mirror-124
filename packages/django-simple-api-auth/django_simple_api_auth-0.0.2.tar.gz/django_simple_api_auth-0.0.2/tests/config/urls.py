# -*- coding: utf-8 -*-

# Django imports
from ariadne.contrib.django.views import GraphQLView as AriadneGraphQLView
from django.conf import settings
from django.conf.urls import include
from django.urls import path

from tests.config.graphqls.ariadne.scheme import schema
from tests.config.graphqls.graphene.views import CustomGraphQLViewMixin
from tests.config.url_patterns.api import api_urls

# App imports

urlpatterns = [
    path('s/', include([
        path('api/', include(api_urls, namespace='api')),
        path('graphene-graphql/', CustomGraphQLViewMixin.as_view(graphiql=True), name='graphene-graphql'),
        path('ariadne-graphql/', AriadneGraphQLView.as_view(schema=schema), name='ariadne-graphql'),
    ])),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [path('__debug__/', include(debug_toolbar.urls)), ] + urlpatterns
