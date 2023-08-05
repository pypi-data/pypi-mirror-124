# -*- coding: utf-8 -*-

# Django imports
from django.conf import settings
from django.conf.urls import include
from django.urls import path
from django.contrib import admin
from django.http import JsonResponse

# App imports
from ariadne.contrib.django.views import GraphQLView as AriadneGraphQLView

from config.url_patterns.api import api_urls

#from tests.config.graphqls.ariadne.scheme import schema
#from tests.config.graphqls.graphene.views import CustomGraphQLViewMixin
from example.graphqls.ariadne.scheme import schema
from example.graphqls.graphene.views import CustomGraphQLViewMixin

urlpatterns = [
    path('s/', include([
        path('admin/', admin.site.urls),
        path('accounts/', include('django.contrib.auth.urls')),
        path('api/', include(api_urls, namespace='api')),
        path('graphene-graphql/', CustomGraphQLViewMixin.as_view(graphiql=True), name='graphene-graphql'),
        path('ariadne-graphql/', AriadneGraphQLView.as_view(schema=schema), name='ariadne-graphql'),
        path('__status__/', lambda _: JsonResponse({'status': 'OK'}))
    ])),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [path('__debug__/', include(debug_toolbar.urls)), ] + urlpatterns
