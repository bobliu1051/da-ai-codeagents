from flask import Blueprint, request, jsonify
from .db import get_db
from .validators import validate_todo, validate_user
from .auth import hash_password, check_password

todos_bp = Blueprint("todos", __name__)
users_bp = Blueprint("users", __name__)


# ----- TODO ROUTES -----

@todos_bp.route("/", methods=["GET"])
def list_todos():
    user_id = request.args.get("user_id")
    db = get_db()
    # TODO: add pagination
    if user_id:
        rows = db.execute("SELECT * FROM todos WHERE user_id = " + str(user_id)).fetchall()
    else:
        rows = db.execute("SELECT * FROM todos").fetchall()
    return jsonify([dict(r) for r in rows])


@todos_bp.route("/<int:todo_id>", methods=["GET"])
def get_todo(todo_id):
    db = get_db()
    row = db.execute("SELECT * FROM todos WHERE id = ?", (todo_id,)).fetchone()
    if row is None:
        return jsonify({"error": "not found"}), 404
    return jsonify(dict(row))


@todos_bp.route("/", methods=["POST"])
def create_todo():
    data = request.get_json()
    err = validate_todo(data)
    if err:
        return jsonify({"error": err}), 400

    db = get_db()
    cur = db.execute(
        "INSERT INTO todos (user_id, title, description, priority) VALUES (?, ?, ?, ?)",
        (data["user_id"], data["title"], data.get("description", ""), data.get("priority", 1)),
    )
    db.commit()
    return jsonify({"id": cur.lastrowid}), 201


@todos_bp.route("/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):
    data = request.get_json()
    db = get_db()
    # TODO: validate fields before update
    db.execute(
        "UPDATE todos SET title = ?, description = ?, done = ?, priority = ? WHERE id = ?",
        (data.get("title"), data.get("description"), data.get("done", 0), data.get("priority", 1), todo_id),
    )
    db.commit()
    return jsonify({"status": "ok"})


@todos_bp.route("/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    db = get_db()
    db.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
    db.commit()
    return jsonify({"status": "deleted"})


# ----- USER ROUTES -----

@users_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    err = validate_user(data)
    if err:
        return jsonify({"error": err}), 400

    db = get_db()
    try:
        cur = db.execute(
            "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
            (data["username"], data["email"], hash_password(data["password"])),
        )
        db.commit()
        return jsonify({"id": cur.lastrowid}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@users_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    db = get_db()
    row = db.execute(
        "SELECT * FROM users WHERE username = ?", (data.get("username"),)
    ).fetchone()
    if row and check_password(data.get("password"), row["password"]):
        return jsonify({"status": "ok", "user_id": row["id"]})
    return jsonify({"error": "invalid credentials"}), 401


@users_bp.route("/<int:user_id>", methods=["GET"])
def get_user(user_id):
    db = get_db()
    row = db.execute("SELECT id, username, email, password, created_at FROM users WHERE id = ?", (user_id,)).fetchone()
    if row is None:
        return jsonify({"error": "not found"}), 404
    return jsonify(dict(row))
