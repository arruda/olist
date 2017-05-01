# -*- coding: utf-8 -*-
from unipath import Path
from django.core.management import call_command
from django.test import TestCase
from django.utils.six import StringIO

from ..management.commands.importcategories import Command as ImportCategoriesCmd
from ..models import Category, Channel

TESTS_DIR = Path(__file__).ancestor(1)
FIXTURES_DIR = TESTS_DIR.child('fixtures')


class TestImportCategoriesCmd(TestCase):

    def test_command_output(self):
        out = StringIO()
        call_command('importcategories', 'some_channel', 'some_file', stdout=out)

        self.assertIn('some_channel', out.getvalue())
        self.assertIn('some_file', out.getvalue())

    def test_get_or_create_channel_should_return_channel_if_exist(self):
        expected_channel = Channel(name='existing_channel')
        expected_channel.save()
        cmd = ImportCategoriesCmd()
        channel = cmd.get_or_create_channel('existing_channel')

        self.assertEqual(expected_channel, channel)

    def test_get_or_create_channel_should_create_channel_if_dont_exist(self):
        cmd = ImportCategoriesCmd()
        channel = cmd.get_or_create_channel('non_existing_channel')

        self.assertEqual('non_existing_channel', channel.name)

    def test_clean_channel_categories_should_remove_all_categories_related_to_channel(self):
        channel = Channel(name="some_channel")
        channel.save()
        channel_main_cats = [Category(name='cat %d' % i, channel=channel) for i in range(3)]
        for cat in channel_main_cats:
            cat.save()

        sub_category = Category(name='sub cat', parent=channel_main_cats[0])
        sub_category.save()

        sub_category2 = Category(name='sub cat2', parent=sub_category)
        sub_category2.save()

        cmd = ImportCategoriesCmd()
        cmd.clean_channels_categories(channel)

        self.assertEqual(Category.objects.all().count(), 0)

    def test_get_category_col_number_from_csv(self):

        cmd = ImportCategoriesCmd()
        first_row = ['col1', 'col2', 'Category', 'col3']
        csv_rows = [first_row, ['1', '2', '3', '4']]
        col_num = cmd.get_category_col_number_from_csv(csv_rows)

        self.assertEqual(col_num, 2)

    def test_update_dict_from_path(self):
        cmd = ImportCategoriesCmd()
        main_dict = {'c': {}}
        main_dict = cmd.update_dict_from_path(main_dict, ['a', 'b'])
        main_dict = cmd.update_dict_from_path(main_dict, ['c', 'd'])
        main_dict = cmd.update_dict_from_path(main_dict, ['c', 'e'])
        self.assertIn('a', main_dict.keys())
        self.assertIn('b', main_dict.get('a').keys())
        self.assertIn('c', main_dict.keys())
        self.assertIn('d', main_dict.get('c').keys())
        self.assertIn('e', main_dict.get('c').keys())

    def test_create_category_and_childs(self):
        cat_dict = {'a': {'b': {'c': {}}}}
        cmd = ImportCategoriesCmd()
        cmd.create_category_and_childs('main_cat', None, cat_dict)

        cat_c = Category.objects.get(name='c')
        self.assertEqual(str(cat_c), 'main_cat/a/b/c')

    def test_parse_categories_csv(self):
        cmd = ImportCategoriesCmd()
        csv_rows = cmd.read_csv_file(FIXTURES_DIR.child('categories.csv'))
        cmd.save_categories_from_csv(csv_rows[1:], category_col_number=1)
        all_cats = Category.objects.all()
        self.assertEqual(all_cats.count(), 23)
        self.assertEquals(str(Category.objects.get(name='XBOX 360')), 'Games/XBOX 360')
        self.assertEquals(str(Category.objects.get(name='Games', parent__name='XBOX One')), 'Games/XBOX One/Games')
        self.assertEquals(str(Category.objects.get(name='Computers', parent=None)), 'Computers')
