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
        .error {
            color: red;
        }
    </style>
</head>
<body>
"""

# html boilerplate for the bottom of every page
page_footer = """
</body>
</html>
"""

class Index(webapp2.RequestHandler):
    """ Handles requests coming in to '/' (the root of our site)
"""


    def get(self):
        # a form for adding user info
        form = """
        <form method='post'>
            <table>
                <tr>
                    <td>
                    <label for="username">Username</label>
                    </td>
                    <td>
                        <input name="username" type="text" value="" required>
                        <span class="error"</span>
                    </td>

                </tr>
                <tr>
                    <td>
                    <label for="password">Password</label>
                    </td>
                    <td>
                        <input type="password" name="password" value="" required>
                    </td>

                </tr>
                <tr>
                    <td>
                    <label for="verify">Verify Password</label>
                    </td>
                    <td>
                        <input type="password" name="verify" required>
                        <span class="error"</span>
                    </td>

                </tr>
                <tr>
                    <td>
                    <label for="email">Email (optional)</label>
                    </td>
                    <td>
                        <input type="email" name="email" value="">
                        <span class="error"</span>
                    </td>

                </tr>
            </table>
            <input type="submit">
        </form>
        """

        header = "<h1>Signup</h1>"

        # if we have an error, make a <p> to display it
        error = self.request.get("error")
        error_element = "<p class='error'>" + error + "</p>" if error else ""

        # combine all the pieces to build the content of our response
        main_content = header + form + error_element
        content = page_header + main_content + page_footer
        self.response.write(content)

class SignUp(webapp2.RequestHandler):
    """Handles requests coming in to '/signup'
    """

    def post(self):
        # look inside the request to figure out what the user typed
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")

        #if the user typed a bad username, redirect and yell at them
        # if the user typed a bad password, redirect and yell at them
        # if the user's password and verify password do not match, redirect and yell at them
        #if the user typed a bad email, redirect and yell at them
        if condition:
            pass
        else:
            error = "Invalid username".format(username)
            error_escaped = cgi.escape(error, quote=True)
            self.redirect("/?error=" + error_escaped)








        # build response content
        edit_header = "<h3>Success!</h3>"
        welcome_msg = "Welcome, " + username + "!"
        content = page_header + "<p>" + welcome_msg + "</p>" + page_footer
        self.response.write(content)

app = webapp2.WSGIApplication([
    ('/', Index),
    ('/signup', SignUp)
], debug=True)
