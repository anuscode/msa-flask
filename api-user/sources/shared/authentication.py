from flask import abort
from flask import request

from functools import wraps
from services.user_service import get_user_by_access_token


def auth_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        access_token = request.headers.get("USER-TOKEN", None)
        if not access_token:
            abort(401)

        user = get_user_by_access_token(access_token)
        if not user:
            abort(401)

        response = f(user, *args, **kwargs)
        return response

    return wrapper
