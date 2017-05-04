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


class CategoriesInChannelList(
        EncryptedLookupGenericViewSet,
        viewsets.mixins.RetrieveModelMixin):
    """
    Return's the list of categories that belong to a given channel
    """
    serializer_class = CategorySerializer
    lookup_field = 'pk'

    def retrieve(self, request, pk=None):
        queryset = self.get_queryset()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        lookup_field = self.kwargs.get('pk', None)
        if not lookup_field:
            raise Http404

        root_cat = Category.objects.filter(channel__pk=lookup_field)
        return Category.objects.get_queryset_descendants(root_cat, include_self=True)
