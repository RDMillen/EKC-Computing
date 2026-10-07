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


class TestInheritance(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_nav_links_on_every_page(self):
        for path in ("/", "/rooms"):
            body = self.client.get(path).get_data(as_text=True)
            self.assertIn("<nav>", body)
            self.assertIn('href="/"', body, msg="Home link missing on %s" % path)
            self.assertIn('href="/rooms"', body, msg="Rooms link missing on %s" % path)

    def test_child_content_is_inserted(self):
        body = self.client.get("/rooms").get_data(as_text=True)
        self.assertIn("Room 101", body, msg="Define {% block content %} so child pages can fill it")
        self.assertIn("Room 201", body)

    def test_home_content(self):
        body = self.client.get("/").get_data(as_text=True)
        self.assertIn("Welcome.", body)


if __name__ == "__main__":
    unittest.main()
