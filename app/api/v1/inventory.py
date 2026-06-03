"""
Inventory API v1.

Admin-only endpoints for managing stock.
"""
from flask import Blueprint, request, jsonify, g
from app.services.inventory_service import InventoryService
from app.middleware.auth import jwt_required, admin_required
from app.utils.errors import AppError

bp = Blueprint("inventory_v1", __name__)


@bp.route("/<int:product_id>/adjust", methods=["POST"])
@jwt_required
@admin_required
def adjust(product_id):
    data = request.get_json() or {}
    try:
        svc = InventoryService()
        svc.adjust(product_id, int(data.get("change", 0)), data.get("reason", ""))
        return jsonify({"status": "ok"})
    except AppError as e:
        return jsonify({"error": str(e)}), e.status_code


@bp.route("/<int:product_id>/history", methods=["GET"])
@jwt_required
@admin_required
def history(product_id):
    svc = InventoryService()
    return jsonify(svc.history(product_id))


@bp.route("/low-stock", methods=["GET"])
@jwt_required
def low_stock():
    # Note: this requires JWT but not admin. Inconsistent with adjust/history above.
    threshold = int(request.args.get("threshold", 10))
    svc = InventoryService()
    return jsonify(svc.low_stock_report(threshold))
