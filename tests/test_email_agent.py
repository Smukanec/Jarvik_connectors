import os
import json
import tempfile
import unittest
from unittest import mock

from agents import auto_connector, email_agent

class EmailAgentTest(unittest.TestCase):
    def setUp(self):
        self.orig_cwd = os.getcwd()
        self.tmpdir = tempfile.TemporaryDirectory()
        os.chdir(self.tmpdir.name)

    def tearDown(self):
        os.chdir(self.orig_cwd)
        self.tmpdir.cleanup()

    def _basic_config(self):
        return {
            "server": "mail.example.com",
            "port": 993,
            "user": "test@example.com",
            "password": "pwd",
            "ssl": True,
        }

    def test_unreachable_server(self):
        with mock.patch("imaplib.IMAP4_SSL", side_effect=Exception("unreachable")):
            result = email_agent.connect(self._basic_config())
        self.assertTrue(result["status"].startswith("exception:"))
        self.assertIsNone(result["mail_count"])

    def test_unauthorized_login(self):
        class FakeIMAP:
            def __init__(self, *a, **kw):
                pass
            def login(self, *a, **kw):
                raise email_agent.imaplib.IMAP4.error("auth failed")
        fake = FakeIMAP()
        with mock.patch("imaplib.IMAP4_SSL", return_value=fake):
            result = email_agent.connect(self._basic_config())
        self.assertTrue(result["status"].startswith("error:"))
        self.assertIsNone(result["mail_count"])

    def test_duplicate_account_overwrites(self):
        msg = (
            "Pripoj se na IMAP e-mail test@firma.cz "
            "server mail.example.com port 993 SSL heslo je tajne123"
        )
        path = "config/connections.json"
        with mock.patch("agents.email_agent.connect", return_value="ok") as m:
            auto_connector.handle_message(msg)
            with open(path) as f:
                first = json.load(f)
            auto_connector.handle_message(msg)
            with open(path) as f:
                second = json.load(f)
            self.assertEqual(m.call_count, 2)
        first.pop("password_id", None)
        second.pop("password_id", None)
        self.assertEqual(first, second)


def load_tests(loader, tests, pattern):
    return unittest.TestSuite([
        loader.loadTestsFromTestCase(EmailAgentTest),
    ])
