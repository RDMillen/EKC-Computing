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
from app import app


class TestFlashRoute(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_redirects_home(self):
        response = self.client.get("/flash-test")
        self.assertEqual(302, response.status_code, msg="/flash-test should redirect")
        self.assertTrue(response.headers["Location"].endswith("/"))

    def test_message_is_in_the_session(self):
        self.client.get("/flash-test")
        with self.client.session_transaction() as sess:
            flashes = sess.get("_flashes", [])
        self.assertEqual([("success", "Flash works!")], [tuple(f) for f in flashes])


if __name__ == "__main__":
    unittest.main()
