import unittest
import os
import tempfile
from unittest import mock
from agents import auto_connector

class AutoConnectorTest(unittest.TestCase):
    def setUp(self):
        self.orig_cwd = os.getcwd()
        self.tmpdir = tempfile.TemporaryDirectory()
        os.chdir(self.tmpdir.name)

    def tearDown(self):
        os.chdir(self.orig_cwd)
        self.tmpdir.cleanup()

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
        with mock.patch("agents.email_agent.connect", return_value="ok"):
            auto_connector.handle_message(msg)
        self.assertTrue(os.path.exists(path))

    def test_invalid_server_name(self):
        msg = (
            "Pripoj se na IMAP e-mail test@firma.cz "
            "server invalid_server port 993 SSL heslo je tajne123"
        )
        cfg = auto_connector.parse_connection_request(msg)
        self.assertIsNone(cfg.get("server"))

    def test_invalid_port(self):
        msg = (
            "Pripoj se na IMAP e-mail test@firma.cz "
            "server mail.example.com port 99999 SSL heslo je tajne123"
        )
        cfg = auto_connector.parse_connection_request(msg)
        self.assertEqual(cfg.get("port"), 993)

    def test_calendar_request_calls_list_events(self):
        msg = "Zobraz kalendar"
        m = mock.Mock(return_value=["ok"])
        with mock.patch.dict(auto_connector.SERVICE_REGISTRY, {"calendar": m}):
            result = auto_connector.handle_message(msg)
        self.assertEqual(result, ["ok"])
        m.assert_called_once_with({"type": "calendar"})

if __name__ == '__main__':
    unittest.main()
