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
from helpers import add_booking, cleanup, login, make_client


class TestMyBookings(unittest.TestCase):
    def setUp(self):
        self.client, self.path = make_client()
        add_booking(1, 1, "2026-12-01", "2026-12-03", 1, 160.0)
        add_booking(1, 1, "2026-11-01", "2026-11-04", 1, 240.0)
        add_booking(2, 4, "2026-11-10", "2026-11-12", 3, 360.0)

    def tearDown(self):
        cleanup(self.path)

    def test_anonymous_users_are_redirected(self):
        self.assertEqual(302, self.client.get("/my-bookings").status_code)

    def test_only_my_bookings_are_shown(self):
        login(self.client, 1)
        body = self.client.get("/my-bookings").get_data(as_text=True)
        self.assertIn("2026-11-01", body)
        self.assertIn("2026-12-01", body)
        self.assertNotIn("2026-11-10", body, msg="Filter by the logged-in user's id")

    def test_sorted_by_check_in(self):
        login(self.client, 1)
        body = self.client.get("/my-bookings").get_data(as_text=True)
        self.assertLess(body.index("2026-11-01"), body.index("2026-12-01"))

    def test_room_details_come_from_the_join(self):
        login(self.client, 1)
        body = self.client.get("/my-bookings").get_data(as_text=True)
        self.assertIn("101 (Single)", body)
        self.assertIn("£240.00", body)

    def test_no_bookings_message(self):
        login(self.client, 2)
        from helpers import execute
        execute("DELETE FROM bookings WHERE user_id = 2")
        self.assertIn("no bookings yet", self.client.get("/my-bookings").get_data(as_text=True))


if __name__ == "__main__":
    unittest.main()
