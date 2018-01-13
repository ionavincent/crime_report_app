import datetime
import json
import unittest

from flask import Flask

from app import init_app
from database import db


class TimeEventsCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_app = Flask(__name__)
        init_app(cls.test_app, "testing")

    def setUp(self):
        self.app_context = self.test_app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.test_app.test_client()
        self.client.testing = True

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def add_test_event(self):
        event = {"name": "Amy's Birthday",
                 "type": "Party"}
        response = self.client.post("/events",
                                    data=json.dumps(event),
                                    content_type="application/json",
                                    charset="UTF-8")
        return response

    def test_get_events(self):
        self.add_test_event()
        response = self.client.get("/events/")
        self.assertEqual(len(json.loads(response.data)), 1)

        expected = {"current_time":
                        datetime.datetime.now().strftime("%B %d, %Y")}
        self.assertEqual(json.loads(response.data), expected)