# -*- coding: utf-8 -*-
# Python imports

# Django imports
from django.urls import re_path, include, path

# 3rd Party imports

# App imports
from rest_framework.routers import DefaultRouter

from django_simple_api_auth.api.rest.v1_0.viewsets import UserApiViewSet

router = DefaultRouter()

router.register(r'users', UserApiViewSet, 'users')
api_v1_0_urls = (
    [
        path('', include(router.urls)),
    ], 'main_api_v1_0'
)
