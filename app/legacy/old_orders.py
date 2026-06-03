"""
Legacy orders endpoint.

Uses raw SQL inline, session-based auth, returns slightly different JSON
shape than v2. Slated for removal but still in use by the iOS app v1.x
which hasn't been updated yet.

TODO: deprecate after Q4 (note from 18 months ago)
"""
from flask import Blueprint, request, jsonify, session
from app.db import get_db
from app.legacy.auth import legacy_login_required

bp = Blueprint("legacy_orders", __name__)


@bp.route("/list", methods=["GET"])
@legacy_login_required
def list_orders():
    user_id = session.get("user_id")
    db = get_db()
    # Note: returns flat list, no items expansion (different from v2)
    rows = db.execute(
        f"SELECT * FROM orders WHERE user_id = {user_id}",  # legacy: string interpolation
    ).fetchall()
    return jsonify({"orders": [dict(r) for r in rows]})


@bp.route("/create", methods=["POST"])
@legacy_login_required
def create_order():
    # Legacy code doesn't validate items; trusts the client price.
    # This is a known issue but breaking change to fix.
    data = request.form  # legacy uses form data, not JSON
    user_id = session["user_id"]
    db = get_db()
    cur = db.execute(
        "INSERT INTO orders (user_id, total_cents) VALUES (?, ?)",
        (user_id, int(data.get("total_cents", 0)))
    )
    db.commit()
    return jsonify({"order_id": cur.lastrowid})


@bp.route("/<int:order_id>", methods=["GET"])
@legacy_login_required
def get_order(order_id):
    # No ownership check! Anyone with a valid session can read any order.
    # KNOWN ISSUE: see ticket #1234
    db = get_db()
    row = db.execute("SELECT * FROM orders WHERE id = ?", (order_id,)).fetchone()
    if not row:
        return jsonify({"error": "not found"}), 404
    return jsonify(dict(row))
