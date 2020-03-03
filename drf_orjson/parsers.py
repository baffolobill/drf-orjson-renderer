import codecs

import orjson
from django.conf import settings
from rest_framework.parsers import BaseParser, ParseError
from rest_framework.renderers import JSONRenderer


class ORJSONParser(BaseParser):
    """
    Parses JSON-serialized data.
    """
    media_type = 'application/json'
    renderer_class = JSONRenderer

    def parse(self, stream, media_type=None, parser_context=None):
        """
        Parses the incoming bytestream as JSON and returns the resulting data.
        """
        parser_context = parser_context or {}
        encoding = parser_context.get('encoding', settings.DEFAULT_CHARSET)

        try:
            decoded_stream = codecs.getreader(encoding)(stream)
            return orjson.loads(decoded_stream)
        except ValueError as exc:
            raise ParseError('JSON parse error - %s' % str(exc))
