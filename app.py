from flask import Flask

from database import db
from endpoints.events import ns
from restplus import api
from config import configure_app


def init_app(app, config_type):
    configure_app(app, config_type)
    app.url_map.strict_slashes = False
    db.init_app(app)

    api.init_app(app)
    api.add_namespace(ns)

    if config_type == "testing":
        with app.app_context():
            db.create_all()


if __name__ == "__main__":
    app = Flask(__name__)
    init_app(app, "testing")
    app.run(host="0.0.0.0", port=8080)
