"""
Migration 001: initial schema.

NOTE: This migration file exists but isn't actually applied by any tool.
The schema in app/db.py is the actual source of truth. These files were
created when we were planning to switch to Alembic but never finished.
"""

UP = """
-- See app/db.py SCHEMA constant for the actual applied schema.
"""

DOWN = """
DROP TABLE IF EXISTS audit_log;
DROP TABLE IF EXISTS sessions;
DROP TABLE IF EXISTS inventory_log;
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS users;
"""
