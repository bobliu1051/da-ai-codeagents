from flask import Flask
from .routes import todos_bp, users_bp
from .db import init_db


def create_app(config=None):
    app = Flask(__name__)
    app.config["DATABASE"] = config.get("DATABASE", "todos.db") if config else "todos.db"
    app.config["SECRET_KEY"] = "dev-secret-change-me"  # TODO: move to env

    init_db(app)

    app.register_blueprint(todos_bp, url_prefix="/api/todos")
    app.register_blueprint(users_bp, url_prefix="/api/users")

    return app
