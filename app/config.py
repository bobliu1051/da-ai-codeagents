"""
Configuration loader.

Supports: development, staging, production.
Loads from environment variables, falls back to defaults.
"""
import os


DEFAULTS = {
    "DATABASE_URL": "sqlite:///app.db",
    "REDIS_URL": "redis://localhost:6379/0",
    "SECRET_KEY": "dev-key-not-for-prod",
    "JWT_SECRET": "another-dev-key",
    "JWT_EXPIRY_SECONDS": 3600,
    "RATE_LIMIT_PER_MINUTE": 60,
    "EMAIL_PROVIDER": "console",
    "PAYMENT_PROVIDER": "stripe",
    "STRIPE_KEY": "sk_test_xxx",
    "STRIPE_WEBHOOK_SECRET": "whsec_xxx",
    "CACHE_TTL_SECONDS": 300,
    "ENV": "development",
}


def get_config(env=None):
    env = env or os.getenv("APP_ENV", "development")
    config = dict(DEFAULTS)

    # Override from environment
    for key in DEFAULTS:
        if key in os.environ:
            config[key] = os.environ[key]

    # Env-specific overrides
    if env == "production":
        # TODO: enforce required env vars
        if config["SECRET_KEY"] == "dev-key-not-for-prod":
            print("WARNING: using default secret key in production")
        config["CACHE_TTL_SECONDS"] = 3600
    elif env == "staging":
        config["CACHE_TTL_SECONDS"] = 600

    config["ENV"] = env
    return config
