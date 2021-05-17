import requests
import time

from rest_client import user_rest_client, alarm_rest_client
from redis_client.redis_client import RedisClient
from redis_client.redis_cache import cache_v, cache_r
from model.models import Item
from shared.annotations import skippable


@cache_r(ttl=600, prefix="user::access_token::")
def get_user_by_access_token(access_token):
    """Get an user using access token, will abort 401 when not found user."""
    user = user_rest_client.get_user_by_access_token(access_token)
    return user


def list_all_items(user_id):
    alarm_item_ids = set(_list_alarm_item_ids(user_id))
    items = Item.list_items()
    for item in items:
        item["is_alarm_set"] = item["id"] in alarm_item_ids
    return items


def list_items_by_item_ids(item_ids):
    items = Item.list_items_by_item_ids(item_ids)
    return items


def get_item(user_id, item_id):
    item = Item.get_item(id=item_id)
    if not item:
        return item
    alarm_item_ids = _list_alarm_item_ids(user_id)
    item["is_alarm_set"] = item_id in alarm_item_ids
    return item


@skippable([])
@cache_r(ttl=600, prefix="alarmed_item_ids::user_id::")
def _list_alarm_item_ids(user_id):
    alarmed_item_ids = alarm_rest_client.list_user_alarmed_item_ids(user_id)
    return alarmed_item_ids


def _list_visit_item_ids(user_id):
    con = RedisClient.connect()
    key = f"latest_visit_item_ids::user_id::{user_id}"
    item_ids = con.zrange(key, 0, -1, desc=True)
    return list(map(int, item_ids))


def list_visit_items(user_id):
    item_ids = _list_visit_item_ids(user_id)
    items = list_items_by_item_ids(item_ids)
    items_map = {item["id"]: item for item in items}
    result = [items_map.get(item_id, None) for item_id in item_ids]
    return list(filter(lambda x: x is not None, result))


def heapq_visit_item_id(user_id, item_id):
    con = RedisClient.connect()
    key = f"latest_visit_item_ids::user_id::{user_id}"
    time_stamp = time.time()
    con.zadd(key, {item_id: time_stamp}, ch=True)

    item_ids = _list_visit_item_ids(user_id)
    for _ in range(len(item_ids) - 3):
        con.zpopmin(key)
