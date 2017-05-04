# -*- coding: utf-8 -*-
import binascii

from django.http import Http404
from rest_framework import viewsets

from rest_framework_encrypted_lookup.views import EncryptedLookupGenericViewSet
from rest_framework.response import Response

from .serializers import CategorySerializer, CategoryWithDetailSerializer, ChannelSerializer

from ..models import Category, Channel


class ChannelViewSet(EncryptedLookupGenericViewSet, viewsets.mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer
    lookup_field = 'pk'

