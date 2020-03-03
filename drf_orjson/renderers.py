import orjson
from django.http.multipartparser import parse_header
from rest_framework.compat import (
    INDENT_SEPARATORS, LONG_SEPARATORS, SHORT_SEPARATORS,
)
from rest_framework.renderers import BaseRenderer, zero_as_none
from rest_framework.settings import api_settings
from rest_framework.utils import encoders
# from rest_framework.compat import six


class ORJSONRenderer(BaseRenderer):
    """
    Renderer which serializes to JSON.
    """
    media_type = 'application/json'
    format = 'json'
    encoder_class = encoders.JSONEncoder
    # ensure_ascii = not api_settings.UNICODE_JSON
    # compact = api_settings.COMPACT_JSON
    # strict = api_settings.STRICT_JSON

    # We don't set a charset because JSON is a binary encoding,
    # that can be encoded as utf-8, utf-16 or utf-32.
    # See: https://www.ietf.org/rfc/rfc4627.txt
    # Also: http://lucumr.pocoo.org/2013/7/19/application-mimetypes-and-encodings/
    charset = None

    def get_indent(self, accepted_media_type, renderer_context):
        if accepted_media_type:
            # If the media type looks like 'application/json; indent=4',
            # then pretty print the result.
            # Note that we coerce `indent=0` into `indent=None`.
            base_media_type, params = parse_header(accepted_media_type.encode('ascii'))
            try:
                return zero_as_none(max(min(int(params['indent']), 8), 0))
            except (KeyError, ValueError, TypeError):
                pass

        # If 'indent' is provided in the context, then pretty print the result.
        # E.g. If we're being called by the BrowsableAPIRenderer.
        return renderer_context.get('indent', None)

    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        Render `data` into JSON, returning a bytestring.
        """
        if data is None:
            return bytes()

        ret = orjson.dumps(
            data, 
            default=self.encoder_class,
            option=orjson.OPT_SERIALIZE_UUID | \
                orjson.OPT_SERIALIZE_NUMPY | \
                orjson.OPT_OMIT_MICROSECONDS | \
                orjson.OPT_NON_STR_KEYS,
        )

        # We always fully escape \u2028 and \u2029 to ensure we output JSON
        # that is a strict javascript subset.
        # See: http://timelessrepo.com/json-isnt-a-javascript-subset
        ret = ret.replace('\u2028', '\\u2028').replace('\u2029', '\\u2029')
        return ret.encode()
