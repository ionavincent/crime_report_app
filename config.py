class Config:
    FLASK_SERVER_NAME = "0.0.0.0"
    FLASK_DEBUG = False

    SQLALCHEMY_DATABASE_URI = "sqlite:///db.sqlite"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig(Config):
    TESTING = True

class DefaultConfig(Config):
    TESTING = False


config = {
    "default": DefaultConfig,
    "testing": TestConfig
}

def configure_app(app, config_type):
    app.config.from_object(config[config_type])