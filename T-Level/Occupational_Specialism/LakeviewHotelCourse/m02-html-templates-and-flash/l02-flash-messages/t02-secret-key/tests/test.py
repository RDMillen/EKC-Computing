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
import importlib


class TestSecretKey(unittest.TestCase):
    def tearDown(self):
        os.environ.pop("SECRET_KEY", None)

    def test_uses_environment_variable(self):
        os.environ["SECRET_KEY"] = "from-the-environment"
        import app as app_module
        importlib.reload(app_module)
        self.assertEqual("from-the-environment", app_module.app.config["SECRET_KEY"])

    def test_has_fallback(self):
        os.environ.pop("SECRET_KEY", None)
        import app as app_module
        importlib.reload(app_module)
        self.assertEqual("dev-only-change-me", app_module.app.config["SECRET_KEY"])


if __name__ == "__main__":
    unittest.main()
