from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def reset_database(app):
    db.drop_all(app)
    db.create_all(app)


