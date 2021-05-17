import json

from flask import current_app as app
from flask import request
from flask import Response
from functools import wraps


class InternalOnlyException(Exception):
    pass


def internal_only(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        allows = app.config["INTERNAL_URLS"]
        is_internal = request.host in allows
        if not is_internal:
            raise InternalOnlyException(
                f"{request.host} is not allow to use this method due to external call prohibit policy."
            )
        response = f(*args, **kwargs)
        return response

    return wrapper


def as_json(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        response = f(*args, **kwargs)

        if not isinstance(response, dict):
            raise ValueError("dict type response required..")

        response = json.dumps(response, ensure_ascii=False)
        return Response(response, mimetype='application/json')

    return wrapper


def skippable(r):
    def decorator(f):
        def wrapper(*args, **kwargs):
            try:
                result = f(*args, **kwargs)
                return result
            except Exception as e:
                print(e)
                return r

        return wrapper

    return decorator
