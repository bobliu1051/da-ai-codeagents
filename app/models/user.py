from app.models import BaseModel


class User(BaseModel):
    table_name = "users"

    def is_admin(self):
        return getattr(self, "role", None) == "admin"

    def to_public_dict(self):
        # Strips password_hash
        d = self.to_dict()
        d.pop("password_hash", None)
        return d
