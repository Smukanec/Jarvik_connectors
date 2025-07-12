import os
import json
import tempfile
import unittest
from datetime import datetime

from agents.calendar_agent import CalendarAgent


class CalendarAgentTest(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.orig_cwd = os.getcwd()
        os.chdir(self.tmpdir.name)

    def tearDown(self):
        os.chdir(self.orig_cwd)
        self.tmpdir.cleanup()

    def test_credentials_file_created(self):
        agent = CalendarAgent()
        agent.list_events()
        path = "config/calendar_credentials.json"
        self.assertTrue(os.path.exists(path))
        with open(path) as f:
            data = json.load(f)
        self.assertIn("token_path", data)

    def test_create_event_structure(self):
        agent = CalendarAgent()
        start = datetime(2024, 1, 1, 10, 0)
        result = agent.create_event("Meet", start, 30)
        self.assertEqual(result["title"], "Meet")
        self.assertEqual(result["start"], "2024-01-01 10:00")
        self.assertEqual(result["end"], "2024-01-01 10:30")
        self.assertEqual(result["status"], "created")


def load_tests(loader, tests, pattern):
    return unittest.TestSuite([
        loader.loadTestsFromTestCase(CalendarAgentTest),
    ])
