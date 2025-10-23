"""
Database models for the authentication system.
"""
from flask_sqlalchemy import SQLAlchemy
import bcrypt

db = SQLAlchemy()


class User(db.Model):
    """User model for authentication."""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128), nullable=False)

    def __init__(self, username, password):
        """
        Initialize a new user with username and password.

        Args:
            username (str): The username for the user
            password (str): The plain text password (will be hashed)
        """
        self.username = username
        self.set_password(password)

    def set_password(self, password):
        """
        Hash and set the user's password.

        Args:
            password (str): The plain text password to hash
        """
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password_bytes, salt).decode('utf-8')

    def check_password(self, password):
        """
        Verify a password against the stored hash.

        Args:
            password (str): The plain text password to verify

        Returns:
            bool: True if password matches, False otherwise
        """
        password_bytes = password.encode('utf-8')
        password_hash_bytes = self.password_hash.encode('utf-8')
        return bcrypt.checkpw(password_bytes, password_hash_bytes)

    def to_dict(self):
        """
        Convert user object to dictionary (excluding password).

        Returns:
            dict: User data without password hash
        """
        return {
            'id': self.id,
            'username': self.username
        }

    def __repr__(self):
        return f'<User {self.username}>'
