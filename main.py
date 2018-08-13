#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os

import webapp2
from google.appengine.ext.webapp import template

from webvision import get_emoji

TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), 'templates')


class MainHandler(webapp2.RequestHandler):
    def get(self):
        context = {}
        file = os.path.join(TEMPLATE_PATH, 'index.html')
        self.response.write(template.render(file, context))

    def post(self):
        img = self.request.POST.get('photo')
        url = self.request.POST.get('photo-url')

        context = {'result': '/static/'+get_emoji(url),
                   'img': url,
                   }
        file = os.path.join(TEMPLATE_PATH, 'index.html')

        self.response.write(template.render(file, context))


app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
