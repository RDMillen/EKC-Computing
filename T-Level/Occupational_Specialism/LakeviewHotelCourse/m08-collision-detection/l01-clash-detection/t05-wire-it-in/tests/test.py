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
from bookings import BookingConflict, create_booking, update_booking
from dbhelpers import make_db
from helpers import add_booking, cleanup, login, make_client, query


class TestFunctions(unittest.TestCase):
    def setUp(self):
        self.db = make_db()   # room 1: 1-4 Nov and 1-3 Dec 2026

    def count(self):
        return self.db.execute("SELECT COUNT(*) FROM bookings").fetchone()[0]

    def test_clashing_booking_is_refused(self):
        before = self.count()
        with self.assertRaises(BookingConflict) as ctx:
            create_booking(self.db, 2, 1, "2026-11-02", 1, 1)
        self.assertIn("Those dates are already booked", str(ctx.exception))
        self.assertEqual(before, self.count(), msg="A refused booking must not be saved")

    def test_conflict_is_a_value_error(self):
        self.assertTrue(issubclass(BookingConflict, ValueError))

    def test_back_to_back_booking_is_allowed(self):
        create_booking(self.db, 2, 1, "2026-11-04", 2, 1)
        self.assertEqual(4, self.count())

    def test_other_rooms_are_free(self):
        create_booking(self.db, 2, 3, "2026-11-02", 1, 1)

    def test_resaving_the_same_dates_is_not_a_clash(self):
        update_booking(self.db, 1, 1, "2026-11-01", 3, 1)

    def test_extending_your_own_stay_is_allowed(self):
        update_booking(self.db, 1, 1, "2026-11-01", 5, 1)
        self.assertEqual("2026-11-06", self.db.execute("SELECT check_out FROM bookings WHERE id = 1").fetchone()[0])

    def test_moving_onto_another_booking_is_refused(self):
        before = tuple(self.db.execute("SELECT * FROM bookings WHERE id = 1").fetchone())
        with self.assertRaises(BookingConflict):
            update_booking(self.db, 1, 1, "2026-11-30", 3, 1)   # ends 3 Dec: clashes with booking 3
        self.assertEqual(before, tuple(self.db.execute("SELECT * FROM bookings WHERE id = 1").fetchone()))


class TestRoutes(unittest.TestCase):
    def setUp(self):
        self.client, self.path = make_client()
        add_booking(1, 3, "2030-05-10", "2030-05-13", 1, 330.0)
        login(self.client, 2)

    def tearDown(self):
        cleanup(self.path)

    def book(self, check_in, nights):
        return self.client.post("/book/3", data={"check_in": check_in, "nights": str(nights), "occupants": "1"})

    def test_route_shows_the_message(self):
        response = self.book("2030-05-11", 1)
        self.assertEqual(200, response.status_code)
        self.assertIn("Those dates are already booked", response.get_data(as_text=True))
        self.assertEqual(1, query("SELECT COUNT(*) FROM bookings")[0][0])

    def test_route_allows_back_to_back(self):
        self.assertEqual(302, self.book("2030-05-13", 2).status_code)

    def test_edit_route_refuses_a_clash(self):
        mine = add_booking(2, 3, "2030-06-01", "2030-06-03", 1, 220.0)
        response = self.client.post("/bookings/%d/edit" % mine,
                                    data={"check_in": "2030-05-12", "nights": "3", "occupants": "1"})
        self.assertIn("Those dates are already booked", response.get_data(as_text=True))
        self.assertEqual("2030-06-01", query("SELECT check_in FROM bookings WHERE id = ?", (mine,))[0][0])


if __name__ == "__main__":
    unittest.main()
