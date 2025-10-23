"""
Unit tests for authentication functionality.
"""
import json
import pytest
from models import User, db


class TestRegistration:
    """Test cases for user registration."""

    def test_register_success(self, client):
        """Test successful user registration."""
        response = client.post('/register',
                              data=json.dumps({
                                  'username': 'newuser',
                                  'password': 'securepassword123'
                              }),
                              content_type='application/json')

        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['message'] == 'User created successfully'
        assert data['user']['username'] == 'newuser'
        assert 'id' in data['user']

    def test_register_duplicate_username(self, client, sample_user):
        """Test registration with existing username."""
        response = client.post('/register',
                              data=json.dumps({
                                  'username': 'testuser',
                                  'password': 'anotherpassword'
                              }),
                              content_type='application/json')

        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'already exists' in data['error'].lower()

    def test_register_missing_username(self, client):
        """Test registration without username."""
        response = client.post('/register',
                              data=json.dumps({
                                  'password': 'password123'
                              }),
                              content_type='application/json')

        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'username' in data['error'].lower()

    def test_register_missing_password(self, client):
        """Test registration without password."""
        response = client.post('/register',
                              data=json.dumps({
                                  'username': 'newuser'
                              }),
                              content_type='application/json')

        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'password' in data['error'].lower()

    def test_register_short_username(self, client):
        """Test registration with username too short."""
        response = client.post('/register',
                              data=json.dumps({
                                  'username': 'ab',
                                  'password': 'password123'
                              }),
                              content_type='application/json')

        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'at least 3 characters' in data['error'].lower()

    def test_register_short_password(self, client):
        """Test registration with password too short."""
        response = client.post('/register',
                              data=json.dumps({
                                  'username': 'newuser',
                                  'password': '12345'
                              }),
                              content_type='application/json')

        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'at least 6 characters' in data['error'].lower()

    def test_register_empty_data(self, client):
        """Test registration with no data."""
        response = client.post('/register',
                              data=json.dumps({}),
                              content_type='application/json')

        assert response.status_code == 400


class TestLogin:
    """Test cases for user login."""

    def test_login_success(self, client, sample_user):
        """Test successful login."""
        response = client.post('/login',
                              data=json.dumps({
                                  'username': 'testuser',
                                  'password': 'testpassword123'
                              }),
                              content_type='application/json')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['message'] == 'Login successful'
        assert 'access_token' in data
        assert data['user']['username'] == 'testuser'

    def test_login_wrong_password(self, client, sample_user):
        """Test login with incorrect password."""
        response = client.post('/login',
                              data=json.dumps({
                                  'username': 'testuser',
                                  'password': 'wrongpassword'
                              }),
                              content_type='application/json')

        assert response.status_code == 401
        data = json.loads(response.data)
        assert 'invalid' in data['error'].lower()

    def test_login_nonexistent_user(self, client):
        """Test login with non-existent username."""
        response = client.post('/login',
                              data=json.dumps({
                                  'username': 'nonexistent',
                                  'password': 'password123'
                              }),
                              content_type='application/json')

        assert response.status_code == 401
        data = json.loads(response.data)
        assert 'invalid' in data['error'].lower()

    def test_login_missing_username(self, client):
        """Test login without username."""
        response = client.post('/login',
                              data=json.dumps({
                                  'password': 'password123'
                              }),
                              content_type='application/json')

        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'username' in data['error'].lower()

    def test_login_missing_password(self, client):
        """Test login without password."""
        response = client.post('/login',
                              data=json.dumps({
                                  'username': 'testuser'
                              }),
                              content_type='application/json')

        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'password' in data['error'].lower()


class TestProtectedRoute:
    """Test cases for protected routes."""

    def test_profile_with_valid_token(self, client, sample_user):
        """Test accessing profile with valid JWT token."""
        # First, login to get token
        login_response = client.post('/login',
                                    data=json.dumps({
                                        'username': 'testuser',
                                        'password': 'testpassword123'
                                    }),
                                    content_type='application/json')

        token = json.loads(login_response.data)['access_token']

        # Access protected route with token
        response = client.get('/profile',
                             headers={'Authorization': f'Bearer {token}'})

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['message'] == 'Profile retrieved successfully'
        assert data['user']['username'] == 'testuser'

    def test_profile_without_token(self, client):
        """Test accessing profile without token."""
        response = client.get('/profile')

        assert response.status_code == 401
        data = json.loads(response.data)
        assert 'token' in data['error'].lower()

    def test_profile_with_invalid_token(self, client):
        """Test accessing profile with invalid token."""
        response = client.get('/profile',
                             headers={'Authorization': 'Bearer invalid_token_here'})

        assert response.status_code == 401
        data = json.loads(response.data)
        assert 'token' in data['error'].lower()


class TestPasswordHashing:
    """Test cases for password hashing."""

    def test_password_is_hashed(self, app):
        """Test that passwords are properly hashed."""
        with app.app_context():
            user = User(username='hashtest', password='plainpassword')
            db.session.add(user)
            db.session.commit()

            # Password should be hashed, not stored in plain text
            assert user.password_hash != 'plainpassword'
            assert len(user.password_hash) > 0

    def test_password_verification(self, app):
        """Test password verification method."""
        with app.app_context():
            user = User(username='verifytest', password='correctpassword')
            db.session.add(user)
            db.session.commit()

            # Correct password should verify
            assert user.check_password('correctpassword') is True

            # Wrong password should not verify
            assert user.check_password('wrongpassword') is False


class TestAPI:
    """Test cases for general API functionality."""

    def test_index_endpoint(self, client):
        """Test the index/health check endpoint."""
        response = client.get('/')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'message' in data
        assert 'endpoints' in data
