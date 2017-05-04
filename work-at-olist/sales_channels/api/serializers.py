# -*- coding: utf-8 -*-
# from django.contrib.auth.models import User

from rest_framework import serializers
from rest_framework_encrypted_lookup.serializers import EncryptedLookupHyperlinkedModelSerializer

from ..models import Category, Channel


class CategorySerializer(EncryptedLookupHyperlinkedModelSerializer):
    path = serializers.CharField(source='__str__')

    class Meta:
        model = Category
        fields = ('pk', 'name', 'path')


class CategoryWithDetailSerializer(EncryptedLookupHyperlinkedModelSerializer):
    parents = CategorySerializer(many=True, source='get_ancestors')

    children = CategorySerializer(many=True, read_only=True)
    path = serializers.CharField(source='__str__')

    class Meta:
        model = Category
        fields = ('pk', 'name', 'path', 'children', 'parents')


class ChannelSerializer(EncryptedLookupHyperlinkedModelSerializer):

    class Meta:
        model = Channel
        fields = ('pk', 'name')
