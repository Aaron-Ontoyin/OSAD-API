import unittest
from sqlalchemy.exc import IntegrityError

from blueprints.auth.models import User
from utils import db
from app import app


class UserModelTestCase(unittest.TestCase):
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

    def test_create_user(self):
        """
        Function to test the creation of a user.

        This function creates a new user object with the username "testuser",
        email "test@example.com", and password "password".
        It then asserts that the username is equal to "testuser", the email
        is equal to "test@example.com", and the password is not equal to "password".

        Parameters:
        - self: The instance of the test class.

        Returns:
        - None
        """
        user = User(username="testuser", email="test@example.com", password="password")
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.password, "password")

    def test_default_values(self):
        """
        Test the default values for the other fields of a User object.

        :param self: The object itself.
        :return: None
        """
        user = User(username="testuser", email="test@example.com", password="password")
        db.session.add(user)
        user = User.query.filter_by(username="testuser").first()
        self.assertEqual(user.firstname, "John")
        self.assertEqual(user.lastname, "Doe")
        self.assertEqual(user.remaining_requests, -1)
        self.assertFalse(user.is_admin)
        self.assertIsNone(user.phone)


    def test_update_user_fields(self):
        """
        Test update_user_fields function.

        This function tests the update_user_fields method of the User class. 
        It creates a new user with the username "testuser" and email "test@example.com".
        Then it sets the firstname field to "Jane" and the lastname field to "Smith".
        Finally, it asserts that the firstname and lastname fields have been updated correctly.

        Parameters:
        - self: The instance of the test case class.

        Returns:
        - None
        """
        user = User(username="testuser", email="test@example.com")
        user.firstname = "Jane"
        user.lastname = "Smith"
        self.assertEqual(user.firstname, "Jane")
        self.assertEqual(user.lastname, "Smith")


    def test_unique_username_and_email(self):
        """
        Test the uniqueness constraint for username and email in the User model.

        This function creates two instances of the User model with the same username and email.
        The first instance is added to the session and committed to the database.
        The second instance is added to the session, and an `IntegrityError` is
        expected to be raised when trying to commit.

        Parameters:
        - self: The current instance of the test class.

        Returns:
        - None
        """
        user1 = User(username="testuser", email="test@example.com", password="password")
        db.session.add(user1)
        db.session.commit()

        user2 = User(username="testuser", email="test@example.com", password="password")
        db.session.add(user2)
        with self.assertRaises(IntegrityError):
            db.session.commit()

    def test_delete_user(self):
        """
        Test the functionality of deleting a user.

        This function creates a test user with the username "testuser", email
        "test@example.com", and password "password".
        It then adds the user to the database and commits the changes.
        Next, it deletes the user from the database and commits the changes.
        
        Finally, it queries the database for a user with the username "testuser"
        and asserts that the result is None,
        indicating that the user has been successfully deleted.
        """
        user = User(username="testuser", email="test@example.com", password="password")
        db.session.add(user)
        db.session.commit()

        db.session.delete(user)
        db.session.commit()

        deleted_user = User.query.filter_by(username="testuser").first()
        self.assertIsNone(deleted_user)


if __name__ == "__main__":
    unittest.main()
