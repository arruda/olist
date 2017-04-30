# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from ...models import Channel, Category


__all__ = ['Command']


class Command(BaseCommand):
    help = "Import categories for a given sales Channel"

    missing_args_message = "Enter a Channel name and a file name."

    def add_arguments(self, parser):
        parser.add_argument('channel_names', nargs='+')
        parser.add_argument('file_names', nargs='+')

    def handle(self, channel_names, file_names, **options):
        channel_name = channel_names[0]
        file_name = file_names[0]
        self.stdout.write(self.style.SUCCESS('%s' % channel_name))
        self.stdout.write(self.style.SUCCESS('%s' % file_name))

    def get_or_create_channel(self, channel):
        pass
