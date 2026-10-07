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


class TestProfile(unittest.TestCase):
    def setUp(self):
        self.client, self.path = make_client()
        login(self.client, 1)

    def tearDown(self):
        cleanup(self.path)

    def user(self, user_id):
        return query("SELECT name, email FROM users WHERE id = ?", (user_id,))[0]

    def test_anonymous_users_are_redirected(self):
        anonymous = self.client.application.test_client()
        response = anonymous.get("/profile")
        self.assertEqual(302, response.status_code)

    def test_form_shows_current_details(self):
        body = self.client.get("/profile").get_data(as_text=True)
        self.assertIn("James Sunderland", body)
        self.assertIn("james@example.com", body)

    def test_update_name_and_email(self):
        response = self.client.post("/profile", data={"name": "James King", "email": "James.King@example.com"})
        self.assertEqual(302, response.status_code)
        self.assertEqual(("James King", "james.king@example.com"), self.user(1))
        self.assertEqual(("Mary Sunderland", "mary@example.com"), self.user(2), msg="Only the logged-in user changes")

    def test_success_message(self):
        body = self.client.post("/profile", data={"name": "James King", "email": "james@example.com"},
                                follow_redirects=True).get_data(as_text=True)
        self.assertIn("Profile updated", body)

    def test_email_belonging_to_someone_else(self):
        body = self.client.post("/profile", data={"name": "James", "email": "mary@example.com"}).get_data(as_text=True)
        self.assertIn("That email is already registered", body)
        self.assertEqual(("James Sunderland", "james@example.com"), self.user(1))

    def test_empty_fields(self):
        body = self.client.post("/profile", data={"name": "", "email": "a@b.com"}).get_data(as_text=True)
        self.assertIn("Please fill in all fields", body)
        self.assertEqual(("James Sunderland", "james@example.com"), self.user(1))


if __name__ == "__main__":
    unittest.main()
