import unittest

from app import create_app
from flask_config import TestingConfig


class UserBlueprintTestCase(unittest.TestCase):

    def setUp(self) -> None:
        app = create_app(config=TestingConfig)
        app.app_context().push()
        self.app = app.test_client()

    def test_list_users(self):
        """Checks to retrieve users properly."""
        headers = dict(USER_TOKEN="32032dc6-a528-4f2d-b450-0908e07eac5f")
        response = self.app.post("/", headers=headers)
        response = response.json

        self.assertEqual(response["count"], 50)
        self.assertIsNotNone(response["payload"])

    def test_list_visit_items(self):
        """Checks to retrieve visit items properly."""
        headers = dict(USER_TOKEN="32032dc6-a528-4f2d-b450-0908e07eac5f")
        response = self.app.get("/visit", headers=headers)
        response = response.json

        self.assertEqual(response["count"], 3)
        self.assertIsNotNone(len(response["payload"]), 3)

    def test_access_token(self):
        """Checks to verify access token."""
        headers = dict(USER_TOKEN="32032dc6-a528-4f2d-b450-0908e07eac5f")
        response = self.app.get("/access_token/32032dc6-a528-4f2d-b450-0908e07eac5f", headers=headers)
        response = response.json

        self.assertTrue("payload" in response)


if __name__ == "__main__":
    unittest.main()
