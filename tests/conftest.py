"""
Pytest configuration and fixtures for testing.
"""
import pytest
from app import create_app
from models import db, User


@pytest.fixture
def app():
    """
    Create and configure a test application instance.

    Returns:
        Flask: Test Flask application
    """
    app = create_app('testing')

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """
    Create a test client for the app.

    Args:
        app: The test Flask application

    Returns:
        FlaskClient: Test client for making requests
    """
    return app.test_client()


@pytest.fixture
def runner(app):
    """
    Create a test CLI runner for the app.

    Args:
        app: The test Flask application

    Returns:
        FlaskCliRunner: Test CLI runner
    """
    return app.test_cli_runner()


@pytest.fixture
def sample_user(app):
    """
    Create a sample user in the database for testing.

    Args:
        app: The test Flask application

    Returns:
        User: A test user instance
    """
    with app.app_context():
        user = User(username='testuser', password='testpassword123')
        db.session.add(user)
        db.session.commit()

        # Refresh the user to ensure it's attached to the session
        db.session.refresh(user)
        return user
