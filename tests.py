from unittest import TestCase
from io import BytesIO

from django.conf import settings
import orjson

settings.configure()

from drf_orjson.renderers import ORJSONRenderer
from drf_orjson.parsers import ORJSONParser


class ORJSONRendererTests(TestCase):
    def setUp(self):
        self.renderer = ORJSONRenderer()
        self.data = {
            'a': [1, 2, 3],
            'b': True,
            'c': 1.23,
            'd': 'test',
            'e': {'foo': 'bar'},
        }

    def test_basic_data_structures_rendered_correctly(self):

        rendered = self.renderer.render(self.data)
        reloaded = orjson.loads(rendered)

        self.assertEqual(reloaded, self.data)

    def test_renderer_works_correctly_when_media_type_and_context_provided(self):

        rendered = self.renderer.render(
            data=self.data,
            accepted_media_type='application/json',
            renderer_context={},
        )
        reloaded = orjson.loads(rendered)

        self.assertEqual(reloaded, self.data)


class ORJSONParserTests(TestCase):
    def setUp(self):
        self.parser = ORJSONParser()
        self.data = {
            'a': [1, 2, 3],
            'b': True,
            'c': 1.23,
            'd': 'test',
            'e': {'foo': 'bar'},
        }

    def test_basic_data_structures_parsed_correctly(self):

        dumped = orjson.dumps(self.data)
        parsed = self.parser.parse(BytesIO(dumped.encode('utf-8')))

        self.assertEqual(parsed, self.data)

    def test_parser_works_correctly_when_media_type_and_context_provided(self):
        dumped = orjson.dumps(self.data)
        parsed = self.parser.parse(
            stream=BytesIO(dumped.encode('utf-8')),
            accepted_media_type='application/json',
            parser_context={},
        )

        self.assertEqual(parsed, self.data)
