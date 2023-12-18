import unittest

from blueprints.auth.models import User
from app import app
from utils import db


class AuthBlueprintTestCase(unittest.TestCase):
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

    def test_correct_register_route(self):
        """
        Test the registration route.
        This is already tested in the setUp method because it creates
        a test user for other routes that require authentication
        """
        pass

    def test_duplicate_user_name_register(self):
        """
        Test the registration with a username that already exists.
        """
        payload = {
            "username": "testuser",  # duplicate username
            "email": "test1@example.com",
            "password": "test1password",
        }
        response = self.client.post("/auth/register", json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json["message"], "Username or email already exists")

    def test_duplicate_email_register(self):
        """
        Test the registration with an email that already exists.
        """
        payload = {
            "username": "testuser1",
            "email": "test@example.com",  # duplicate email
            "password": "test1password",
        }
        response = self.client.post("/auth/register", json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json["message"], "Username or email already exists")

    def test_missing_fields_register(self):
        """
        Test the registration with missing fields.
        """
        # missing username
        payload = {
            "email": "test1@example.com",
            "password": "test1password",
        }
        response = self.client.post("/auth/register", json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json["message"], "Missing fields: username")

        # missing email
        payload = {
            "username": "testuser1",
            "password": "test1password",
        }
        response = self.client.post("/auth/register", json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json["message"], "Missing fields: email")

        # missing password
        payload = {
            "username": "testuser1",
            "email": "test1@example.com",
        }
        response = self.client.post("/auth/register", json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json["message"], "Missing fields: password")

    def test_correct_login_route(self):
        """
        Test the login route.
        This is already tested in the setUp method because it gets access
        and refresh tokens for other routes that require authentication
        """
        pass

    def test_incorrect_login_route(self):
        """
        Test the login route with incorrect credentials.
        """
        payload = {
            "username": "testuser",
            "password": "wrongpassword", # incorrect password
        }
        response = self.client.post("/auth/login", json=payload)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json["msg"], "Invalid password")

        payload = {
            "username": "testuser1", # incorrect username
            "password": "test1password", 
        }
        response = self.client.post("/auth/login", json=payload)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json["msg"], "Invalid username")

        payload = {
            "password": "test1password", # missing username
        }
        response = self.client.post("/auth/login", json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json["msg"], "Missing required fields")

        payload = {
            "username": "testuser1", # missing password
        }
        response = self.client.post("/auth/login", json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json["msg"], "Missing required fields")

    def test_logout(self):
        """
        Test the logout route.
        """
        response = self.client.delete("/auth/logout", headers={"Authorization": f"Bearer {self.refresh_token}"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["msg"], "Refresh token successfully revoked")

        response = self.client.delete("/auth/logout", headers={"Authorization": f"Bearer {self.access_token}"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["msg"], "Access token successfully revoked")

        # Test invalid tokens after revoking
        response = self.client.delete("/auth/logout", headers={"Authorization": f"Bearer {self.refresh_token}"})
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json["msg"], "Token has been revoked")

        response = self.client.delete("/auth/logout", headers={"Authorization": f"Bearer {self.access_token}"})
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json["msg"], "Token has been revoked")

    def test_invalid_token(self):
        """
        Test an invalid token.
        """
        # Bad token type
        response = self.client.delete("/auth/logout", headers={"Authorization": "Bearer invalid_token"})
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json["msg"], "Not enough segments")

        # Revoked token was tested at logout

    def test_get_user(self):
        """
        Test the get user route.
        """
        response = self.client.get("/auth/user", headers={"Authorization": f"Bearer {self.access_token}"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["username"], "testuser")
        self.assertEqual(response.json["email"], "test@example.com")
        self.assertEqual(response.json["is_admin"], False)
        self.assertEqual(response.json["remaining_requests"], -1)
        self.assertEqual(response.json["firstname"], "John")
        self.assertEqual(response.json["lastname"], "Doe")
        self.assertEqual(response.json["phone"], None)

    def test_update_user(self):
        """
        Test the update user route.
        """
        payload = {
            "firstname": "Jane",
            "lastname": "Doe",
            "phone": "1234567890",
            "is_admin": True
        }
        response = self.client.patch("/auth/user", json=payload, headers={"Authorization": f"Bearer {self.access_token}"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["msg"], "User updated successfully")
        response = self.client.get("/auth/user", headers={"Authorization": f"Bearer {self.access_token}"})
        self.assertEqual(response.json["username"], "testuser")
        self.assertEqual(response.json["email"], "test@example.com")
        self.assertEqual(response.json["remaining_requests"], -1)
        self.assertEqual(response.json["firstname"], "Jane")
        self.assertEqual(response.json["lastname"], "Doe")
        self.assertEqual(response.json["phone"], "1234567890")
        # Ensure normal users cannot update themselves as admin
        self.assertEqual(response.json["is_admin"], False)

    def test_delete_user(self):
        """
        Test the delete user route.
        """
        response = self.client.delete("/auth/user", headers={"Authorization": f"Bearer {self.access_token}"})
        self.assertEqual(response.status_code, 204)
        response = self.client.get("/auth/user", headers={"Authorization": f"Bearer {self.access_token}"})
        self.assertEqual(response.status_code, 401)
        self.assertIn("Error loading the user", response.json["msg"])

    def test_change_password(self):
        """
        Test the change password route.
        """
        # Test invalid old password
        payload = {
            "old_password": "invalidpassword", # wrong password
            "new_password": "newpassword"
        }
        response = self.client.patch("/auth/change-password", json=payload, headers={"Authorization": f"Bearer {self.access_token}"})
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json["msg"], "Invalid old password")
        # Test missing new password
        payload = {
            "old_password": "testpassword",
        }
        response = self.client.patch("/auth/change-password", json=payload, headers={"Authorization": f"Bearer {self.access_token}"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json["msg"], "Missing required fields")
        # Test missing old password
        payload = {
            "new_password": "newpassword"
        }
        response = self.client.patch("/auth/change-password", json=payload, headers={"Authorization": f"Bearer {self.access_token}"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json["msg"], "Missing required fields")
        # Test success
        payload = {
            "old_password": "testpassword",
            "new_password": "newpassword"
        }
        response = self.client.patch("/auth/change-password", json=payload, headers={"Authorization": f"Bearer {self.access_token}"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["msg"], "Password changed successfully")
        # Check old password
        response = self.client.post("/auth/login", json={"username": "testuser", "password": payload["old_password"]})
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json["msg"], "Invalid password")
        # Check new password 
        response = self.client.post("/auth/login", json={"username": "testuser", "password": payload["new_password"]})
        self.assertEqual(response.status_code, 200)
        self.assertIn("access_token", response.json)
        self.assertIn("refresh_token", response.json)
        self.refresh_token = response.json["refresh_token"]
        self.access_token = response.json["access_token"]

    def test_get_password_reset_token(self):
        """
        Test the get password reset token route.
        """
        payload = {
            "email": "test@example.com",
        }
        response = self.client.get("/auth/password-reset-token", json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["msg"], "Password reset email sent")
        # Test missing email
        payload = {}
        response = self.client.get("/auth/password-reset-token", json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json["msg"], "Missing required field: email")
        # Test invalid email
        payload = {
            "email": "invalidemail",
        }
        response = self.client.get("/auth/password-reset-token", json=payload)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json["msg"], "User not found with email invalidemail")
        
    def test_reset_password(self):
        """
        Test the reset password route.
        """
        # Test missing token
        payload = {
            "password": "newpassword",
        }
        response = self.client.patch("/auth/reset-password", json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json["msg"], "Missing required fields")
        # Test missing password
        payload = {
            "token": "1234567890",
        }
        response = self.client.patch("/auth/reset-password", json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json["msg"], "Missing required fields")
        # Test invalid token
        payload = {
            "password": "newpassword",
            "token": "invalidtoken",
        }
        response = self.client.patch("/auth/reset-password", json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json["msg"], "Invalid or expired token") 
        # Test success
        payload = {
            "email": "test@example.com",
        }
        response = self.client.get("/auth/password-reset-token", json=payload)
        with open("reset_password_token.txt", "r") as f:
            token = f.read().splitlines()[1].split(":")[-1].strip()
        payload = {
            "password": "newpassword",
            "token": token,
        }
        response = self.client.patch("/auth/reset-password", json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["msg"], "Password reset successful")

    def test_refresh_token(self):
        """
        Test the refresh token route.
        """
        response = self.client.get("/auth/refresh-token", headers={"Authorization": f"Bearer {self.refresh_token}"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("access_token", response.json)
        self.assertNotEqual(response.json["access_token"], self.access_token)
        new_access_token = response.json["access_token"]
        # Test new access token is valid using get user route
        response = self.client.get("/auth/user", headers={"Authorization": f"Bearer {new_access_token}"})
        self.assertEqual(response.status_code, 200)

    def test_get_all_users(self):
        """
        Test the get all users route.
        """
        from utils import bcrypt
        # Create admin account
        hashed_password = bcrypt.generate_password_hash("password").decode("utf-8")
        user = User(username="username", email="email", password=hashed_password, is_admin=True)
        db.session.add(user)
        response = self.client.post("/auth/login", json={"username": "username", "password": "password"})
        self.assertEqual(response.status_code, 200)
        admin_access_token = response.json["access_token"]
        # Test admin user getting all users
        response = self.client.get("/auth/users", headers={"Authorization": f"Bearer {admin_access_token}"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["users"]), 2)
        self.assertEqual(response.json["users"][0]["username"], "testuser")
        # Test Non admin user getting all users
        response = self.client.get("/auth/users", headers={"Authorization": f"Bearer {self.access_token}"})
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json["msg"], "Unauthorized. Admins only")


if __name__ == "__main__":
    unittest.main()