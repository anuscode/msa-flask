"""User blue_print definitions."""
from flask import abort
from flask import Blueprint
from shared.annotations import as_json, internal_only
from shared.authentication import auth_required
from services import user_service

user_blueprint = Blueprint("user_blueprint", __name__)


@user_blueprint.route("/", methods=["POST"])
@as_json
@auth_required
def list_users(_):
    """Checks session.."""
    users = user_service.list_users()
    response = dict(count=len(users), payload=users)
    return response


@user_blueprint.route("/visit", methods=["GET"])
@as_json
@auth_required
def list_visit_items(user):
    """Checks session.."""
    user_id = user["id"]
    visit_items = user_service.list_visit_items_by_user_id(user_id)
    response = dict(count=len(visit_items), payload=visit_items)
    return response


@user_blueprint.route("/access_token/<access_token>", methods=["GET"])
@as_json
@internal_only
def verify_access_token(access_token: str):
    user = user_service.get_user_by_access_token(access_token)
    if not user:
        abort(404)
    response = dict(payload=user)
    return response
