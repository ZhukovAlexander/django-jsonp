from functools import wraps
import types
import json

from django.http.response import HttpResponse, HttpResponseBadRequest
from django.views.decorators.http import require_GET
from django.views.generic import View


APPLICATION_JS = 'application/javascript'
JSONP = 'jsonp'
CALLBACK = 'callback'

JSONP_TEMPLATE = u'{callback}({payload})'

def get_callback(request):
    return request.GET.get(CALLBACK, request.GET.get(JSONP, None))


def jsonp_response(response, callback=None):
    if not callback:
        return HttpResponseBadRequest('No callback supplied')

    if isinstance(response, dict):
        return HttpResponse(content=JSONP_TEMPLATE.format(callback=callback, payload=json.dumps(response)),
                            content_type=APPLICATION_JS)
    elif isinstance(response, HttpResponse):
        response.content = JSONP_TEMPLATE.format(callback=callback, payload=response.content)
        response['Content-Type'] = APPLICATION_JS
        return response
    else:
        raise NotImplementedError('Not supported response value')


def jsonp(view):
    if isinstance(view, types.FunctionType):
        @require_GET
        @wraps(view)
        def jsonpfied_view(request, *args, **kwargs):

            return jsonp_response(view(request, *args, **kwargs), callback=get_callback(request))
        return jsonpfied_view

    elif issubclass(view, View):
        class JSONPfiedCBV(view):
            http_method_names = ['get']  # only GET method is allowed for JSONP

            def get(self, request, *args, **kwargs):
                return jsonp_response(
                    super(JSONPfiedCBV, self).get(request, *args, **kwargs),
                    callback=get_callback(request))

        return JSONPfiedCBV
    else:
        raise NotImplementedError('Only django CBVs and FBVs are supported')