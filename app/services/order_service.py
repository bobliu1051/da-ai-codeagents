"""
Order service.

Handles checkout, payment, status transitions, refunds.
This is the most complex piece. Some pieces are missing.
"""
from app.repositories.order_repo import OrderRepository
from app.repositories.product_repo import ProductRepository
from app.integrations.payment import PaymentClient
from app.integrations.email_sender import send_order_confirmation
from app.utils.errors import ValidationError, NotFoundError, BusinessRuleError
from app.utils.audit import log_action


class OrderService:
    def __init__(self):
        self.orders = OrderRepository()
        self.products = ProductRepository()
        self.payments = PaymentClient()

    def create_order(self, user_id, items):
        """
        items: list of {"product_id": int, "quantity": int}
        """
        if not items:
            raise ValidationError("no items")

        # Compute total from product table (don't trust client price)
        line_items = []
        total = 0
        for item in items:
            product = self.products.find_by_id(item["product_id"])
            if not product:
                raise NotFoundError(f"product {item['product_id']} not found")
            qty = int(item.get("quantity", 1))
            if qty <= 0:
                raise ValidationError("invalid quantity")
            if product.stock < qty:
                raise BusinessRuleError(f"insufficient stock for {product.sku}")
            line_items.append({
                "product_id": product.id,
                "quantity": qty,
                "unit_price_cents": product.price_cents,
            })
            total += product.price_cents * qty

        order_id = self.orders.create(user_id, line_items, total)

        # Decrement stock
        # FIXME: this should be transactional with the order creation.
        # If we crash between order_id creation and stock decrement, stock is wrong.
        for item in line_items:
            self.products.decrement_stock(item["product_id"], item["quantity"])

        log_action(user_id, "order.created", "order", order_id, {"total": total})
        return order_id

    def pay(self, order_id, payment_method_id):
        order = self.orders.find_by_id(order_id)
        if not order:
            raise NotFoundError("order not found")
        if order.status != "pending":
            raise BusinessRuleError(f"cannot pay order in status {order.status}")

        intent = self.payments.charge(order.total_cents, payment_method_id)
        # Note: no error handling for failed charges here
        self.orders.update_status(order_id, "paid")
        # update payment_intent_id separately - oversight
        log_action(order.user_id, "order.paid", "order", order_id, {"intent": intent["id"]})

        # Send confirmation email
        try:
            send_order_confirmation(order.user_id, order_id)
        except Exception:
            pass  # don't fail the payment because of email

        return intent

    def cancel(self, order_id, user_id):
        order = self.orders.find_by_id(order_id)
        if not order:
            raise NotFoundError("order not found")
        if order.user_id != user_id:
            raise BusinessRuleError("not your order")

        # Allowed transitions: pending -> cancelled, paid -> cancelled (with refund)
        if order.status not in ("pending", "paid"):
            raise BusinessRuleError(f"cannot cancel order in status {order.status}")

        if order.status == "paid":
            # Issue refund
            self.payments.refund(order.payment_intent_id)
            self.orders.update_status(order_id, "refunded")
        else:
            self.orders.update_status(order_id, "cancelled")

        # TODO: restore inventory on cancel
        log_action(user_id, "order.cancelled", "order", order_id, None)

    def list_for_user(self, user_id, status=None):
        return self.orders.find_for_user(user_id, status)
