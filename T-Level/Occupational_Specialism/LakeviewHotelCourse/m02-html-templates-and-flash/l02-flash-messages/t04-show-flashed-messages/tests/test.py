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


class TestFlashDisplay(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_success_message_is_displayed(self):
        body = self.client.get("/flash-test", follow_redirects=True).get_data(as_text=True)
        self.assertIn("Flash works!", body)
        self.assertIn("alert-success", body)

    def test_error_category_is_used_for_the_class(self):
        body = self.client.get("/flash-error", follow_redirects=True).get_data(as_text=True)
        self.assertIn("Something went wrong", body)
        self.assertIn("alert-error", body)

    def test_message_disappears_after_one_view(self):
        self.client.get("/flash-test", follow_redirects=True)
        body = self.client.get("/").get_data(as_text=True)
        self.assertNotIn("Flash works!", body)


if __name__ == "__main__":
    unittest.main()
