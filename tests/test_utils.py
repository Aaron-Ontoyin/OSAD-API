import os
import unittest
import unittest
from unittest.mock import patch

import redis
from dotenv import load_dotenv

from utils import send_mail, create_email_message, db
from app import app

load_dotenv()


class UtilitiesTestCase(unittest.TestCase):
    def setUp(self):
        """
        Set up the test environment
        """
        self.app = app.test_client()
        self.app.testing = True

    @unittest.skip("skipping test_send_email")
    @patch('utils.smtp')
    def test_send_email(self, mock_smtp):
        mock_smtp_instance = mock_smtp.return_value

        send_mail("el-aoyin9021@st.umat.edu.gh", "Test subject", "Test body")

        from_mail_address = os.getenv("SMTP_EMAIL_ADDRESS")
        from_email_password = os.getenv("SMTP_EMAIL_PASSWORD")

        mock_smtp_instance.login.assert_called_with(from_mail_address, from_email_password)

        msg = create_email_message(subject="Test subject", text="Test body")

        mock_smtp_instance.sendmail.assert_called_with(
            from_mail_address, "test@vw.com", msg.as_string()
        )

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
            rurl = os.getenv("REDIS_URL")
            rhost = rurl.split(":")[1].strip("//")
            rport = rurl.split(":")[2].split("/")[0]
            rdb = rurl.split(":")[2].split("/")[1]
            redis_client = redis.StrictRedis(
                host=rhost, port=rport, db=rdb, decode_responses=True
            )

        except Exception as e:
            self.fail("Redis connection test failed: {}".format(e))
        else:
            self.assertTrue(redis_client)


if __name__ == "__main__":
    unittest.main()
