import os
import unittest

from settings import Config

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

    def test_detect_image(self):
        """
        Test the detect image route.
        """
        # Test missing image
        response = self.client.post(
            "/object-detection/detect-image",
            headers={"Authorization": f"Bearer {self.access_token}"},
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json["msg"], "No image provided")
        # Test success
        test_img_path = os.path.join(os.path.dirname(__file__), "test_img.jpeg")
        with open(test_img_path, "rb") as image:
            files = {"image": (image, "test_img.jpeg")}
            response = self.client.post(
                "/object-detection/detect-image",
                data=files,
                headers={"Authorization": f"Bearer {self.access_token}"},
            )
            self.assertEqual(response.status_code, 200)
            detected_objs = response.json.get("detected_objs")
            self.assertEqual(detected_objs["detected_as"], ["bird"])
            self.assertEqual(detected_objs["description"], "1 object(s) detected in the image")

            self.assertIsNotNone(detected_objs)
            img_url = response.json.get("img_url")
            self.assertIsNotNone(img_url)


        # Check if image is uploaded and delete it. Might be auto deleted
        self.assertTrue(os.path.exists(img_url))
        # Just ensure the files are cleaned after testing
        os.remove(img_url)
        self.assertFalse(os.path.exists(img_url))

        # Simulate invalid image
        pass

    def test_get_images(self):
        """
        Test the get images route.
        """
        test_img_path = os.path.join(os.path.dirname(__file__), "test_img.png")
        with open(test_img_path, "rb") as image:
            files = {"image": (image, "test_img.jpeg")}
            response = self.client.post(
                "/object-detection/detect-image",
                data=files,
                headers={"Authorization": f"Bearer {self.access_token}"},
            )
            self.assertEqual(response.status_code, 200)
            img_url = response.json.get("img_url")
            self.assertTrue(os.path.exists(img_url))
            os.remove(img_url)
            self.assertFalse(os.path.exists(img_url))

        # Test success
        response = self.client.get(
            "/object-detection/images",
            headers={"Authorization": f"Bearer {self.access_token}"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json[0].get("detected_as"))
        self.assertIsNotNone(response.json[0].get("description"))
        self.assertEqual(response.json[0]["user_id"], 1)
        self.assertIsNotNone(response.json[0].get("url"))
        self.assertIsNotNone(response.json[0].get("detected_on"))
        self.assertTrue(response.json[0]["url"].startswith(Config.BASE_URL))

    def test_get_image(self):
        """
        Test the get image route.
        """
        test_img_path = os.path.join(os.path.dirname(__file__), "test_img.png")
        with open(test_img_path, "rb") as image:
            files = {"image": (image, "test_img.png")}
            response = self.client.post(
                "/object-detection/detect-image",
                data=files,
                headers={"Authorization": f"Bearer {self.access_token}"},
            )
            self.assertEqual(response.status_code, 200)
            img_url = response.json.get("img_url")
            self.assertTrue(os.path.exists(img_url))
            os.remove(img_url)
            self.assertFalse(os.path.exists(img_url))

        # Test success
        response = self.client.get(
            "/object-detection/image",
            json={"image_id": 1},
            headers={"Authorization": f"Bearer {self.access_token}"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json.get("detected_as"))
        self.assertIsNotNone(response.json.get("description"))
        self.assertEqual(response.json["user_id"], 1)
        self.assertIsNotNone(response.json.get("url"))
        self.assertTrue(response.json.get("url").startswith(Config.BASE_URL))

    def test_delete_image(self):
        """
        Test the delete image route.
        """
        test_img_path = os.path.join(os.path.dirname(__file__), "test_img.png")
        with open(test_img_path, "rb") as image:
            files = {"image": (image, "test_img.png")}
            response = self.client.post(
                "/object-detection/detect-image",
                data=files,
                headers={"Authorization": f"Bearer {self.access_token}"},
            )
            self.assertEqual(response.status_code, 200)
            img_url = response.json.get("img_url")
            self.assertTrue(os.path.exists(img_url))
            os.remove(img_url)
            self.assertFalse(os.path.exists(img_url))

        # Test success
        response = self.client.delete(
            "/object-detection/image",
            json={"image_id": 1},
            headers={"Authorization": f"Bearer {self.access_token}"},
        )
        self.assertEqual(response.status_code, 204)

        # Test invalid image
        response = self.client.delete(
            "/object-detection/image",
            json={"image_id": 1},
            headers={"Authorization": f"Bearer {self.access_token}"},
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json["msg"], "Image not found")


if __name__ == "__main__":
    unittest.main()
