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
import re
import sys
import cgi


page_header = """
<!DOCTYPE html>
<html>
<head>
<style content_type="text/css">
    form {
    display: block;
    }
    body {
    display: block;
    margin: 8px;
    }
    span {
    color: red;
    }
</style>
<title>User-Signup</title>
</head>
<body>
"""

page_form = """
<h2>Signup</h2>
<form method="post">
<table>
<tr>
<td><label for="username">Userame:</label></td>
<td><input type="text" name="username" autofocus="on" value="%(username)s" required></td>
<td><span>%(username_error)s</span></td>
</tr>
<tr>
<td><label for="password">Password:</label></td>
<td><input type="password" name="password" value="" required></td>
<td><span>%(password_error)s</span></td>
</tr>
<tr>
<td><label for="verify">Verify Password:</td>
<td><input type="password" name="verify" value="" required></td>
<td><span>%(verify_password_error)s</span></td>
</tr>
<tr>
<td><label for="email">Email:</td>
<td><input type="text" name="email" value="%(email)s"></td>
<td><span>%(email_error)s</span></td>
</tr>
</table>
<input type="submit">
</form>
"""

page_footer = """
</body>
</html>
"""

class MainHandler(webapp2.RequestHandler):

    def write_form(self, email_error="",
                         email="",
                         verify_password_error="",
                         password_error="",
                         username_error="",
                         username=""):

        form_contents = {'email_error': email_error,
                         'email': email,
                         'verify_password_error': verify_password_error,
                         'password_error': password_error,
                         'username_error': username_error,
                         'username': username
                        }
        content = page_header + (page_form % form_contents) + page_footer
        self.response.write(content)

    def get(self):
        self.write_form(email_error="", email="",
                   verify_password_error="", password_error="",
                   username_error="", username="")

    def post(self):

        username = self.request.get('username')
        username = cgi.escape(username)
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        def verify_username(username):
            USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
            return USER_RE.match(username)

        def verify_password(password):
            USER_PASS = re.compile(r"^.{3,20}$")
            return USER_PASS.match(password)

        def verify_email(email):
            if email == "":
                pass
            else:
                USER_EMAIL = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
                return USER_EMAIL.match(email)

        if (verify_username(username) and verify_password(password) and \
            verify_password(verify) and  password == verify and \
            (verify_email(email) or email == "")):
            self.redirect("/welcome?username=" + username)
        else:
            if not verify_username(username):
                username_error = "Invalid Username"
            else:
                username_error = ""
            if not verify_password(password):
                password_error = "Invalid Password"
            else:
                password_error = ""
            if not password == verify:
                verify_password_error = "Passwords Do Not Match"
            else:
                verify_password_error = ""
            if email == "":
                email_error = ""
            else:
                if not verify_email(email):
                    email_error = "Invalid Email"
                else:
                    email_error = ""

            self.write_form(username=username,
                username_error=username_error,
                password_error=password_error,
                verify_password_error=verify_password_error,
                email=email,
                email_error=email_error)

class WelcomeHandler(webapp2.RequestHandler):

    def get(self):
        username = self.request.get('username')
        self.response.out.write("Welcome, %s!" %username)


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome', WelcomeHandler),
],debug=True)
