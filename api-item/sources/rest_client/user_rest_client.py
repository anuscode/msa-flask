import requests

from flask import abort
from flask import current_app as app


def get_user_by_access_token(access_token):
    base_url = app.config["API_USER"]
    url = f"{base_url}/access_token/{access_token}"
    response = requests.get(url)

    if response.status_code == 404:
        abort(401)

    if not response.ok:
        abort(500)

    response = response.json()
    ret = response["payload"]
    return ret
