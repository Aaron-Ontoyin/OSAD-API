import os
import unittest

from app import app
from utils import db
from blueprints.text_audio_processing.models import AudioText


class TextAudioBlueprintRoutesTestCase(unittest.TestCase):
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

        self.test_audio_path = os.path.join(os.path.dirname(__file__), "test_audio.m4a")
        with open(self.test_audio_path, "rb") as audio:
            files = {"audio": (audio, "test_audio.m4a")}
            self.process_audio_response = self.client.post(
                "/tap/process-audio",
                data=files,
                headers={"Authorization": f"Bearer {self.access_token}"},
            )

    def tearDown(self):
        audio_url = self.process_audio_response.json.get("audio_url")
        os.remove(audio_url)
    
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_process_text(self):
        response = self.client.post(
            "/tap/process-text",
            json={"text": "Hello, World! Vadmin Here! This is a test!"},
            headers={"Authorization": f"Bearer {self.access_token}"},
        )
        self.assertEqual(response.status_code, 200)
        # It reurns a url for the audio
        self.assertIsInstance(response.json.get("audio_url"), str)
        # Audio and text objects have been created
        audio_text = AudioText.query.filter_by(
            audio_url=response.json.get("audio_url")
        ).first()
        self.assertIsNotNone(audio_text)
        self.assertEqual(
            audio_text.text_value, "Hello, World! Vadmin Here! This is a test!"
        )
        # Clear test audio from static folder
        os.remove(response.json.get("audio_url"))

    def test_process_audio(self):
        response = self.process_audio_response # request made in setUp. Needed for other test
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json.get("text"))
        self.assertEqual(response.json.get("text"), "hello world test 1 2")
        audio_url = response.json.get("audio_url")
        audio_text = AudioText.query.filter_by(audio_url=audio_url).first()
        self.assertEqual(audio_text.text_value, "hello world test 1 2")
        self.assertTrue(os.path.exists(audio_url))
        
    def test_get_audio_text(self):
        response = self.client.get(
            "/tap/audio-text",
            json={"audio_text_id": 1},
            headers={"Authorization": f"Bearer {self.access_token}"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json.get("text"))
        self.assertIsNotNone(response.json.get("audio_url"))
        self.assertIsNotNone(response.json.get("processed_on"))

    def test_get_all_audio_texts(self):
        response = self.client.get(
            "/tap/audios-texts",
            headers={"Authorization": f"Bearer {self.access_token}"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json)
        self.assertIsInstance(response.json, list)
        self.assertEqual(len(response.json), 1)

    def test_delete_audio_text(self):
        response = self.client.delete(
            "/tap/audio-text",
            json={"audio_text_id": 1},
            headers={"Authorization": f"Bearer {self.access_token}"},
        )
        self.assertEqual(response.status_code, 204)
        # Unavailable audio text
        response = self.client.get(
            "/tap/audio-text",
            json={"audio_text_id": 1},
            headers={"Authorization": f"Bearer {self.access_token}"},
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json.get("msg"), "Audio text not found")


if __name__ == "__main__":
    unittest.main()
