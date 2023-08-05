# -*- coding: utf-8 -*-
# Python imports

# Django imports
from django.urls import include, path

# 3rd Party imports

# App imports
from config.url_patterns.v1_0 import api_v1_0_urls

api_urls = (
    [
        path('1.0/', include(api_v1_0_urls, namespace='v1.0')),
    ], 'main_api')
