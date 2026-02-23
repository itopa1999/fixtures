"""
Tournament Admin Views URLs
Custom admin dashboard and management endpoints
"""

from django.urls import path, include
from .admin_views import *

app_name = 'tour_admin'

auth_urls = [
    path('login/', AdminLoginView.as_view(), name='login'),
]

urlpatterns = [
    path('auth/', include(auth_urls)),
]
