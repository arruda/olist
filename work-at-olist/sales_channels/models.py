# -*- coding: utf-8 -*-
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.translation import ugettext_lazy as _


class Channel(models.Model):
    name = models.CharField(max_length=250, verbose_name=_('Name'), unique=True, blank=False, null=False)

    def __str__(self):
        return "{}".format(self.name)


class Category(MPTTModel):
    name = models.CharField(max_length=100, verbose_name=_('Name'), blank=False, null=False)
    channel = models.ForeignKey('Channel', verbose_name=_('Channel'), related_name='categories', blank=True, null=True)
    parent = TreeForeignKey(
        'self',
        verbose_name=_('Parent'),
        null=True,
        blank=True,
        related_name='children',
        db_index=True
    )

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        try:
            category_names = [c.name for c in self.get_ancestors(ascending=False, include_self=True)]
        except ValueError as e:
            return self.name
        else:
            return "/".join(category_names)
