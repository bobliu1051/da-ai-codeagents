"""
Legacy session-based auth.

Used by all endpoints under /api/v1/orders and /api/v1/users.
New code should use JWT (see middleware/auth.py).
"""
from functools import wraps
from flask import session, jsonify


def legacy_login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return jsonify({"error": "not logged in"}), 401
        return f(*args, **kwargs)
    return wrapper
