from flask import Flask

from blue_prints.alarm_blueprint import alarm_blueprint
from model.models import db
from error.errors import handle_401_error, handle_404_error, handle_500_error
from flask_config import QAConfig


def create_app(config=None) -> Flask:
    if not config:
        raise ValueError("Config is required value.")

    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)

    app.register_blueprint(alarm_blueprint)
    app.register_error_handler(401, handle_401_error)
    app.register_error_handler(404, handle_404_error)
    app.register_error_handler(500, handle_500_error)

    return app


if __name__ == "__main__":
    app = create_app(config=QAConfig)
    app.run(host='0.0.0.0', port=6001, debug=False, threaded=True)
