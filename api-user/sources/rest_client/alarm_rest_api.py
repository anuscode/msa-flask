import requests

from flask import abort
from flask import current_app as app


# 서비스 레이어에서 skippable annotation 으로 exception 관리
def list_user_alarmed_item_ids(user_id):
    """알람 서버에서 알람 상품 아이디를 받아 온다."""
    base_url = app.config["API_ALARM"]
    url = f"{base_url}/alarm_item_ids"
    headers = {'Content-type': 'application/json'}
    data = dict(user_id=user_id)
    response = requests.get(url, headers=headers, json=data)

    if not response.ok:
        abort(500)

    response = response.json()
    return response["payload"]
