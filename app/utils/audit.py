"""
Audit log helper.
"""
import json
from app.db import get_db


def log_action(user_id, action, resource_type=None, resource_id=None, metadata=None):
    db = get_db()
    db.execute(
        "INSERT INTO audit_log (user_id, action, resource_type, resource_id, metadata) "
        "VALUES (?, ?, ?, ?, ?)",
        (user_id, action, resource_type, resource_id, json.dumps(metadata) if metadata else None)
    )
    db.commit()
