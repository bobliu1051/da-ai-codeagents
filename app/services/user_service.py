"""
User service - business logic for user operations.
"""
import hashlib
import secrets
from datetime import datetime, timedelta
from app.repositories.user_repo import UserRepository
from app.db import get_db
from app.utils.errors import ValidationError, AuthError, NotFoundError


class UserService:
    def __init__(self):
        self.repo = UserRepository()

    def register(self, email, password, username=None):
        if not email or "@" not in email:
            raise ValidationError("invalid email")
        if not password or len(password) < 8:
            raise ValidationError("password too short")

        existing = self.repo.find_by_email(email)
        if existing:
            raise ValidationError("email already registered")

        # PBKDF2 with salt
        salt = secrets.token_hex(16)
        hashed = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100_000).hex()
        password_hash = f"{salt}${hashed}"

        user_id = self.repo.create(email, password_hash, username=username)
        return self.repo.find_by_id(user_id)

    def authenticate(self, email, password):
        user = self.repo.find_by_email(email)
        if not user:
            raise AuthError("invalid credentials")

        # password_hash is "salt$hashed"
        try:
            salt, stored_hash = user.password_hash.split("$", 1)
        except (ValueError, AttributeError):
            raise AuthError("invalid credentials")

        computed = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100_000).hex()
        if computed != stored_hash:
            raise AuthError("invalid credentials")

        return user

    def create_session(self, user_id):
        token = secrets.token_urlsafe(32)
        expires = datetime.utcnow() + timedelta(seconds=3600)
        db = get_db()
        db.execute(
            "INSERT INTO sessions (token, user_id, expires_at) VALUES (?, ?, ?)",
            (token, user_id, expires.isoformat())
        )
        db.commit()
        return token

    def get_by_id(self, user_id):
        user = self.repo.find_by_id(user_id)
        if not user:
            raise NotFoundError("user not found")
        return user
