import json
import unittest

from app import create_app
from flask_config import TestingConfig


class ItemBlueprintTestCase(unittest.TestCase):

    def setUp(self) -> None:
        app = create_app(config=TestingConfig)
        app.app_context().push()
        self.app = app.test_client()

    def test_list_all_items(self):
        """Checks to create a post properly."""
        header = dict(USER_TOKEN="32032dc6-a528-4f2d-b450-0908e07eac5f")
        response = self.app.get("/", headers=header)
        response = response.json

        self.assertEqual(len(response), 2)
        self.assertEqual(response["count"], 100)
        self.assertIsNotNone(len(response["payload"]), response["count"])

    def test_get_item(self):
        """Checks to create a post properly."""
        header = dict(USER_TOKEN="32032dc6-a528-4f2d-b450-0908e07eac5f")
        response = self.app.get("/1", headers=header)
        response = response.json

        self.assertIsNotNone(response["payload"])

    def test_list_items(self):
        """Checks to set alarm true properly."""
        headers = dict(USER_TOKEN="32032dc6-a528-4f2d-b450-0908e07eac5f")
        content_type = "application/json"
        data = json.dumps(dict(item_ids=[1, 2, 3, 4]))
        response = self.app.get("/items", data=data, headers=headers, content_type=content_type)
        response = response.json

        self.assertEqual(response["count"], 4)
        self.assertEqual(len(response["payload"]), 4)


if __name__ == "__main__":
    unittest.main()
