"""
JWT-based authentication decorator.

There's also a session-based auth in legacy/auth.py. The legacy endpoints
use sessions; the v1 and v2 APIs use JWT. There's no plan documented for
unifying these.
"""
import jwt
from functools import wraps
from flask import request, g, current_app, jsonify


def jwt_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return jsonify({"error": "missing token"}), 401
        token = auth_header[7:]
        try:
            payload = jwt.decode(
                token,
                current_app.config["JWT_SECRET"],
                algorithms=["HS256"]
            )
            g.current_user_id = payload["user_id"]
            g.current_user_role = payload.get("role", "user")
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "invalid token"}), 401
        return f(*args, **kwargs)
    return wrapper


def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if getattr(g, "current_user_role", None) != "admin":
            return jsonify({"error": "admin required"}), 403
        return f(*args, **kwargs)
    return wrapper
