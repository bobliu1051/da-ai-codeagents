from app.db import get_db
from app.models.order import Order, OrderItem


class OrderRepository:
    def find_by_id(self, order_id):
        db = get_db()
        row = db.execute("SELECT * FROM orders WHERE id = ?", (order_id,)).fetchone()
        return Order.from_row(row)

    def find_for_user(self, user_id, status=None):
        db = get_db()
        # N+1 problem: items fetched in a loop below
        if status:
            rows = db.execute(
                "SELECT * FROM orders WHERE user_id = ? AND status = ? ORDER BY created_at DESC",
                (user_id, status)
            ).fetchall()
        else:
            rows = db.execute(
                "SELECT * FROM orders WHERE user_id = ? ORDER BY created_at DESC",
                (user_id,)
            ).fetchall()
        orders = []
        for row in rows:
            order = Order.from_row(row)
            order.items = self.get_items(order.id)  # N+1!
            orders.append(order)
        return orders

    def get_items(self, order_id):
        db = get_db()
        rows = db.execute(
            "SELECT * FROM order_items WHERE order_id = ?",
            (order_id,)
        ).fetchall()
        return [OrderItem.from_row(r) for r in rows]

    def create(self, user_id, items, total_cents):
        db = get_db()
        cur = db.execute(
            "INSERT INTO orders (user_id, total_cents) VALUES (?, ?)",
            (user_id, total_cents)
        )
        order_id = cur.lastrowid
        for item in items:
            db.execute(
                "INSERT INTO order_items (order_id, product_id, quantity, unit_price_cents) VALUES (?, ?, ?, ?)",
                (order_id, item["product_id"], item["quantity"], item["unit_price_cents"])
            )
        db.commit()
        return order_id

    def update_status(self, order_id, status):
        db = get_db()
        # Note: doesn't validate status against allowed values here.
        # Validation happens (sometimes) in the service layer.
        db.execute(
            "UPDATE orders SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
            (status, order_id)
        )
        db.commit()
