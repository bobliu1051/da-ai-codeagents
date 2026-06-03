"""
Orders API v2.

Uses service layer + JWT auth. Returns JSON.
"""
from flask import Blueprint, request, jsonify, g
from app.services.order_service import OrderService
from app.middleware.auth import jwt_required
from app.utils.errors import AppError

bp = Blueprint("orders_v2", __name__)


@bp.route("/", methods=["POST"])
@jwt_required
def create():
    data = request.get_json() or {}
    try:
        svc = OrderService()
        order_id = svc.create_order(g.current_user_id, data.get("items", []))
        return jsonify({"id": order_id}), 201
    except AppError as e:
        return jsonify({"error": str(e)}), e.status_code


@bp.route("/", methods=["GET"])
@jwt_required
def list_mine():
    status = request.args.get("status")
    svc = OrderService()
    orders = svc.list_for_user(g.current_user_id, status=status)
    return jsonify([_order_to_dict(o) for o in orders])


@bp.route("/<int:order_id>/pay", methods=["POST"])
@jwt_required
def pay(order_id):
    data = request.get_json() or {}
    try:
        svc = OrderService()
        intent = svc.pay(order_id, data.get("payment_method_id"))
        return jsonify({"status": "paid", "intent": intent})
    except AppError as e:
        return jsonify({"error": str(e)}), e.status_code


@bp.route("/<int:order_id>/cancel", methods=["POST"])
@jwt_required
def cancel(order_id):
    try:
        svc = OrderService()
        svc.cancel(order_id, g.current_user_id)
        return jsonify({"status": "cancelled"})
    except AppError as e:
        return jsonify({"error": str(e)}), e.status_code


def _order_to_dict(o):
    d = o.to_dict()
    if hasattr(o, "items"):
        d["items"] = [i.to_dict() for i in o.items]
    return d
