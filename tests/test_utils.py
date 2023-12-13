import os
import unittest

import redis
from dotenv import load_dotenv

from utils import send_email, db, redis_client
from app import app

load_dotenv()

class UtilitiesTestCase(unittest.TestCase):
    def setUp(self):
        """
        Set up the test environment
        """
        self.app = app.test_client()
        self.app.testing = True

    def test_send_email(self):
        """
        Test sending an email
        """
        recipient = "test@example.com"
        subject = "Test Subject"
        message = "Test Message"

        send_email(recipient, subject, message)

        # Later, this would be an actual email
        with open("reset_password_token.txt", "r") as f:
            file_contents = f.read()
            self.assertIn(message, file_contents)

        os.remove("reset_password_token.txt")

    def test_postgres_connection(self):
        """
        Test the connection to the PostgreSQL database
        """
        db_uri = os.getenv("SQLALCHEMY_DATABASE_URI")
        try:
            engine = db.create_engine(db_uri)
            conn = engine.connect()
        except Exception as e:
            self.fail("PostgreSQL connection test failed: {}".format(e))
        else:
            self.assertTrue(conn)
            conn.close()

    def test_redis_connection(self):
        """
        Test the connection to the Redis database
        """
        try:
            redis_client = redis.StrictRedis(
                host=os.getenv("REDIS_HOST"), port=os.getenv("REDIS_PORT"), db=0, decode_responses=True
            )
        except Exception as e:
            self.fail("Redis connection test failed: {}".format(e))
        else:
            self.assertTrue(redis_client)


if __name__ == '__main__':
    unittest.main()