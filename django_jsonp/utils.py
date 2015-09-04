APPLICATION_JS = 'application/javascript'

JSONP_TEMPLATE = u'{callback}({payload})'

JSONP = 'jsonp'
CALLBACK = 'callback'


def get_callback(request):
    return request.GET.get(CALLBACK, request.GET.get(JSONP, None))