"""
Payment integration.

Wraps the payment provider (currently Stripe). The signature was designed
to allow swapping providers but it's coupled to Stripe-specific fields.
"""
import os


class PaymentClient:
    def __init__(self):
        self.api_key = os.getenv("STRIPE_KEY", "sk_test_xxx")

    def charge(self, amount_cents, payment_method_id):
        # In real code this calls stripe.PaymentIntent.create(...)
        # For now, simulate.
        if amount_cents <= 0:
            raise ValueError("invalid amount")
        return {
            "id": f"pi_{payment_method_id}_{amount_cents}",
            "status": "succeeded",
            "amount": amount_cents,
        }

    def refund(self, payment_intent_id):
        if not payment_intent_id:
            raise ValueError("no payment intent to refund")
        return {
            "id": f"re_{payment_intent_id}",
            "status": "succeeded",
        }

    def verify_webhook(self, payload, signature):
        # TODO: implement signature verification
        # For now, accept all webhooks (dangerous!)
        return True
