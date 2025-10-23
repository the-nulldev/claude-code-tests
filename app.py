"""
Main Flask application with authentication routes.
"""
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity
from config import config
from models import db, User
from auth import token_required, get_current_user, validate_registration_data, validate_login_data
import os


def create_app(config_name='default'):
    """
    Application factory pattern for creating Flask app.

    Args:
        config_name (str): Configuration name (development, production, testing)

    Returns:
        Flask: Configured Flask application
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize extensions
    db.init_app(app)
    jwt = JWTManager(app)

    # Create database tables
    with app.app_context():
        db.create_all()

    # Routes
    @app.route('/')
    def index():
        """Health check endpoint."""
        return jsonify({
            "message": "Authentication API is running",
            "endpoints": {
                "register": "/register [POST]",
                "login": "/login [POST]",
                "profile": "/profile [GET] (protected)"
            }
        })

    @app.route('/register', methods=['POST'])
    def register():
        """
        Register a new user.

        Request Body:
            {
                "username": "string",
                "password": "string"
            }

        Returns:
            201: User created successfully
            400: Invalid input data
            409: Username already exists
        """
        try:
            data = request.get_json()

            # Validate input data
            is_valid, error_message = validate_registration_data(data)
            if not is_valid:
                return jsonify({"error": error_message}), 400

            username = data['username'].strip()
            password = data['password']

            # Create new user
            user = User(username=username, password=password)
            db.session.add(user)
            db.session.commit()

            return jsonify({
                "message": "User created successfully",
                "user": user.to_dict()
            }), 201

        except Exception as e:
            db.session.rollback()
            return jsonify({"error": "Registration failed", "details": str(e)}), 500

    @app.route('/login', methods=['POST'])
    def login():
        """
        Authenticate a user and return a JWT token.

        Request Body:
            {
                "username": "string",
                "password": "string"
            }

        Returns:
            200: Authentication successful with token
            400: Invalid input data
            401: Invalid credentials
        """
        try:
            data = request.get_json()

            # Validate input data
            is_valid, error_message = validate_login_data(data)
            if not is_valid:
                return jsonify({"error": error_message}), 400

            username = data['username']
            password = data['password']

            # Find user
            user = User.query.filter_by(username=username).first()

            # Verify password
            if not user or not user.check_password(password):
                return jsonify({"error": "Invalid username or password"}), 401

            # Create access token
            access_token = create_access_token(identity=user.id)

            return jsonify({
                "message": "Login successful",
                "access_token": access_token,
                "user": user.to_dict()
            }), 200

        except Exception as e:
            return jsonify({"error": "Login failed", "details": str(e)}), 500

    @app.route('/profile', methods=['GET'])
    @token_required
    def profile():
        """
        Get the current user's profile (protected route).

        Headers:
            Authorization: Bearer <token>

        Returns:
            200: User profile data
            401: Unauthorized (invalid or missing token)
        """
        try:
            user = get_current_user()

            if not user:
                return jsonify({"error": "User not found"}), 404

            return jsonify({
                "message": "Profile retrieved successfully",
                "user": user.to_dict()
            }), 200

        except Exception as e:
            return jsonify({"error": "Failed to retrieve profile", "details": str(e)}), 500

    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Endpoint not found"}), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({"error": "Method not allowed"}), 405

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({"error": "Internal server error"}), 500

    return app


if __name__ == '__main__':
    # Get configuration from environment variable or use default
    env = os.environ.get('FLASK_ENV', 'development')
    app = create_app(env)
    app.run(debug=True, host='0.0.0.0', port=5000)
