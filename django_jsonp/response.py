from __future__ import absolute_import
import json

from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.http.response import HttpResponseBadRequest

from .utils import APPLICATION_JS, JSONP_TEMPLATE


class JSONPResponse(HttpResponse):
    def __init__(self, data, callback, encoder=DjangoJSONEncoder, safe=True, *args, **kwargs):
        if safe and not isinstance(data, dict):
            raise TypeError('In order to allow non-dict objects to be '
                            'serialized set the safe parameter to False')
        kwargs.setdefault('content_type', APPLICATION_JS)
        wrapped_payload = JSONP_TEMPLATE.format(
            callback=callback,
            # in case we got a string, for example when converting an HttpResponse instance
            payload=json.dumps(data, cls=encoder) if isinstance(data, dict) else data)
        super(JSONPResponse, self).__init__(content=wrapped_payload, **kwargs)

    @classmethod
    def from_http_response(cls, http_response, callback, *args, **kwargs):
        return cls(http_response.content, callback, safe=False,  *args, **kwargs)


def get_jsonp_response(data, callback=None):
    if not callback:
        return HttpResponseBadRequest('No callback supplied')
    if isinstance(data, dict):
        return JSONPResponse(data, callback)
    elif isinstance(data, HttpResponse):
        return JSONPResponse.from_http_response(data, callback)
    else:
        raise NotImplementedError('Not supported response type')