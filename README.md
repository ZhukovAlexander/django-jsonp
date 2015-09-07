# django-jsonp
Simple JSONP support for django 

[![Coverage Status](https://coveralls.io/repos/ZhukovAlexander/django-jsonp/badge.svg?branch=master&service=github)](https://coveralls.io/github/ZhukovAlexander/django-jsonp?branch=master)
[![Build Status](https://travis-ci.org/ZhukovAlexander/django-jsonp.svg)](https://travis-ci.org/ZhukovAlexander/django-jsonp)
## Installation

Install using `pip`...

```bash
$ pip install git+https://github.com/ZhukovAlexander/django-jsonp#egg=django_jsonp
```

## Usage

```python
from djsonp.decorators import jsonp
from djsonp.response import JSONPResponse
from djsonp.utils import get_callback

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
```
