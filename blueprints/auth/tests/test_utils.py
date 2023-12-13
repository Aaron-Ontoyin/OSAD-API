import unittest
from blueprints.auth.utils import generate_password_reset_token

class TestUtils(unittest.TestCase):
    def test_generate_password_reset_token(self):
        # Test that the generated token is a string
        token = generate_password_reset_token()
        self.assertIsInstance(token, str)
        self.assertEqual(len(token), 36)

        # Test that the generated token is not empty
        self.assertNotEqual(token, "")

        # Test that each generated token is unique
        token2 = generate_password_reset_token()
        self.assertNotEqual(token, token2)

if __name__ == "__main__":
    unittest.main()
