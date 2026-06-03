"""
Seed the database with sample data.

Usage:
    python -m scripts.seed
"""
from app import create_app
from app.services.user_service import UserService
from app.db import get_db


def seed():
    app = create_app("development")
    with app.app_context():
        svc = UserService()
        try:
            svc.register("admin@example.com", "admin1234", username="admin")
        except Exception:
            pass  # already exists

        db = get_db()
        # Make admin an admin
        db.execute("UPDATE users SET role = 'admin' WHERE email = 'admin@example.com'")

        # Add some products
        products = [
            ("SKU-001", "Widget", "A useful widget", 999, 50),
            ("SKU-002", "Gadget", "A clever gadget", 1499, 20),
            ("SKU-003", "Thingamajig", "Hard to describe", 2499, 5),
        ]
        for sku, name, desc, price, stock in products:
            db.execute(
                "INSERT OR IGNORE INTO products (sku, name, description, price_cents, stock) "
                "VALUES (?, ?, ?, ?, ?)",
                (sku, name, desc, price, stock)
            )
        db.commit()
        print("Seeded.")


if __name__ == "__main__":
    seed()
