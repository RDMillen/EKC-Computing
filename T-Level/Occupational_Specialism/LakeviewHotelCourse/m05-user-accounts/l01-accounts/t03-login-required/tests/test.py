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
from helpers import cleanup, login, make_client


class TestLoginRequired(unittest.TestCase):
    def setUp(self):
        self.client, self.path = make_client()

    def tearDown(self):
        cleanup(self.path)

    def test_anonymous_user_is_redirected(self):
        response = self.client.get("/account")
        self.assertEqual(302, response.status_code)
        self.assertTrue(response.headers["Location"].endswith("/login"))

    def test_anonymous_user_sees_a_message(self):
        body = self.client.get("/account", follow_redirects=True).get_data(as_text=True)
        self.assertIn("Please log in first", body)

    def test_logged_in_user_gets_the_page(self):
        login(self.client, 1)
        response = self.client.get("/account")
        self.assertEqual(200, response.status_code)
        self.assertIn("James Sunderland", response.get_data(as_text=True))

    def test_the_view_keeps_its_name(self):
        import views
        self.assertEqual("account", views.account.__name__, msg="Use @functools.wraps(view)")


if __name__ == "__main__":
    unittest.main()
