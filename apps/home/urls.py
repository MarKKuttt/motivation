# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views
from . import views
from .file_formatters import export_users_xls

urlpatterns = [

    # The home page
    # path('home', views.index, name='home'),

    path('', views.main_page, name='main_page'),
    path('export/', export_users_xls, name='export_to_excel'),
    path('datatable.html/', views.your_view, name='your_view'),


    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]

