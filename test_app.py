"""
Unit tests for app.py - OpenAI API integration

These tests use mocking to avoid making real API calls during testing.
Run with: python -m pytest test_app.py -v
or: python -m unittest test_app.py
"""

import unittest
from unittest.mock import patch, MagicMock, call
import sys
from io import StringIO


class TestOpenAIIntegration(unittest.TestCase):
    """Test suite for OpenAI API integration in app.py"""

    def setUp(self):
        """Set up test fixtures before each test method"""
        self.mock_response = MagicMock()
        self.mock_response.choices = [MagicMock()]
        self.mock_response.choices[0].message.content = "Test haiku response"

    @patch('app.OpenAI')
    def test_openai_client_initialization(self, mock_openai_class):
        """Test that OpenAI client is initialized with correct API key"""
        # Import app to trigger initialization
        import app

        # Verify OpenAI was called with the API key
        mock_openai_class.assert_called_once_with(
            api_key="sk-1234567890abcdefghijklmnopqrstuvwxYZABCDEF"
        )

    @patch('app.client')
    def test_chat_completion_request_structure(self, mock_client):
        """Test that chat completion is called with correct parameters"""
        mock_client.chat.completions.create.return_value = self.mock_response

        # Re-import to execute the code
        import importlib
        import app
        importlib.reload(app)

        # Verify the chat completion was called with correct structure
        mock_client.chat.completions.create.assert_called_once()
        call_kwargs = mock_client.chat.completions.create.call_args[1]

        self.assertEqual(call_kwargs['model'], 'gpt-4o-mini')
        self.assertEqual(len(call_kwargs['messages']), 2)

    @patch('builtins.print')
    @patch('app.client')
    def test_response_output(self, mock_client, mock_print):
        """Test that the response content is printed correctly"""
        mock_client.chat.completions.create.return_value = self.mock_response

        # Re-import to execute the code
        import importlib
        import app
        importlib.reload(app)

        # Verify print was called with the response content
        mock_print.assert_called_with("Test haiku response")

    def test_api_key_format(self):
        """Test that the API key follows expected format"""
        import app

        # Check API key is a string and has expected prefix
        self.assertIsInstance(app.api_key, str)
        self.assertTrue(app.api_key.startswith('sk-'))
        self.assertGreater(len(app.api_key), 20)

    @patch('app.client')
    def test_model_specification(self, mock_client):
        """Test that the correct model is specified"""
        mock_client.chat.completions.create.return_value = self.mock_response

        import importlib
        import app
        importlib.reload(app)

        call_kwargs = mock_client.chat.completions.create.call_args[1]
        self.assertEqual(call_kwargs['model'], 'gpt-4o-mini')

    @patch('app.client')
    def test_message_roles(self, mock_client):
        """Test that messages have correct roles (system and user)"""
        mock_client.chat.completions.create.return_value = self.mock_response

        import importlib
        import app
        importlib.reload(app)

        call_kwargs = mock_client.chat.completions.create.call_args[1]
        messages = call_kwargs['messages']

        self.assertEqual(messages[0]['role'], 'system')
        self.assertEqual(messages[1]['role'], 'user')

    @patch('app.client')
    def test_system_message_content(self, mock_client):
        """Test that system message has correct content"""
        mock_client.chat.completions.create.return_value = self.mock_response

        import importlib
        import app
        importlib.reload(app)

        call_kwargs = mock_client.chat.completions.create.call_args[1]
        messages = call_kwargs['messages']

        self.assertEqual(
            messages[0]['content'],
            'You are a helpful assistant.'
        )

    @patch('app.client')
    def test_user_message_content(self, mock_client):
        """Test that user message contains expected prompt"""
        mock_client.chat.completions.create.return_value = self.mock_response

        import importlib
        import app
        importlib.reload(app)

        call_kwargs = mock_client.chat.completions.create.call_args[1]
        messages = call_kwargs['messages']

        self.assertIn('haiku', messages[1]['content'].lower())
        self.assertIn('debugging', messages[1]['content'].lower())
        self.assertIn('Python', messages[1]['content'])


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error scenarios"""

    @patch('app.client')
    def test_empty_response_content(self, mock_client):
        """Test handling of empty response content"""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = ""
        mock_client.chat.completions.create.return_value = mock_response

        with patch('builtins.print') as mock_print:
            import importlib
            import app
            importlib.reload(app)

            # Should still call print, even with empty string
            mock_print.assert_called_once_with("")

    @patch('app.client')
    def test_api_call_exception_propagation(self, mock_client):
        """Test that API exceptions are propagated (not caught)"""
        mock_client.chat.completions.create.side_effect = Exception("API Error")

        with self.assertRaises(Exception) as context:
            import importlib
            import app
            importlib.reload(app)

        self.assertIn("API Error", str(context.exception))

    @patch('app.OpenAI')
    def test_client_initialization_with_api_key(self, mock_openai_class):
        """Test that client is properly initialized as OpenAI instance"""
        mock_openai_instance = MagicMock()
        mock_openai_class.return_value = mock_openai_instance

        import importlib
        import app
        importlib.reload(app)

        # Verify the client is the instance returned by OpenAI()
        self.assertEqual(app.client, mock_openai_instance)


if __name__ == '__main__':
    unittest.main()
