from flask import Flask

from config import configure_app
from database import db
from endpoints.reports import ns
from restplus import api

app = Flask(__name__, static_folder="web")


@app.route('/view')
def view():
    return app.send_static_file("index.html")


def init_app(app, config_type):
    configure_app(app, config_type)
    app.url_map.strict_slashes = False
    db.init_app(app)

    api.init_app(app)
    api.add_namespace(ns)

    if config_type == "testing":
        with app.app_context():
            db.drop_all()
            db.create_all()


if __name__ == "__main__":
    init_app(app, "testing")
    app.run(host="0.0.0.0", port=8080)
