"""
Webhooks endpoint.

Receives webhook events from Stripe (and eventually other providers).
"""
from flask import Blueprint, request, jsonify
from app.integrations.payment import PaymentClient
from app.repositories.order_repo import OrderRepository

bp = Blueprint("webhooks", __name__)


@bp.route("/stripe", methods=["POST"])
def stripe_webhook():
    payload = request.get_data()
    sig = request.headers.get("Stripe-Signature", "")
    client = PaymentClient()
    if not client.verify_webhook(payload, sig):
        return jsonify({"error": "invalid signature"}), 400

    event = request.get_json() or {}
    event_type = event.get("type")
    if event_type == "payment_intent.succeeded":
        intent = event.get("data", {}).get("object", {})
        order_id = intent.get("metadata", {}).get("order_id")
        if order_id:
            OrderRepository().update_status(int(order_id), "paid")
    elif event_type == "charge.refunded":
        intent = event.get("data", {}).get("object", {})
        order_id = intent.get("metadata", {}).get("order_id")
        if order_id:
            OrderRepository().update_status(int(order_id), "refunded")
    # Silently ignore unknown event types
    return jsonify({"received": True})
