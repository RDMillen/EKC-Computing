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
from werkzeug.security import check_password_hash

from helpers import cleanup, make_client, query


class TestRegister(unittest.TestCase):
    def setUp(self):
        self.client, self.path = make_client()

    def tearDown(self):
        cleanup(self.path)

    def post(self, **fields):
        return self.client.post("/register", data=fields)

    def count(self):
        return query("SELECT COUNT(*) FROM users")[0][0]

    def test_form_is_shown(self):
        self.assertEqual(200, self.client.get("/register").status_code)

    def test_successful_registration(self):
        response = self.post(name="Maria", email="maria@example.com", password="correct-horse")
        self.assertEqual(302, response.status_code)
        self.assertTrue(response.headers["Location"].endswith("/login"))
        rows = query("SELECT name, email, password_hash FROM users WHERE email = ?", ("maria@example.com",))
        self.assertEqual(1, len(rows))
        stored = rows[0][2]
        self.assertNotEqual("correct-horse", stored, msg="Never store a plain-text password")
        self.assertTrue(check_password_hash(stored, "correct-horse"), msg="Store generate_password_hash(password)")

    def test_success_message(self):
        response = self.client.post("/register", follow_redirects=False,
                                    data=dict(name="Maria", email="maria@example.com", password="correct-horse"))
        with self.client.session_transaction() as sess:
            flashes = [tuple(f) for f in sess.get("_flashes", [])]
        self.assertIn(("success", "Registered successfully. Please log in."), flashes)

    def test_email_is_stored_in_lower_case(self):
        self.post(name="Maria", email="Maria@Example.COM", password="correct-horse")
        self.assertEqual([("maria@example.com",)], query("SELECT email FROM users WHERE name = 'Maria'"))

    def test_duplicate_email(self):
        before = self.count()
        body = self.post(name="Imposter", email="james@example.com", password="correct-horse").get_data(as_text=True)
        self.assertIn("That email is already registered", body)
        self.assertEqual(before, self.count())

    def test_missing_fields(self):
        before = self.count()
        body = self.post(name="Maria", email="", password="correct-horse").get_data(as_text=True)
        self.assertIn("Please fill in all fields", body)
        self.assertEqual(before, self.count())

    def test_short_password(self):
        before = self.count()
        body = self.post(name="Maria", email="maria@example.com", password="short").get_data(as_text=True)
        self.assertIn("Password must be at least 8 characters", body)
        self.assertEqual(before, self.count())


if __name__ == "__main__":
    unittest.main()
