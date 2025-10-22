# -*- coding: utf-8 -*-
"""
URLs do app PDF Extractor
"""

from django.urls import path
from . import views

app_name = 'pdf_extractor'

urlpatterns = [
    path('', views.pdf_extractor_index, name='index'),
    path('api/extract/', views.extract_pdf_data, name='extract_data'),
]


