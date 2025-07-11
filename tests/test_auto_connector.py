import unittest
from agents import auto_connector

class AutoConnectorTest(unittest.TestCase):
    def test_parse_extracts_email(self):
        msg = "Pripoj se na IMAP e-mail jiri@firma.cz server mail.firma.cz port 993 SSL heslo je tajne123"
        cfg = auto_connector.parse_connection_request(msg)
        self.assertEqual(cfg.get("user"), "jiri@firma.cz")

if __name__ == '__main__':
    unittest.main()
