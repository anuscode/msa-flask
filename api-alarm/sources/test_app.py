import json
import unittest

from app import create_app
from flask_config import TestingConfig


class AlarmBlueprintTestCase(unittest.TestCase):

    def setUp(self) -> None:
        app = create_app(config=TestingConfig)
        app.app_context().push()
        self.app = app.test_client()

    def test_update_alarm_true(self):
        """Checks to set alarm true properly."""
        headers = dict(USER_TOKEN="32032dc6-a528-4f2d-b450-0908e07eac5f")
        content_type = "application/json"
        data = json.dumps(dict(item_id=99))
        response = self.app.post("/", data=data, headers=headers, content_type=content_type)

        self.assertEqual(response.json, {})

    def test_update_alarm_false(self):
        """Checks to set alarm false properly."""
        headers = dict(USER_TOKEN="32032dc6-a528-4f2d-b450-0908e07eac5f")
        content_type = "application/json"
        data = json.dumps(dict(item_id=3))
        response = self.app.delete("/", data=data, headers=headers, content_type=content_type)

        self.assertEqual(response.json, {})

    def test_list_user_alarmed_item(self):
        """Checks to set alarm false properly."""
        headers = dict(USER_TOKEN="32032dc6-a528-4f2d-b450-0908e07eac5f")
        response = self.app.get("/", headers=headers)
        response = response.json
        items = response["payload"]

        for item1, item2 in zip(items[:-1], items[1:]):
            self.assertTrue(item1["id"] >= item2["id"])

    def test_list_user_alarmed_item_ids(self):
        """Checks to retrieve alarmed item ids properly."""
        content_type = "application/json"
        data = json.dumps(dict(user_id=3))
        response = self.app.get("/alarm_item_ids", data=data, content_type=content_type)
        response = response.json
        print(response)


if __name__ == "__main__":
    unittest.main()
