# -*- coding: utf-8 -*-# -*- coding: utf-8 -*-
from unipath import Path

from django.core.management import call_command
from django.test import TestCase
from django.utils.six import StringIO

from rest_framework.test import APIClient

from ..api.serializers import ChannelSerializer
from ..models import Category, Channel

TESTS_DIR = Path(__file__).ancestor(1)
FIXTURES_DIR = TESTS_DIR.child('fixtures')


class TestAPI(TestCase):

    def setUp(self):
        out = StringIO()
        self.channels = [Channel.objects.create(name="ch%d" % i) for i in range(3)]
        for i in range(3):
            call_command('importcategories', 'ch%d' % i, FIXTURES_DIR.child('categories.csv'), stdout=out)

    def test_list_channels_url_exist(self):
        client = APIClient()
        response = client.get('/api/channels/')
        self.assertEqual(response.status_code, 200)

    def test_list_channels_should_return_channels(self):
        client = APIClient()
        response = client.get('/api/channels/')
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertEqual(response_json.get('count'), 3)
        self.assertEqual(response_json.get('results')[0].get('name'), 'ch0')
        self.assertEqual(response_json.get('results')[1].get('name'), 'ch1')
        self.assertEqual(response_json.get('results')[2].get('name'), 'ch2')

    def test_list_categories_in_channel_should_return_all_categories_related(self):
        cipher = ChannelSerializer(instance=self.channels[0]).get_cipher()
        channel_pk_encrypt = cipher.encode(self.channels[0].pk)
        client = APIClient()
        response = client.get('/api/categories_in_channel/{}/'.format(channel_pk_encrypt))
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertEqual(response_json.get('count'), 24)

    def test_categories_detail_should_return_all_child(self):
        cipher = ChannelSerializer(instance=self.channels[0]).get_cipher()
        books_computer_cat = Category.objects.get(
            name='Computers', parent__name='Books', parent__channel=self.channels[0]
        )
        cat_pk_encrypt = cipher.encode(books_computer_cat.pk)
        client = APIClient()
        response = client.get('/api/categories/{}/'.format(cat_pk_encrypt))
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertEqual(response_json.get('path'), 'Books/Computers')
        self.assertEqual(len(response_json.get('children')), 3)
        self.assertEqual(response_json.get('children')[0].get('path'), 'Books/Computers/Applications')
        self.assertEqual(response_json.get('children')[1].get('path'), 'Books/Computers/Database')
        self.assertEqual(response_json.get('children')[2].get('path'), 'Books/Computers/Programming')

    def test_categories_detail_should_return_all_parents(self):
        cipher = ChannelSerializer(instance=self.channels[0]).get_cipher()
        books_computer_aplications_cat = Category.objects.filter(
            name='Applications'
        )[0]
        cat_pk_encrypt = cipher.encode(books_computer_aplications_cat.pk)
        client = APIClient()
        response = client.get('/api/categories/{}/'.format(cat_pk_encrypt))
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertEqual(response_json.get('path'), 'Books/Computers/Applications')
        self.assertEqual(len(response_json.get('parents')), 2)
        self.assertEqual(response_json.get('parents')[0].get('path'), 'Books')
        self.assertEqual(response_json.get('parents')[1].get('path'), 'Books/Computers')
