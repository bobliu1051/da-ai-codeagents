"""
Application factory.

NOTE: Some routes are wired up here directly, others via blueprint auto-discovery.
The auto-discovery only picks up modules under app/api/v2/. Legacy routes under
app/legacy/ are wired up manually below.
"""
from flask import Flask
from app.config import get_config
from app.db import init_db
from app.middleware.logging import LoggingMiddleware
from app.middleware.auth import jwt_required
from app.middleware.rate_limit import RateLimiter

import importlib
import pkgutil


def create_app(env=None):
    app = Flask(__name__)
    cfg = get_config(env)
    app.config.update(cfg)

    init_db(app)

    # Middleware
    app.wsgi_app = LoggingMiddleware(app.wsgi_app)
    rate_limiter = RateLimiter(app, max_per_minute=60)

    # Auto-discover v2 blueprints
    from app.api import v2 as v2_pkg
    for _, modname, _ in pkgutil.iter_modules(v2_pkg.__path__):
        mod = importlib.import_module(f"app.api.v2.{modname}")
        if hasattr(mod, "bp"):
            app.register_blueprint(mod.bp, url_prefix=f"/api/v2/{modname}")

    # Legacy routes - manually wired
    from app.legacy import old_orders, old_users
    app.register_blueprint(old_orders.bp, url_prefix="/api/v1/orders")
    app.register_blueprint(old_users.bp, url_prefix="/api/v1/users")

    # V1 (newer than legacy, older than v2) - some routes here too
    from app.api.v1 import products, inventory
    app.register_blueprint(products.bp, url_prefix="/api/v1/products")
    app.register_blueprint(inventory.bp, url_prefix="/api/v1/inventory")

    return app
