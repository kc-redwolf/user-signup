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
import re

# html boilerplate for the top of every page
page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>User-Signup</title>
    <style type="text/css">
        .label {
        text-align: right
        }
        .error {
            color: red;
        }
    </style>
</head>
<body>
"""

form = """
    <form method='post'>
        <table>
            <tr>
                <td class="label">Username</td>
                <td><input type="text" name="username" value="{{username}}"></td>
                <td class="error">{{error_username}}</td>
            </tr>
            <tr>
                <td class="label">Password</td>
                <td><input type="password" name="password" value=""></td>
                <td class="error">{{error_password}}</td>
            </tr>
            <tr>
                <td class="label">Verify Password</td>
                <td><input type="password" name="verify" value=""></td>
                <td class="error">{{error_verify}}</td>
            </tr>
            <tr>
                <td class="label">Email (optional)</td>
                <td><input type="text" name="email" value="{{email}}"></td>
                <td class="error">{{error_email}}</td>
            </tr>
        </table>
        <input type="submit">
    </form>
"""

# html boilerplate for the bottom of every page
page_footer = """
</body>
</html>
"""

header = "<h1>Signup</h1>"

main_content = header + form
content = page_header + main_content + page_footer

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile("^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE = re.compile("^[\S]+@[\S]+\.[\S]+$")
def valid_email(email):
    return not email or EMAIL_RE.match(email)

def escape_html(s):
    return cgi.escape(s, quote = True)


class SignupPage(webapp2.RequestHandler):
    """Handles requests coming in to '/'
    """

    def get (self):
        self.response.write(content)

    def post(self):
        # look inside the request to figure out what the user typed
        have_error = False
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")

        params = dict(username=username, email=email)

        #if the user typed a bad username, redirect and yell at them
        # if the user typed a bad password, redirect and yell at them
        # if the user's password and verify password do not match, redirect and yell at them
        #if the user typed a bad email, redirect and yell at them
        if valid_username(username) and valid_password(password, verify) and valid_verify(password, verify) and valid_email(email):
            self.redirect('/success?username=' + username)
        else:
            if not valid_username(username):
                user_err = "Invalid username".format(username)
            if not valid_password(password, verify):
                password_err = "Invalid password".format(password)
            if not valid_verify(password, verify):
                verify_err = "Your passwords did not match".format(verify)
            if not valid_email(email):
                email_err = "Invalid email".format(email)

            self.response.out.write(content)


class Success(webapp2.RequestHandler):
    """Returns response for a successful Successful Signup"""
    def get(self):
        # build response content
        edit_header = "<h3>Success!</h3>"
        username = self.request.get("username")
        welcome_msg = "Welcome, " + username + "!"
        content = page_header + "<p>" + welcome_msg + "</p>" + page_footer
        self.response.out.write(content)

app = webapp2.WSGIApplication([
    ('/success', Success),
    ('/.*', SignupPage)
], debug=True)
