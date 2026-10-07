import os
import sys
import unittest

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
sys.path.insert(0, os.path.dirname(_HERE))

# Keep failure messages short: never print a whole HTML page back at the student.
_original_assert_in = unittest.TestCase.assertIn
_original_assert_not_in = unittest.TestCase.assertNotIn



def _join(msg, hint):
    if not msg:
        return hint
    msg = str(msg).rstrip()
    return msg + (" " if msg.endswith((".", "!", "?", ":")) else ". ") + hint


def _short_assert_in(self, member, container, msg=None):
    if isinstance(container, str) and len(container) > 200:
        if member not in container:
            hint = "The page should contain %r, but it does not." % (member,)
            self.fail(_join(msg, hint))
    else:
        _original_assert_in(self, member, container, msg)


def _short_assert_not_in(self, member, container, msg=None):
    if isinstance(container, str) and len(container) > 200:
        if member in container:
            hint = "The page should not contain %r, but it does." % (member,)
            self.fail(_join(msg, hint))
    else:
        _original_assert_not_in(self, member, container, msg)


unittest.TestCase.assertIn = _short_assert_in
unittest.TestCase.assertNotIn = _short_assert_not_in
from helpers import PASSWORD, cleanup, login, make_client


class TestLogin(unittest.TestCase):
    def setUp(self):
        self.client, self.path = make_client()

    def tearDown(self):
        cleanup(self.path)

    def post(self, email, password):
        return self.client.post("/login", data={"email": email, "password": password})

    def session_user(self):
        with self.client.session_transaction() as sess:
            return sess.get("user_id")

    def test_form_is_shown(self):
        self.assertEqual(200, self.client.get("/login").status_code)

    def test_good_login(self):
        response = self.post("james@example.com", PASSWORD)
        self.assertEqual(302, response.status_code)
        self.assertTrue(response.headers["Location"].endswith("/rooms"))
        self.assertEqual(1, self.session_user(), msg="Store the user's id in session['user_id']")

    def test_welcome_message_and_navbar(self):
        body = self.client.post("/login", data={"email": "james@example.com", "password": PASSWORD},
                                follow_redirects=True).get_data(as_text=True)
        self.assertIn("Welcome back, James Sunderland", body)
        self.assertIn("Log out", body, msg="base.html shows Log out when g.user is set")

    def test_email_is_not_case_sensitive(self):
        self.assertEqual(302, self.post("JAMES@Example.com", PASSWORD).status_code)

    def test_wrong_password(self):
        response = self.post("james@example.com", "not-the-password")
        self.assertEqual(200, response.status_code)
        self.assertIn("Invalid email or password", response.get_data(as_text=True))
        self.assertIsNone(self.session_user())

    def test_unknown_email_gives_same_message(self):
        response = self.post("nobody@example.com", PASSWORD)
        self.assertIn("Invalid email or password", response.get_data(as_text=True))
        self.assertIsNone(self.session_user())

    def test_logout(self):
        login(self.client, 1)
        response = self.client.get("/logout")
        self.assertEqual(302, response.status_code)
        self.assertTrue(response.headers["Location"].endswith("/login"))
        self.assertIsNone(self.session_user(), msg="logout() must clear the session")

    def test_logout_message(self):
        login(self.client, 1)
        body = self.client.get("/logout", follow_redirects=True).get_data(as_text=True)
        self.assertIn("You have been logged out", body)


if __name__ == "__main__":
    unittest.main()
