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
import webapp2
import cgi

def build_page(textarea_content):
    username_label = "<label>Username </label>"
    username_input = "<input type='text' name='username' value=''/>"

    password_label = "<label>Password </label>"
    password_input = "<input type='password' name='password' value=''/>"

    verify_label = "<label>Verify Password </label>"
    verify_input = "<input type='password' name='verify' value=''/>"

    email_label = "<label>Email (optional) </label>"
    email_input = "<input type='email' name='email' value=''/>"

    submit = "<input type='submit'/>"
    form = ("<form method='post'>" +
            username_label + username_input + "<br>" +
            password_label + password_input + "<br>" +
            verify_label + verify_input + "<br>" +
            email_label + email_input + "<br>" +
            submit + "</form>")

    header = "<h2>Signup</h2>"

    return header + form


class MainHandler(webapp2.RequestHandler):
    def get(self):
        content = build_page("")
        self.response.write(content)

    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")
        escaped_username = cgi.escape(username)

        content = build_page(username + password + verify + email)
        self.response.write(content)

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
