from flask import abort
from redis_client.redis_cache import cache_v, cache_r
from redis_client.redis_client import RedisClient
from model.models import User
from rest_client import item_rest_api
from rest_client import alarm_rest_api
from shared.annotations import skippable


def list_users():
    """Retrieves all users.."""
    user = User.list_users()
    return user


@cache_r(ttl=600, prefix="user::access_token::")
def get_user_by_access_token(access_token):
    """Get an user using access token, will abort 401 when not found user."""
    user = User.get_user(access_token=access_token)
    return user


def _list_visit_item_ids(user_id):
    con = RedisClient.connect()
    key = f"latest_visit_item_ids::user_id::{user_id}"
    item_ids = con.zrange(key, 0, -1, desc=True)
    return list(map(int, item_ids))


@skippable([])
@cache_r(ttl=600, prefix="alarmed_item_ids::user_id::")
def list_user_alarmed_item_ids(user_id):
    alarm_item_ids = alarm_rest_api.list_user_alarmed_item_ids(user_id)
    return alarm_item_ids


@skippable([])
def list_items_by_item_ids(item_ids):
    items = item_rest_api.list_items_by_item_ids(item_ids)
    return items


def list_visit_items_by_user_id(user_id):
    # visited item_ids from redis
    item_ids = _list_visit_item_ids(user_id)

    # item data from API_ITEM
    items = list_items_by_item_ids(item_ids)
    items = {item["id"]: item for item in items}

    # get user's alarmed item ids from API_ALARM
    alarm_item_ids = list_user_alarmed_item_ids(user_id)
    alarm_item_ids = set(alarm_item_ids)

    result = []
    for item_id in item_ids:
        item = items.get(item_id, None)
        if not item:
            continue
        item["is_alarm_set"] = item_id in alarm_item_ids
        result.append(item)

    return result
