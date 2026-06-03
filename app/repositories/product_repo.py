from app.db import get_db
from app.models.order import Product


class ProductRepository:
    def find_by_id(self, product_id):
        db = get_db()
        row = db.execute(
            "SELECT * FROM products WHERE id = ? AND is_active = 1",
            (product_id,)
        ).fetchone()
        return Product.from_row(row)

    def find_by_sku(self, sku):
        db = get_db()
        row = db.execute("SELECT * FROM products WHERE sku = ?", (sku,)).fetchone()
        return Product.from_row(row)

    def list_active(self, limit=100, offset=0):
        db = get_db()
        rows = db.execute(
            "SELECT * FROM products WHERE is_active = 1 LIMIT ? OFFSET ?",
            (limit, offset)
        ).fetchall()
        return [Product.from_row(r) for r in rows]

    def search(self, query):
        # Simple LIKE search. TODO: switch to FTS
        db = get_db()
        rows = db.execute(
            "SELECT * FROM products WHERE name LIKE ? OR description LIKE ?",
            (f"%{query}%", f"%{query}%")
        ).fetchall()
        return [Product.from_row(r) for r in rows]

    def decrement_stock(self, product_id, qty):
        db = get_db()
        # WARNING: race condition. No SELECT FOR UPDATE in SQLite.
        # Has caused negative stock in production a few times.
        db.execute(
            "UPDATE products SET stock = stock - ? WHERE id = ?",
            (qty, product_id)
        )
        db.execute(
            "INSERT INTO inventory_log (product_id, change, reason) VALUES (?, ?, ?)",
            (product_id, -qty, "order")
        )
        db.commit()
