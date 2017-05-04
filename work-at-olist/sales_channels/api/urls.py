# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from rest_framework import routers
from rest_framework.documentation import include_docs_urls
from .import views

router = routers.DefaultRouter()
router.register(r'channels', views.ChannelViewSet)
router.register(r'categories', views.CategoryDetailViewSet)
router.register(r'categories_in_channel', views.CategoriesInChannelList, base_name='categories_in_channel')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^docs/', include_docs_urls(title='Work-at-olist API'))
]
