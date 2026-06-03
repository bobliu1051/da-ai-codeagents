"""
User repository - data access layer.

NOTE: Not all code uses repositories. The legacy code in app/legacy/ uses
raw SQL inline. Mid-project we moved to repositories for new endpoints.
"""
from app.db import get_db
from app.models.user import User


class UserRepository:
    def find_by_id(self, user_id):
        db = get_db()
        row = db.execute(
            "SELECT * FROM users WHERE id = ? AND deleted_at IS NULL",
            (user_id,)
        ).fetchone()
        return User.from_row(row)

    def find_by_email(self, email):
        db = get_db()
        row = db.execute(
            "SELECT * FROM users WHERE email = ?",
            (email,)
        ).fetchone()
        return User.from_row(row)

    def create(self, email, password_hash, username=None, role="user"):
        db = get_db()
        cur = db.execute(
            "INSERT INTO users (email, password_hash, username, role) VALUES (?, ?, ?, ?)",
            (email, password_hash, username, role)
        )
        db.commit()
        return cur.lastrowid

    def soft_delete(self, user_id):
        db = get_db()
        db.execute(
            "UPDATE users SET deleted_at = CURRENT_TIMESTAMP WHERE id = ?",
            (user_id,)
        )
        db.commit()

    def list_all(self, include_deleted=False):
        db = get_db()
        if include_deleted:
            rows = db.execute("SELECT * FROM users").fetchall()
        else:
            rows = db.execute("SELECT * FROM users WHERE deleted_at IS NULL").fetchall()
        return [User.from_row(r) for r in rows]
