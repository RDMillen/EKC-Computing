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
from helpers import cleanup, login, make_client, query


class TestBookRoute(unittest.TestCase):
    def setUp(self):
        self.client, self.path = make_client()
        login(self.client, 1)

    def tearDown(self):
        cleanup(self.path)

    def post(self, room_id=3, **changes):
        data = {"check_in": "2030-05-10", "nights": "3", "occupants": "2"}
        data.update(changes)
        return self.client.post("/book/%d" % room_id, data=data)

    def bookings(self):
        return query("SELECT user_id, room_id, check_in, check_out, occupants, total_price FROM bookings")

    def test_anonymous_users_are_redirected(self):
        anonymous = self.client.application.test_client()
        self.assertEqual(302, anonymous.get("/book/3").status_code)

    def test_form_is_shown(self):
        response = self.client.get("/book/3")
        self.assertEqual(200, response.status_code)
        self.assertIn("Book room 103", response.get_data(as_text=True))

    def test_missing_room(self):
        self.assertEqual(404, self.client.get("/book/999").status_code)

    def test_booking_is_saved_for_the_logged_in_user(self):
        response = self.post()
        self.assertEqual(302, response.status_code)
        self.assertRegex(response.headers["Location"], r"/bookings/\d+$")
        self.assertEqual([(1, 3, "2030-05-10", "2030-05-13", 2, 330.0)], self.bookings())

    def test_confirmation_page(self):
        location = self.post().headers["Location"]
        body = self.client.get(location).get_data(as_text=True)
        self.assertIn("103 (Double)", body)
        self.assertIn("2030-05-13", body)

    def test_success_message(self):
        body = self.client.post("/book/3", data={"check_in": "2030-05-10", "nights": "3", "occupants": "2"},
                                follow_redirects=True).get_data(as_text=True)
        self.assertIn("Booking confirmed", body)
        self.assertIn("£330.00", body)

    def test_extra_guests_are_priced(self):
        self.post(room_id=4, nights="2", occupants="4")
        self.assertEqual(400.0, self.bookings()[0][5])

    def test_too_many_guests(self):
        body = self.post(occupants="3").get_data(as_text=True)
        self.assertIn("sleeps at most 2", body)
        self.assertEqual([], self.bookings())

    def test_unavailable_room(self):
        body = self.post(room_id=2).get_data(as_text=True)
        self.assertIn("not available", body)
        self.assertEqual([], self.bookings())

    def test_bad_input_shows_a_message_not_a_crash(self):
        response = self.post(nights="abc")
        self.assertEqual(200, response.status_code)
        self.assertIn("Could not book", response.get_data(as_text=True))
        self.assertEqual([], self.bookings())

    def test_confirmation_is_private(self):
        location = self.post().headers["Location"]
        other = self.client.application.test_client()
        login(other, 2)
        self.assertEqual(403, other.get(location).status_code)


if __name__ == "__main__":
    unittest.main()
