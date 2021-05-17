import requests

from flask import abort
from flask import current_app as app


# 서비스 레이어에서 skippable annotation 으로 exception 관리
def list_items_by_item_ids(item_ids):
    """아이템 서버에서 상품 아이디를 받아 온다."""
    base_url = app.config["API_ITEM"]
    url = f"{base_url}/items"
    headers = {'Content-type': 'application/json'}
    data = dict(item_ids=item_ids)
    response = requests.get(url, headers=headers, json=data)

    if not response.ok:
        abort(500)

    response = response.json()
    return response["payload"]
