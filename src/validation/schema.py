#!/usr/bin/env python
#
# Copyright 2019 Rickard Armiento
#
# This file is part of a Python candidate reference implementation of
# the optimade API [https://www.optimade.org/]
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os, json

from openapi_core import create_spec
from openapi_core.shortcuts import ResponseValidator
from openapi_core.wrappers.mock import MockRequest, MockResponse

from .request import request, RequestError

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "openapi.json")) as f:
    spec_dict = json.load(f)

spec = create_spec(spec_dict)
validator = ResponseValidator(spec)

def schema_validate(request, response):
    result = validator.validate(request, response)
    # raise errors if response invalid
    result.raise_for_errors()

    # get list of errors
    errors = result.errors
    return result

def schema_validate_request(base_url, relurl):
    try:
        result = request(base_url+relurl)

        openapi_request = MockRequest(host_url=base_url, method="GET", path=relurl)
        openapi_response = MockResponse(data=result['raw_output'],status_code=result['code'])

        print "RAW OUTPUT",result['raw_output']
        
        return schema_validate(openapi_request, openapi_response)
    except RequestError as e:
        return {'error':str(e), 'warning':[], 'note':[]}

