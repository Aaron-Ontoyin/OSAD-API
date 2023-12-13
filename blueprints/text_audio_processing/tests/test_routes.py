import os
import unittest

from app import app
from utils import db


class ObjectDetectionBlueprintTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.testing = True
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # create test user for routes that require authentication
        payload = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword",
        }

        # Make a POST request to the register endpoint with the test data
        response = self.client.post("/auth/register", json=payload)
        # Assert that the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Login to get the access token and refresh token
        response = self.client.post("/auth/login", json=payload)

        # Assert that the response status code is 200
        self.assertEqual(response.status_code, 200)
        self.assertIn("access_token", response.json)
        self.assertIn("refresh_token", response.json)
        self.refresh_token = response.json["refresh_token"]
        self.access_token = response.json["access_token"]

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_process_text(self):
        response = self.client.post(
            "/tap/process-text",
            json={"text": "Hello, World!"},
            headers={"Authorization": f"Bearer {self.access_token}"},
        )
        self.assertEqual(response.status_code, 200)
        # It reurns a url for the audio
        self.assertIsInstance(response.json.get("audio_url"), str)

    def test_process_audio(self):
        response = self.client.post(
            "/tap/process-audio",
            json={"audio": "For now, it's text"},
            headers={"Authorization": f"Bearer {self.access_token}"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json.get("text_url"))
        self.assertIsInstance(response.json.get("text_url"), str)


if __name__ == "__main__":
    unittest.main()
