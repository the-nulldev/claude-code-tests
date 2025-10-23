"""
Authentication utilities and decorators.
"""
from functools import wraps
from flask import jsonify, request
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from models import User, db


def token_required(f):
    """
    Decorator to protect routes that require authentication.

    Usage:
        @app.route('/protected')
        @token_required
        def protected_route():
            return jsonify({"message": "Access granted"})
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            verify_jwt_in_request()
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({"error": "Invalid or missing token", "details": str(e)}), 401

    return decorated_function


def get_current_user():
    """
    Get the current authenticated user from the JWT token.

    Returns:
        User: The authenticated user object, or None if not found
    """
    try:
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        return User.query.get(user_id)
    except Exception:
        return None


def validate_registration_data(data):
    """
    Validate user registration data.

    Args:
        data (dict): Registration data containing username and password

    Returns:
        tuple: (is_valid, error_message)
    """
    if not data:
        return False, "No data provided"

    username = data.get('username', '').strip()
    password = data.get('password', '')

    if not username:
        return False, "Username is required"

    if len(username) < 3:
        return False, "Username must be at least 3 characters long"

    if len(username) > 80:
        return False, "Username must be at most 80 characters long"

    if not password:
        return False, "Password is required"

    if len(password) < 6:
        return False, "Password must be at least 6 characters long"

    # Check if username already exists
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return False, "Username already exists"

    return True, None


def validate_login_data(data):
    """
    Validate user login data.

    Args:
        data (dict): Login data containing username and password

    Returns:
        tuple: (is_valid, error_message)
    """
    if not data:
        return False, "No data provided"

    username = data.get('username')
    password = data.get('password')

    if not username:
        return False, "Username is required"

    if not password:
        return False, "Password is required"

    return True, None
