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
from helpers import add_booking, cleanup, login, make_client, query


class TestCancel(unittest.TestCase):
    def setUp(self):
        self.client, self.path = make_client()
        self.mine = add_booking(1, 1, "2026-11-01", "2026-11-04", 1, 240.0)
        self.theirs = add_booking(2, 4, "2026-11-10", "2026-11-12", 3, 360.0)
        login(self.client, 1)

    def tearDown(self):
        cleanup(self.path)

    def ids(self):
        return [r[0] for r in query("SELECT id FROM bookings ORDER BY id")]

    def test_cancel_own_booking(self):
        response = self.client.post("/bookings/%d/cancel" % self.mine)
        self.assertEqual(302, response.status_code)
        self.assertTrue(response.headers["Location"].endswith("/my-bookings"))
        self.assertEqual([self.theirs], self.ids())

    def test_message(self):
        body = self.client.post("/bookings/%d/cancel" % self.mine, follow_redirects=True).get_data(as_text=True)
        self.assertIn("Booking cancelled", body)

    def test_cannot_cancel_someone_elses_booking(self):
        self.assertEqual(403, self.client.post("/bookings/%d/cancel" % self.theirs).status_code)
        self.assertEqual([self.mine, self.theirs], self.ids())

    def test_get_is_not_allowed(self):
        self.assertEqual(405, self.client.get("/bookings/%d/cancel" % self.mine).status_code)
        self.assertEqual([self.mine, self.theirs], self.ids())

    def test_missing_booking(self):
        self.assertEqual(404, self.client.post("/bookings/999/cancel").status_code)

    def test_anonymous_users_are_redirected(self):
        anonymous = self.client.application.test_client()
        self.assertEqual(302, anonymous.post("/bookings/%d/cancel" % self.mine).status_code)
        self.assertEqual([self.mine, self.theirs], self.ids())


if __name__ == "__main__":
    unittest.main()
