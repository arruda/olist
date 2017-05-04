# -*- coding: utf-8 -*-
import csv
from unipath import Path
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
        self.stdout.write(
            self.style.SUCCESS('Importing categories from "{}"" into channel "{}"'.format(file_name, channel_name))
        )
        channel = self.get_or_create_channel(channel_name)
        csv_rows = self.read_csv_file(file_name)

        category_col_number = self.get_category_col_number_from_csv(csv_rows)
        self.save_categories_from_csv(channel, csv_rows, category_col_number=category_col_number)

    def get_or_create_channel(self, channel_name):
        return Channel.objects.get_or_create(name=channel_name)[0]

    def clean_channels_categories(self, channel):
        channel.categories.all().delete()

    def read_csv_file(self, file_name):
        if file_name[0] != '/':
            file_path = Path(ROOT_DIR, file_name)
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

    def save_categories_from_csv(self, channel, csv_rows, category_col_number=0):
        categories_dict = {}
        for row in csv_rows:
            category_path = row[category_col_number]
            category_parents = category_path.split(' / ')
            categories_dict = self.update_dict_from_path(categories_dict, category_parents)
        for cat_name, childs in categories_dict.items():
            self.create_category_and_childs(channel, cat_name, None, childs)

    def create_category_and_childs(self, channel, name, parent, childs):
        category = Category(name=name, parent=parent, channel=channel)
        category.save()
        self.stdout.write(self.style.SUCCESS('Creating category: %s' % str(category)))
        for cat_name, grand_childs in childs.items():
            self.create_category_and_childs(None, cat_name, category, grand_childs)

    def get_category_col_number_from_csv(self, csv_rows):
        return csv_rows[0].index('Category')
