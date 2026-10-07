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
from html.parser import HTMLParser

from app import app


class Collector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.lang = None
        self.input_ids = []
        self.label_fors = []
        self.has_submit = False
        self.has_main = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "html":
            self.lang = attrs.get("lang")
        elif tag == "input" and attrs.get("type") != "hidden":
            self.input_ids.append(attrs.get("id"))
        elif tag == "label":
            self.label_fors.append(attrs.get("for"))
        elif tag == "button" and attrs.get("type", "submit") == "submit":
            self.has_submit = True
        elif tag == "main":
            self.has_main = True


class TestAccessibleForm(unittest.TestCase):
    def setUp(self):
        parser = Collector()
        parser.feed(app.test_client().get("/enquiry").get_data(as_text=True))
        self.page = parser

    def test_language(self):
        self.assertEqual("en", (self.page.lang or "").lower(), msg='Add lang="en" to the <html> tag')

    def test_two_inputs(self):
        self.assertGreaterEqual(len(self.page.input_ids), 2, msg="Add a name input and an email input")

    def test_every_input_has_a_label(self):
        for input_id in self.page.input_ids:
            self.assertIsNotNone(input_id, msg="Every input needs an id")
            self.assertIn(input_id, self.page.label_fors, msg="No <label for=...> for input '%s'" % input_id)

    def test_submit_button(self):
        self.assertTrue(self.page.has_submit, msg="Add a submit button")


if __name__ == "__main__":
    unittest.main()
