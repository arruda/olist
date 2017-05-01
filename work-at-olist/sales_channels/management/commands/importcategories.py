# -*- coding: utf-8 -*-
import csv

from django.conf import settings
from django.core.management.base import BaseCommand
from ...models import Channel, Category


__all__ = ['Command']

ROOT_DIR = settings.ROOT_DIR


class Command(BaseCommand):
    help = "Import categories for a given sales Channel"

    missing_args_message = "Enter a Channel name and a csv file relative to the project root dir (%s)." % ROOT_DIR

    def add_arguments(self, parser):
        parser.add_argument('channel_names', nargs='+')
        parser.add_argument('file_names', nargs='+')

    def handle(self, channel_names, file_names, **options):
        channel_name = channel_names[0]
        file_name = file_names[0]
        self.stdout.write(self.style.SUCCESS('%s' % channel_name))
        self.stdout.write(self.style.SUCCESS('%s' % file_name))

    def get_or_create_channel(self, channel_name):
        return Channel.objects.get_or_create(name=channel_name)[0]

    def clean_channels_categories(self, channel):
        channel.categories.all().delete()

    def read_csv_file(self, file_name):
        if file_name[0] != '/':
            file_path = ROOT_DIR.child(file_name)
        else:
            file_path = file_name

        rows = []
        with open(file_path) as f:
            reader = csv.reader(f)
            for row in reader:
                rows.append(row)
        return rows

    def update_dict_from_path(self, main_dict, category_list):
        last_category_dict = main_dict
        for cat_name in category_list:
            new_category = last_category_dict.get(cat_name, {})
            last_category_dict[cat_name] = new_category
            last_category_dict = new_category
        return main_dict

    def save_categories_from_csv(self, csv_rows, category_col_number=0):
        categories_dict = {}
        for row in csv_rows:
            category_path = row[category_col_number]
            category_parents = category_path.split(' / ')
            categories_dict = self.update_dict_from_path(categories_dict, category_parents)
        for cat_name, childs in categories_dict.items():
            self.create_category_and_childs(cat_name, None, childs)

    def create_category_and_childs(self, name, parent, childs):
        category = Category(name=name, parent=parent)
        category.save()
        for cat_name, grand_childs in childs.items():
            self.create_category_and_childs(cat_name, category, grand_childs)

    def get_category_col_number_from_csv(self, csv_rows):
        return csv_rows[0].index('Category')
