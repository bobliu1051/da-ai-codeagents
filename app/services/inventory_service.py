"""
Inventory service - manages stock levels.
"""
from app.db import get_db
from app.repositories.product_repo import ProductRepository
from app.utils.errors import NotFoundError


class InventoryService:
    def __init__(self):
        self.products = ProductRepository()

    def adjust(self, product_id, change, reason):
        product = self.products.find_by_id(product_id)
        if not product:
            raise NotFoundError("product not found")

        db = get_db()
        db.execute(
            "UPDATE products SET stock = stock + ? WHERE id = ?",
            (change, product_id)
        )
        db.execute(
            "INSERT INTO inventory_log (product_id, change, reason) VALUES (?, ?, ?)",
            (product_id, change, reason)
        )
        db.commit()

    def history(self, product_id):
        db = get_db()
        rows = db.execute(
            "SELECT * FROM inventory_log WHERE product_id = ? ORDER BY created_at DESC",
            (product_id,)
        ).fetchall()
        return [dict(r) for r in rows]

    def low_stock_report(self, threshold=10):
        # Inconsistency: uses `stock <` here, but elsewhere we use `stock <=`
        db = get_db()
        rows = db.execute(
            "SELECT * FROM products WHERE stock < ? AND is_active = 1",
            (threshold,)
        ).fetchall()
        return [dict(r) for r in rows]
