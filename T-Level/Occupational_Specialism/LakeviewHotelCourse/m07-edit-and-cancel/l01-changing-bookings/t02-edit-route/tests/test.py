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


class TestEditRoute(unittest.TestCase):
    def setUp(self):
        self.client, self.path = make_client()
        self.booking_id = add_booking(1, 1, "2026-11-01", "2026-11-04", 1, 240.0)
        login(self.client, 1)
        self.url = "/bookings/%d/edit" % self.booking_id

    def tearDown(self):
        cleanup(self.path)

    def row(self):
        return query("SELECT check_in, check_out, occupants, total_price FROM bookings WHERE id = ?", (self.booking_id,))[0]

    def test_anonymous_users_are_redirected(self):
        self.assertEqual(302, self.client.application.test_client().get(self.url).status_code)

    def test_form_is_prefilled(self):
        body = self.client.get(self.url).get_data(as_text=True)
        self.assertIn('value="2026-11-01"', body)
        self.assertIn('value="3"', body, msg="3 nights")

    def test_update_changes_dates_and_price(self):
        response = self.client.post(self.url, data={"check_in": "2026-11-02", "nights": "5", "occupants": "1"})
        self.assertEqual(302, response.status_code)
        self.assertTrue(response.headers["Location"].endswith("/bookings/%d" % self.booking_id))
        self.assertEqual(("2026-11-02", "2026-11-07", 1, 400.0), self.row())

    def test_success_message(self):
        body = self.client.post(self.url, data={"check_in": "2026-11-02", "nights": "5", "occupants": "1"},
                                follow_redirects=True).get_data(as_text=True)
        self.assertIn("Booking updated", body)

    def test_error_is_shown_and_nothing_changes(self):
        response = self.client.post(self.url, data={"check_in": "2026-11-02", "nights": "5", "occupants": "2"})
        self.assertEqual(200, response.status_code)
        self.assertIn("sleeps at most 1", response.get_data(as_text=True))
        self.assertEqual(("2026-11-01", "2026-11-04", 1, 240.0), self.row())

    def test_other_users_cannot_edit(self):
        other = self.client.application.test_client()
        login(other, 2)
        self.assertEqual(403, other.get(self.url).status_code)
        data = {"check_in": "2030-01-01", "nights": "1", "occupants": "1"}
        self.assertEqual(403, other.post(self.url, data=data).status_code)
        self.assertEqual(("2026-11-01", "2026-11-04", 1, 240.0), self.row())

    def test_missing_booking(self):
        self.assertEqual(404, self.client.get("/bookings/999/edit").status_code)


if __name__ == "__main__":
    unittest.main()
