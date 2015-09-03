import json

from django.http.response import HttpResponse, HttpResponseNotAllowed, HttpResponseBadRequest
from django.test import TestCase
from django.test.client import RequestFactory
from django.views.generic import View
from django_jsonp import jsonp

from django_jsonp.decorators import APPLICATION_JS


class FBVTestCase(TestCase):

    def setUp(self):

        self.factory = RequestFactory()
        self.dict_response = dict(foo='bar')

        @jsonp
        def simple_dict_view(request):
            return self.dict_response

        @jsonp
        def simple_http_response_view(request):
            return HttpResponse(json.dumps(self.dict_response))

        self.simple_dict_view = simple_dict_view
        self.simple_http_response_view = simple_http_response_view

    def assert_content_and_content_type(self, response, callback):
        self.assertEqual(response.content, '{0}({1})'.format(callback, json.dumps(self.dict_response)))
        self.assertEqual(response['Content-Type'], APPLICATION_JS)

    def test_response_correct_format_from_dict(self):
        callback = 'showMeTheMoney'
        request = self.factory.get('/fake.json?callback={0}'.format(callback))
        response = self.simple_dict_view(request)
        self.assertEqual(response.content, '{0}({1})'.format(callback, json.dumps(self.dict_response)))
        self.assertEqual(response['Content-Type'], APPLICATION_JS)

    def test_response_correct_from_http_response(self):
        callback = 'whatsMyAgeAgain'
        response = self.simple_http_response_view(self.factory.get('/fake.json?callback={0}'.format(callback)))
        self.assert_content_and_content_type(response, callback)

    def test_with_different_callback_param_name(self):
        callback = 'giveMeNovocaine'
        response = self.simple_http_response_view(request=self.factory.get('/fake.json?jsonp={0}'.format(callback)))
        self.assert_content_and_content_type(response, callback)


class CBVTestCase(TestCase):
    def setUp(self):

        self.factory = RequestFactory()
        dict_response = dict(foo='bar')
        self.dict_response = dict_response

        @jsonp
        class DictResponse(View):
            def get(self, request):
                return dict_response

        @jsonp
        class InvalidResponseFormat(View):
            def get(self, request):
                return []

        self.simple_dict_view = DictResponse.as_view()
        self.invalid_view = InvalidResponseFormat.as_view()

    def assert_content_and_content_type(self, response, callback):
        self.assertEqual(response.content, '{0}({1})'.format(callback, json.dumps(self.dict_response)))
        self.assertEqual(response['Content-Type'], APPLICATION_JS)

    def test_correct_response(self):
        callback = 'isThereASpoon'
        response = self.simple_dict_view(request=self.factory.get('/fake.json?jsonp={0}'.format(callback)))
        self.assert_content_and_content_type(response, callback)

    def test_method_not_allowed(self):
        callback = 'isThereASpoon'
        put_response = self.simple_dict_view(request=self.factory.put('/fake.json?jsonp={0}'.format(callback)))
        post_response = self.simple_dict_view(request=self.factory.post('/fake.json?jsonp={0}'.format(callback)))
        delete_response = self.simple_dict_view(request=self.factory.delete('/fake.json?jsonp={0}'.format(callback)))
        for r in [put_response, post_response, delete_response]:
            self.assertIsInstance(r, HttpResponseNotAllowed)

    def test_invalid_response_format(self):
        callback = 'howMuchIsTheFish'
        self.assertRaises(NotImplementedError,
                          lambda: self.invalid_view(request=self.factory.get('/fake.json?jsonp={0}'.format(callback))))

    def test_no_callback(self):
        response = self.simple_dict_view(request=self.factory.get('/fake.json?'))
        self.assertIsInstance(response, HttpResponseBadRequest)
