# django-jsonp
Simple JSONP support for django 

[![Coverage Status](https://coveralls.io/repos/ZhukovAlexander/django-jsonp/badge.svg?branch=master&service=github)](https://coveralls.io/github/ZhukovAlexander/django-jsonp?branch=master)
[![Build Status](https://travis-ci.org/ZhukovAlexander/django-jsonp.svg)](https://travis-ci.org/ZhukovAlexander/django-jsonp)
[![PyPI version](https://badge.fury.io/py/django_jsonp.svg)](http://badge.fury.io/py/django_jsonp)
[![PyPI](https://img.shields.io/pypi/pyversions/django-jsonp.svg)](https://pypi.python.org/pypi/django-jsonp/)

## Installation

Install using `pip`...

```bash
$ pip install django-jsonp
```

## Usage

```python
from djsonp import jsonp, JSONPResponse, get_callback

# decorate something that returns a dict-like object
@jsonp
def my_view(request):
    return {'foo': 'bar'}
    

# it can work with an HttpResponse instances
@jsonp
def another_view(request):
    return HttpResponse("{'foo': 'bar'}")

# or just return a JSONPResponse
def jsonp_view(request):
    return JSONPResponse(data={'foo': 'bar', }, callback=get_callback(request))

# it also works for CBVs
from django.views.generic import View

@jsonp
class DictResponse(View):
    def get(self, request):
        return HttpResponse("{'foo': 'bar'}")
```
