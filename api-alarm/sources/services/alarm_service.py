import json
import time

from model.models import Alarm
from rest_client import user_rest_client, item_rest_client
from redis_client.redis_cache import cache_v, cache_r
from redis_client.redis_client import RedisClient
from shared.annotations import transactional, skippable


@cache_r(ttl=600, prefix="user::access_token::")
def get_user_by_access_token(access_token):
    """Get an user using access token, will abort 401 when not found user."""
    user = user_rest_client.get_user_by_access_token(access_token)
    return user


@cache_r(ttl=600, prefix="alarmed_item_ids::user_id::")
def list_user_alarmed_item_ids(user_id):
    """유저의 알람 처리 된 아이템 '아이디'를 반납한다."""
    items = Alarm.list_user_alarmed_items(user_id=user_id)
    item_ids = [item["id"] for item in items]
    return item_ids


@skippable([])
def _list_items_by_item_ids(item_ids):
    items = item_rest_client.list_items_by_item_ids(item_ids)
    items.sort(key=lambda x: x.get("id", 0), reverse=True)
    return items


def list_user_alarmed_items(user_id):
    """유저의 알람 처리 된 '아이템'을 반납한다."""
    item_ids = list_user_alarmed_item_ids(user_id)
    items = _list_items_by_item_ids(item_ids)
    items.sort(key=lambda x: x.get("id", 0), reverse=True)
    return items


@transactional
def set_alarm_true(user_id, item_id):
    Alarm.insert_alarm_item(user_id=user_id, item_id=item_id)
    items = Alarm.list_user_alarmed_items(user_id=user_id)
    items = [item["item_id"] for item in items]
    dumped = json.dumps(items)
    RedisClient.set(f"alarmed_item_ids::user_id::{user_id}", dumped, ex=600)


@transactional
def set_alarm_false(user_id, item_id):
    Alarm.delete_alarm_item(user_id=user_id, item_id=item_id)
    items = Alarm.list_user_alarmed_items(user_id=user_id)
    items = [item["item_id"] for item in items]
    dumped = json.dumps(items)
    RedisClient.set(f"alarmed_item_ids::user_id::{user_id}", dumped, ex=600)
