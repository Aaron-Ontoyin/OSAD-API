import os
import unittest

from flask import Flask
from app import app


class AppTestCase(unittest.TestCase):
    def setUp(self):
        """
        Set up the test environment by creating an instance of the Flask app and a test client.
        """
        self.app = app.test_client()
        self.app.testing = True


    def test_flask_app_creation(self):
        """
        Test the creation of a Flask app.

        This function checks whether the 'app' object is an instance of the 'Flask' class.

        Parameters:
            None

        Returns:
            None
        """
        self.assertIsInstance(app, Flask)

    def test_app_configurations(self):
        """
        Test the application configurations.

        This function asserts that the `__name__` attribute of the `app` object is equal to "__main__".
        It also checks whether the `SQLALCHEMY_DATABASE_URI` and `JWT_SECRET_KEY` keys exist in the `app.config` dictionary.

        Parameters:
            self: The reference to the current instance of the test class.

        Returns:
            None
        """
        self.assertTrue(app.config["SQLALCHEMY_DATABASE_URI"])
        self.assertTrue(app.config["JWT_SECRET_KEY"])
        self.assertTrue(app.config["JWT_ACCESS_TOKEN_EXPIRES"])
        self.assertTrue(app.config["JWT_REFRESH_TOKEN_EXPIRES"])
        self.assertTrue(app.config["REDIS_URL"])
        self.assertTrue(app.config["SECRET_KEY"])
        self.assertTrue(app.config["SMTP_EMAIL_ADDRESS"])
        self.assertTrue(app.config["SMTP_EMAIL_PASSWORD"])
        

    def test_environment_variables(self):
        """
        A function to test the environment variables.
        """
        self.assertTrue(os.environ.get("JWT_SECRET_KEY"))
        self.assertTrue(os.environ.get("JWT_ACCESS_TOKEN_EXPIRES"))
        self.assertTrue(os.environ.get("JWT_REFRESH_TOKEN_EXPIRES"))
        self.assertTrue(os.environ.get("SQLALCHEMY_DATABASE_URI"))
        self.assertTrue(os.environ.get("REDIS_URL"))
        self.assertTrue(os.environ.get("SECRET_KEY"))
        self.assertTrue(os.environ.get("SMTP_EMAIL_ADDRESS"))
        self.assertTrue(os.environ.get("SMTP_EMAIL_PASSWORD"))

    def test_authentication_blueprint(self):
        """
        Test the authentication blueprint.

        This function tests whether the authentication blueprint is properly registered in the Flask app.
        It checks if the "auth" blueprint exists in the `app.blueprints` dictionary and if its name and class
        match the expected values.
        
        It also checks if the "object_detection" and "text_audio_processing" blueprints are properly registered.

        Returns:
            None
        """
        self.assertIn("auth", app.blueprints)
        self.assertEqual(app.blueprints["auth"].name, "auth")
        self.assertEqual(app.blueprints["auth"].__class__.__name__, "Blueprint")
        self.assertIn("object_detection", app.blueprints)
        self.assertEqual(
            app.blueprints["object_detection"].name, "object_detection"
        )
        self.assertEqual(
            app.blueprints["object_detection"].__class__.__name__, "Blueprint"
        )
        self.assertIn("text_audio_processing", app.blueprints)
        self.assertEqual(
            app.blueprints["text_audio_processing"].name, "text_audio_processing"
        )
        self.assertEqual(
            app.blueprints["text_audio_processing"].__class__.__name__, "Blueprint"
        )


if __name__ == "__main__":
    unittest.main()
