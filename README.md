# django-shortuuid

![PyPI](https://img.shields.io/pypi/v/django-shortuuid?style=flat-square)
![PyPI - Implementation](https://img.shields.io/pypi/implementation/django-shortuuid?style=flat-square)
![GitHub License](https://img.shields.io/github/license/stabldev/django-shortuuid?style=flat-square)
![Build](https://img.shields.io/github/actions/workflow/status/stabldev/django-shortuuid/release.yml?style=flat-square)

A drop-in Django model field for generating short, URL-safe, and unique IDs using [shortuuid](https://github.com/skorokithakis/shortuuid).  
Customizable, migration-friendly, with optional collision detection and Django admin integration.

## Features

- Short, URL-safe unique IDs for Django models (default 22 characters, configurable)
- Customizable alphabet, prefix, and length
- Optional database collision detection and retry logic
- Django admin: field is read-only but visible
- Compatible with Django migrations
- Python type hints

## Installation

```
pip install django-shortuuid
```

## Usage

```py
from django.db import models
from django_shortuuid.fields import ShortUUIDField

class MyModel(models.Model):
    id = ShortUUIDField(primary_key=True, prefix="id-")
    # ... other fields ...
```

By default, `auto=True` generates a unique short UUID when each instance is saved, and makes the field read-only in forms/admin.

## Example

See [django_example/](django_example/) for a full Django setup and admin usage.

## Configuration

- `auto`: Generate and set value automatically (`True` by default)
- `length`: Length of the generated unique string (default `22`)
- `prefix`: Optional string prefix for the field value
- `alphabet`: Custom alphabet for uuid generation (default: `shortuuid`’s default)
- `collision_check`: Enables collision checking in the database (`True` by default)
- `max_retries`: Max attempts to generate unique value before error (`10` by default)

## License

[MIT](LICENSE) Copyright (c) [stabldev](https://github.com/stabldev)

## Credits

This project was inspired by [benrobster/django-shortuuidfield](https://github.com/benrobster/django-shortuuidfield)  
and builds on ideas from the original implementation.

Special thanks to [shortuuid](https://github.com/skorokithakis/shortuuid) for the short, URL-safe UUID generation.
