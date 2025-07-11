import unittest
import os
from unittest import mock
from agents import auto_connector

class AutoConnectorTest(unittest.TestCase):
    def test_parse_extracts_email(self):
        msg = "Pripoj se na IMAP e-mail jiri@firma.cz server mail.firma.cz port 993 SSL heslo je tajne123"
        cfg = auto_connector.parse_connection_request(msg)
        self.assertEqual(cfg.get("user"), "jiri@firma.cz")

    def test_handle_message_creates_file(self):
        msg = (
            "Pripoj se na IMAP e-mail test@firma.cz "
            "server mail.example.com port 993 SSL heslo je tajne123"
        )
        path = "config/connections.json"
        if os.path.exists(path):
            os.remove(path)
        with mock.patch("agents.email_agent.connect", return_value="ok"):
            auto_connector.handle_message(msg)
        self.assertTrue(os.path.exists(path))

if __name__ == '__main__':
    unittest.main()
