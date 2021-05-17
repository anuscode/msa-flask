"""User blue_print definitions."""
from flask import request
from flask import Blueprint
from shared.annotations import as_json, internal_only
from shared.authentication import auth_required
from services import item_service

item_blueprint = Blueprint("item_blueprint", __name__)


@item_blueprint.route("/", methods=["GET"])
@as_json
@auth_required
def list_all_items(user):
    """Retrieves all items."""
    user_id = user["id"]
    items = item_service.list_all_items(user_id)
    response = dict(count=len(items), payload=items)
    return response


@item_blueprint.route("/<int:item_id>", methods=["GET"])
@as_json
@auth_required
def get_item(user, item_id: int):
    """Retrieves a item by item_id."""
    user_id = user["id"]
    item = item_service.get_item(user_id, item_id)
    if not item:
        return dict()
    item_service.heapq_visit_item_id(user_id, item_id)
    response = dict(payload=item)
    return response


@item_blueprint.route("/items", methods=["GET"])
@as_json
@internal_only
def list_items():
    """Retrieves item list by item_ids."""
    params = request.get_json()
    item_ids = params.get("item_ids", [])
    items = item_service.list_items_by_item_ids(item_ids)
    response = dict(count=len(items), payload=items)
    return response
