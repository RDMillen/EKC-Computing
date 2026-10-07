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
from helpers import cleanup, make_client


class TestRoomDetail(unittest.TestCase):
    def setUp(self):
        self.client, self.path = make_client()

    def tearDown(self):
        cleanup(self.path)

    def test_existing_room(self):
        response = self.client.get("/rooms/1")
        self.assertEqual(200, response.status_code)
        body = response.get_data(as_text=True)
        self.assertIn("Room 101", body)
        self.assertIn("Single", body)
        self.assertIn("£80.00", body)

    def test_available_room_has_booking_link(self):
        self.assertIn("/book/1", self.client.get("/rooms/1").get_data(as_text=True))

    def test_unavailable_room_has_no_booking_link(self):
        body = self.client.get("/rooms/2").get_data(as_text=True)
        self.assertIn("not available", body)
        self.assertNotIn("/book/2", body)

    def test_missing_room_is_404(self):
        self.assertEqual(404, self.client.get("/rooms/999").status_code)


if __name__ == "__main__":
    unittest.main()
