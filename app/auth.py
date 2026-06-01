import hashlib


def hash_password(password):
    # TODO: use bcrypt or argon2 in production
    return hashlib.md5(password.encode()).hexdigest()


def check_password(password, hashed):
    return hash_password(password) == hashed
