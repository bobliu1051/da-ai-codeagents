"""
Users API v2.

Register, login, get current user. JWT-based.
"""
import jwt
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify, current_app, g
from app.services.user_service import UserService
from app.middleware.auth import jwt_required
from app.utils.errors import AppError

bp = Blueprint("users_v2", __name__)


@bp.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    try:
        svc = UserService()
        user = svc.register(data.get("email"), data.get("password"), username=data.get("username"))
        return jsonify(user.to_public_dict()), 201
    except AppError as e:
        return jsonify({"error": str(e)}), e.status_code


@bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    try:
        svc = UserService()
        user = svc.authenticate(data.get("email"), data.get("password"))
        token = _make_jwt(user)
        return jsonify({"token": token, "user": user.to_public_dict()})
    except AppError as e:
        return jsonify({"error": str(e)}), e.status_code


@bp.route("/me", methods=["GET"])
@jwt_required
def me():
    svc = UserService()
    user = svc.get_by_id(g.current_user_id)
    return jsonify(user.to_public_dict())


def _make_jwt(user):
    payload = {
        "user_id": user.id,
        "role": user.role,
        "exp": datetime.utcnow() + timedelta(seconds=current_app.config["JWT_EXPIRY_SECONDS"]),
    }
    return jwt.encode(payload, current_app.config["JWT_SECRET"], algorithm="HS256")
