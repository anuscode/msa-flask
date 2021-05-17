"""Alarm blue_print definitions."""
from flask import abort
from flask import Blueprint
from flask import request
from shared.annotations import as_json, internal_only
from shared.authentication import auth_required
from services import alarm_service

alarm_blueprint = Blueprint("alarm_blueprint", __name__)


@alarm_blueprint.route("/", methods=["POST"])
@as_json
@auth_required
def update_alarm_true(user):
    """Sets alarm true."""
    params = request.get_json()
    item_id = params.get("item_id", None)
    user_id = user.get("id", None)
    alarm_service.set_alarm_true(user_id, item_id)
    response = dict()
    return response


@alarm_blueprint.route("/", methods=["DELETE"])
@as_json
@auth_required
def update_alarm_false(user):
    """Sets alarm false."""
    params = request.get_json()
    item_id = params.get("item_id", None)
    user_id = user.get("id", None)
    alarm_service.set_alarm_false(user_id, item_id)
    response = dict()
    return response


@alarm_blueprint.route("/", methods=["GET"])
@as_json
@auth_required
def list_user_alarmed_items(user):
    """Retrieves user's alarmed items."""
    user_id = user.get("id", None)
    items = alarm_service.list_user_alarmed_items(user_id)
    response = dict(count=len(items), payload=items)
    return response


@alarm_blueprint.route("/alarm_item_ids", methods=["GET"])
@as_json
@internal_only
def list_user_alarmed_item_ids():
    """Retrieves user's alarmed item ids."""
    params = request.get_json()
    user_id = params.get("user_id", None)

    if not user_id:
        abort(500)

    item_ids = alarm_service.list_user_alarmed_item_ids(user_id)
    response = dict(count=len(item_ids), payload=item_ids)
    return response
