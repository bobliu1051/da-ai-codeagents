"""
Legacy users endpoint.

Pre-dates UserService. Has its own register/login implementation.
"""
import hashlib
from flask import Blueprint, request, jsonify, session
from app.db import get_db

bp = Blueprint("legacy_users", __name__)


@bp.route("/register", methods=["POST"])
def register():
    data = request.form
    email = data.get("email")
    password = data.get("password")
    if not email or not password:
        return jsonify({"error": "missing fields"}), 400

    # SHA1 hashing - never updated. WARNING: known weak.
    pwhash = hashlib.sha1(password.encode()).hexdigest()
    db = get_db()
    try:
        cur = db.execute(
            "INSERT INTO users (email, password_hash) VALUES (?, ?)",
            (email, pwhash)
        )
        db.commit()
        return jsonify({"user_id": cur.lastrowid})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route("/login", methods=["POST"])
def login():
    data = request.form
    email = data.get("email")
    password = data.get("password")
    pwhash = hashlib.sha1(password.encode()).hexdigest()
    db = get_db()
    row = db.execute(
        "SELECT * FROM users WHERE email = ? AND password_hash = ?",
        (email, pwhash)
    ).fetchone()
    if not row:
        return jsonify({"error": "invalid login"}), 401
    session["user_id"] = row["id"]
    return jsonify({"status": "ok"})


@bp.route("/logout", methods=["POST"])
def logout():
    session.pop("user_id", None)
    return jsonify({"status": "ok"})
