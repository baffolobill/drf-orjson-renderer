Django Rest Framework ORJSON Renderer
==================

[![Build Status](https://travis-ci.org/baffolobill/drf-orjson-renderer.png?branch=master)](https://travis-ci.org/baffolobill/drf-orjson-renderer)

Django Rest Framework renderer using [orjson](https://github.com/ijl/orjson)

## Installation

`pip install git+https://github.com/baffolobill/drf-orjson-renderer.git`

You can then set the `ORJSONRenderer` class as your default renderer in your `settings.py`

```python
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'drf_orjson.renderers.ORJSONRenderer',
    ),
    ...
}
```

Also you can set the `ORJSONParser` class as your default parser in your `settings.py`

```python
REST_FRAMEWORK = {
    'DEFAULT_PARSER_CLASSES': (
        'drf_orjson.parsers.ORJSONParser',
    ),
    ...
}
```
