import os
from datetime import timedelta, datetime

import unittest

from blueprints.object_detection.models import Image
from blueprints.auth.models import User
from utils import db
from app import app
from settings import Config


class ImageModelTestCase(unittest.TestCase):
    """
    Class to test the User model.
    """

    def setUp(self):
        """
        Set up the test environment.
        """
        self.app = app
        self.app.testing = True
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        """
        Tear down the test environment.
        """
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_image(self):
        """
        Test the creation of an Image data in db.
        """
        url = os.path.join(
            Config.BASE_URL, "blueprints/object_detection/static/images/test.jpg"
        )
        user = User(username="testuser", email="test@example.com", password="password")
        db.session.add(user)
        user = User.query.filter_by(username="testuser").first()
        image = Image(
            user_id=user.id,
            detected_as="test",
            description="test description",
            url=url,
        )
        db.session.add(image)
        inserted_image = Image.query.filter_by(user_id=user.id).first()
        self.assertEqual(inserted_image.user_id, 1)
        self.assertEqual(inserted_image.detected_as, "test")
        self.assertEqual(inserted_image.description, "test description")
        self.assertEqual(inserted_image.url, url)
        self.assertIsInstance(inserted_image.id, type(0))
        # Test Auto date created
        self.assertAlmostEqual(
            inserted_image.detected_on, datetime.now(), delta=timedelta(seconds=5)
        )


if __name__ == "__main__":
    unittest.main()
