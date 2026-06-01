# TODO API

A simple Flask-based REST API for managing todos and users.

## Setup

```bash
pip install -r requirements.txt
python run.py
```

The server runs on port 5000.

## Endpoints

### Todos
- `GET /api/todos/` - list all todos
- `GET /api/todos/<id>` - get a single todo
- `POST /api/todos/` - create a todo
- `PUT /api/todos/<id>` - update a todo
- `DELETE /api/todos/<id>` - delete a todo

### Users
- `POST /api/users/register` - create a new user
- `POST /api/users/login` - log in
- `GET /api/users/<id>` - get user info

## Validation Rules
- Todo titles must be non-empty and under 200 characters
- User emails must be valid format
- Passwords are required for users

## TODO
- Add pagination to list endpoints
- Move secret key to environment variable
- Better password hashing
