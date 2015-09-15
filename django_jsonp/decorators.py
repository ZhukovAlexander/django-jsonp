from functools import wraps
import types

from django.views.decorators.http import require_GET
from django.views.generic import View
from django_jsonp.response import get_jsonp_response

from utils import get_callback


def jsonp(view):
    if isinstance(view, types.FunctionType):
        @require_GET
        @wraps(view)
        def jsonpfied_view(request, *args, **kwargs):

            return get_jsonp_response(view(request, *args, **kwargs), callback=get_callback(request))
        return jsonpfied_view

    elif issubclass(view, View):
        class JSONPfiedCBV(view):
            http_method_names = ['get']  # only GET method is allowed for JSONP

            def get(self, request, *args, **kwargs):
                return get_jsonp_response(
                    super(JSONPfiedCBV, self).get(request, *args, **kwargs),
                    callback=get_callback(request))

        return JSONPfiedCBV
    else:
        raise NotImplementedError('Only django CBVs and FBVs are supported')