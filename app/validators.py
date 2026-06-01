import re


def validate_todo(data):
    if not data:
        return "no data provided"
    if "title" not in data or not data["title"]:
        return "title is required"
    if "user_id" not in data:
        return "user_id is required"
    if len(data["title"]) > 200:
        return "title too long"
    return None


def validate_user(data):
    if not data:
        return "no data provided"
    if "username" not in data:
        return "username is required"
    if "password" not in data:
        return "password is required"
    if "email" not in data:
        return "email is required"
    # email format check
    if not re.match(r"^[^@]+@[^@]+\.[^@]+$", data["email"]):
        return "invalid email format"
    return None


def validate_email(email):
    # Different style than above - raises instead of returns
    if not email:
        raise ValueError("email required")
    if "@" not in email:
        raise ValueError("invalid email")
    return True
