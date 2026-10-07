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
from helpers import cleanup, make_client, query

VALID = {"number": "401", "room_type": "Penthouse", "capacity": "4", "price_per_night": "399.50"}


class TestAddRoom(unittest.TestCase):
    def setUp(self):
        self.client, self.path = make_client()

    def tearDown(self):
        cleanup(self.path)

    def room_count(self):
        return query("SELECT COUNT(*) FROM rooms")[0][0]

    def test_form_is_shown(self):
        response = self.client.get("/rooms/new")
        self.assertEqual(200, response.status_code)
        self.assertIn("Add a room", response.get_data(as_text=True))

    def test_valid_room_is_saved_and_redirects(self):
        response = self.client.post("/rooms/new", data=VALID)
        self.assertEqual(302, response.status_code, msg="Redirect after a successful POST")
        self.assertTrue(response.headers["Location"].endswith("/rooms"))
        self.assertEqual([(401, "Penthouse", 4, 399.5)],
                         query("SELECT number, room_type, capacity, price_per_night FROM rooms WHERE number = 401"))

    def test_success_message(self):
        body = self.client.post("/rooms/new", data=VALID, follow_redirects=True).get_data(as_text=True)
        self.assertIn("Room added", body)
        self.assertIn("alert-success", body)

    def test_missing_fields(self):
        before = self.room_count()
        response = self.client.post("/rooms/new", data={"number": "401"})
        self.assertEqual(200, response.status_code)
        self.assertIn("Please fill in all fields", response.get_data(as_text=True))
        self.assertEqual(before, self.room_count())

    def test_invalid_numbers(self):
        before = self.room_count()
        data = dict(VALID, capacity="many")
        body = self.client.post("/rooms/new", data=data).get_data(as_text=True)
        self.assertIn("must be numbers", body)
        self.assertEqual(before, self.room_count())

    def test_duplicate_room_number(self):
        before = self.room_count()
        body = self.client.post("/rooms/new", data=dict(VALID, number="101")).get_data(as_text=True)
        self.assertIn("That room number already exists", body)
        self.assertEqual(before, self.room_count())

    def test_sql_in_a_field_is_just_text(self):
        nasty = "x'); DROP TABLE rooms;--"
        self.client.post("/rooms/new", data=dict(VALID, room_type=nasty))
        self.assertEqual([(nasty,)], query("SELECT room_type FROM rooms WHERE number = 401"),
                         msg="Use ? parameters so this is stored as plain text")


if __name__ == "__main__":
    unittest.main()
