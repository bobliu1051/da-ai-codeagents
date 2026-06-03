"""
Background tasks.

Currently run synchronously. The plan was to move to Celery + Redis but
that migration is incomplete. See tasks/queue.py for the half-done queue.
"""
from app.db import get_db
from app.integrations.email_sender import send_email


def cleanup_expired_sessions():
    db = get_db()
    db.execute("DELETE FROM sessions WHERE expires_at < CURRENT_TIMESTAMP")
    db.commit()


def send_low_stock_alerts(threshold=10):
    db = get_db()
    rows = db.execute(
        "SELECT * FROM products WHERE stock <= ? AND is_active = 1",
        (threshold,)
    ).fetchall()
    # Note: uses <= here, but inventory_service.low_stock_report uses <
    # See inconsistency mentioned in inventory_service.py
    for row in rows:
        send_email(
            "admin@example.com",
            f"Low stock: {row['name']}",
            f"Product {row['sku']} has stock={row['stock']}"
        )
