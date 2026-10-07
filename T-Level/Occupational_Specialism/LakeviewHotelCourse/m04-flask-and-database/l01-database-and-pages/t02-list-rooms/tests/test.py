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
from helpers import cleanup, execute, make_client


class TestRoomsList(unittest.TestCase):
    def setUp(self):
        self.client, self.path = make_client()

    def tearDown(self):
        cleanup(self.path)

    def test_status(self):
        self.assertEqual(200, self.client.get("/rooms").status_code)

    def test_every_room_is_listed(self):
        body = self.client.get("/rooms").get_data(as_text=True)
        for number in ("101", "102", "103", "201", "312"):
            self.assertIn(number, body, msg="Room %s is missing from the page" % number)
        self.assertIn("£80.00", body)
        self.assertIn("Unavailable", body, msg="Room 102 is unavailable")

    def test_data_comes_from_the_database(self):
        execute("INSERT INTO rooms (number, room_type, capacity, price_per_night) VALUES (999, 'Loft', 2, 99.0)")
        body = self.client.get("/rooms").get_data(as_text=True)
        self.assertIn("999", body, msg="Query the rooms table instead of using a Python list")

    def test_sorted_by_room_number(self):
        execute("INSERT INTO rooms (number, room_type, capacity, price_per_night) VALUES (50, 'Loft', 2, 99.0)")
        body = self.client.get("/rooms").get_data(as_text=True)
        self.assertLess(body.index(">50<"), body.index(">101<"), msg="ORDER BY number")


if __name__ == "__main__":
    unittest.main()
