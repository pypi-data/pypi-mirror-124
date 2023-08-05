# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division, print_function, absolute_import
import os

from ...compat import *
from .. import BaseServer
#from ...http import Host
#from ...decorators import property
#from ...utils import ByteString, String
from ... import environ


class Application(BaseServer):
#     def __init__(self, *args, **kwargs):
#         pout.v(args, kwargs)
#         super().__init__(*args, **kwargs)

    async def __call__(self, scope, receive, send):
        """this is what will be called for each request that that ASGI server handles"""
        pout.v(scope, receive, send)
        c = self.create_call(raw_request)
        res = c.handle()
        return self.handle_web_response(raw_request)

    def handle_web_response(self, raw_request):
        c = self.create_call(raw_request)
        res = c.handle()
        self.create_response_body(res)

        def resp(*args, **kwargs):
            pout.v(args, kwargs)
        return resp

    def create_request(self, raw_request, **kwargs):
        """
        create instance of request

        raw_request -- the raw request object retrieved from a WSGI server
        """
        r = self.request_class()
        for header_name, header_value in raw_request.get("headers", {}):
            r.set_header(header_name, header_value)

        r.method = raw_request['method']
        r.path = raw_request['path']
        r.query = raw_request['query_string']

        # handle headers not prefixed with http
#         for k in ['CONTENT_TYPE', 'CONTENT_LENGTH']:
#             v = r.environ.pop(k, None)
#             if v:
#                 r.set_header(k, v)

        self.create_request_body(r, raw_request, **kwargs)
        r.raw_request = raw_request
        return r

    def create_request_body(self, request, raw_request, **kwargs):
        body_args = []
        body_kwargs = {}
        body = None
#         if 'wsgi.input' in raw_request:
#             body = raw_request['wsgi.input']
#             body = request.create_body(raw_request['wsgi.input'])
#             body_kwargs = body.kwargs
#             body_args = body.args

        request.body_args = body_args
        request.body_kwargs = body_kwargs
        request.body = body
        return request

    def create_backend(self, **kwargs):
        raise NotImplementedError()

    def handle_request(self):
        raise NotImplementedError()

    def serve_forever(self):
        raise NotImplementedError()

    def serve_count(self, count):
        raise NotImplementedError()

