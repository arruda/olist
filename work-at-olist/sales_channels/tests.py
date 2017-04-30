# -*- coding: utf-8 -*-
from django.core.management import call_command
from django.test import TestCase
from django.utils.six import StringIO

from .management.commands.importcategories import Command as ImportCategoriesCmd
from .models import Category, Channel


class TestCategory(TestCase):

    def test_category_str_should_return_correctly_listing_of_parents(self):
        cat_1 = Category(name='cat 1')
        cat_1.save()

        cat_1_a = Category(name='cat 1-A', parent=cat_1)
        cat_1_a.save()

        cat_1_a_2 = Category(name='cat 1-A-2', parent=cat_1_a)
        cat_1_a_2.save()

        cat_1_b = Category(name='cat 1-B', parent=cat_1)
        cat_1_b.save()

        self.assertEqual(str(cat_1), 'cat 1')
        self.assertEqual(str(cat_1_a), 'cat 1/cat 1-A')
        self.assertEqual(str(cat_1_a_2), 'cat 1/cat 1-A/cat 1-A-2')
        self.assertEqual(str(cat_1_b), 'cat 1/cat 1-B')

    def test_category_str_should_return_correctly_when_not_saved(self):
        cat_1 = Category(name='cat 1')
        cat_1.save()

        cat_1_a = Category(name='cat 1-A', parent=cat_1)

        self.assertEqual(str(cat_1_a), 'cat 1-A')


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
