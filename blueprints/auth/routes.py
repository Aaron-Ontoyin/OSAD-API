import os
from functools import wraps

from flask import request, jsonify
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt,
    current_user
)

from .models import User
from .utils import generate_password_reset_token
from utils import jwt, redis_client, db, bcrypt, send_email


INVALID_USER_MESSAGE = "Invalid user"


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    jti = jwt_payload["jti"]
    token_in_redis = redis_client.get(jti)
    return token_in_redis is not None


def register():
    username = request.json.get("username")
    email = request.json.get("email")
    password = request.json.get("password")

    missing_fields = [
        field
        for field in ["username", "email", "password"]
        if not request.json.get(field)
    ]
    if missing_fields:
        return jsonify({"message": f"Missing fields: {', '.join(missing_fields)}"}), 400

    existing_user = User.query.filter(
        (User.username == username) | (User.email == email)
    ).first()
    if existing_user:
        return jsonify({"message": "Username or email already exists"}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
    user = User(username=username, email=email, password=hashed_password)
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"})


def login():
    username = request.json.get("username")
    password = request.json.get("password")

    if not username or not password:
        return jsonify({"message": "Missing required fields"}), 400

    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"message": "Invalid username"}), 401
    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({"message": "Invalid password"}), 401

    access_token = create_access_token(identity=user.id, fresh=True)
    refresh_token = create_refresh_token(identity=user.id)

    return (
        jsonify(
            {
                "message": "Login successful",
                "access_token": access_token,
                "refresh_token": refresh_token,
            }
        ),
        200,
    )


@jwt_required(verify_type=False)
def logout():
    """
    Revokes the current JWT access token and associated refresh tokens by adding them to the revoked tokens list.

    Returns:
        tuple: A JSON response indicating successful logout with HTTP status code 200,
               or an error message with HTTP status code 401 if no current user is found.
    """
    token = get_jwt()
    jti = token["jti"]
    ttype = token["type"]
    default_access_ex = os.environ.get("JWT_ACCESS_TOKEN_EXPIRES") or (60 * 60)
    default_refresh_ex = os.environ.get("JWT_REFRESH_TOKEN_EXPIRES") or (
        60 * 60 * 24 * 30
    )
    default_ex = default_access_ex if ttype == "access" else default_refresh_ex
    redis_client.set(
        jti, "", ex=os.environ.get("JWT_BLOCKLIST_TOKEN_EXPIRES") or default_ex
    )

    return jsonify(msg=f"{ttype.capitalize()} token successfully revoked")


@jwt_required()
def get_user():
    """
    Returns the current user.
    """
    user_data = {
        "username": current_user.username,
        "email": current_user.email,
        "firstname": current_user.firstname,
        "lastname": current_user.lastname,
        "phone": current_user.phone,
        "is_admin": current_user.is_admin,
        "remaining_requests": current_user.remaining_requests,
    }
    return jsonify(user_data), 200


@jwt_required()
def update_user():
    """
    Updates the current user's data

    Returns:
        tuple: A JSON response with the updated user's data and an HTTP status code.
    """

    username = request.json.get("username")
    email = request.json.get("email")
    firstname = request.json.get("firstname")
    lastname = request.json.get("lastname")
    phone = request.json.get("phone")

    if username:
        current_user.username = username
    if email:
        current_user.email = email
    if firstname:
        current_user.firstname = firstname
    if lastname:
        current_user.lastname = lastname
    if phone:
        current_user.phone = phone
    db.session.commit()

    return jsonify({"message": "User updated successfully"}), 200


@jwt_required()
def delete_user():
    """
    Deletes the current user.

    Returns:
        tuple: A JSON response with a message and an HTTP status code.
    """

    db.session.delete(current_user)
    db.session.commit()

    return (jsonify({"message": f"User deleted successfully"}), 200)


@jwt_required()
def change_password():
    """
    Changes the current user's password.

    Returns:
        tuple: A JSON response with a message and an HTTP status code.
    """
    old_password = request.json.get("old_password")
    new_password = request.json.get("new_password")

    if not old_password or not new_password:
        return jsonify({"message": "Missing required fields"}), 400

    if not bcrypt.check_password_hash(current_user.password, old_password):
        return jsonify({"message": "Invalid old password"}), 401

    hashed_password = bcrypt.generate_password_hash(new_password).decode("utf-8")
    current_user.password = hashed_password
    db.session.commit()

    return jsonify({"message": "Password changed successfully"}), 200


def get_password_reset_token():
    """
    Resets the user's password.
    """
    email = request.json.get("email")
    if not email:
        return jsonify({"message": "Missing required field: email"}), 400
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"message": f"User not found with email {email}"}), 404

    token = generate_password_reset_token()
    redis_client.set(token, user.id, ex=60 * 30)

    email_body = f"""
    Use the token below to reset your password: {token}
    This token will expire in 30 minutes!
    """
    send_email(user, "OSAD Password Reset", email_body)

    return jsonify({"message": "Password reset email sent"}), 200


def reset_password():
    """
    Resets the user's password.
    """
    token = request.json.get("token")
    password = request.json.get("password")
    if not token or not password:
        return jsonify({"message": "Missing required fields"}), 400

    user_id = redis_client.get(token)
    if not user_id:
        return jsonify({"message": "Invalid or expired token"}), 400

    user = User.query.get(user_id)

    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
    user.password = hashed_password
    db.session.commit()

    redis_client.delete(token)

    return jsonify({"message": "Password reset successful"}), 200

@jwt_required(refresh=True)
def refresh_token():
    """
    Refreshes the access token.
    """
    access_token = create_access_token(identity=current_user.id, fresh=False)
    return jsonify({"access_token": access_token}), 200


# Admin routes
def admin_required(func):
    """
    A decorator that checks if the current user is an admin.

    Args:
        func (function): The function to be decorated.

    Returns:
        function: The decorated function.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_admin:
            return jsonify({"message": "Unauthorized. Admins only"}), 403
        return func(current_user, *args, **kwargs)

    return wrapper


@jwt_required()
@admin_required
def get_all_users():
    """
    Retrieves all user records if the requester is an admin.

    Returns:
        tuple: A JSON response with all users' data and an HTTP status code.
    """
    users = User.query.all()
    user_data = [{"username": user.username, "email": user.email} for user in users]

    return jsonify({"users": user_data}), 200


@jwt_required()
@admin_required
def make_admin(user_id):
    """
    Makes the current user an admin.

    Returns:
        tuple: A JSON response with a message and an HTTP status code.
    """
    user = User.query.get(user_id)
    user.is_admin = True
    db.session.commit()
    return jsonify({"message": f"User with id {user_id} promoted to admin"}), 200
