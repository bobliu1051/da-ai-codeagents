"""
Migration 002: add audit_log table.

UNUSED - see migrations/001_initial.py note.
"""

UP = """
CREATE TABLE IF NOT EXISTS audit_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    action TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

DOWN = "DROP TABLE audit_log;"
