import unittest
from unittest.mock import patch, MagicMock
import app


class TestOpenAIIntegration(unittest.TestCase):
    """Test suite for the OpenAI API integration in app.py"""

    @patch('app.OpenAI')
    def test_openai_client_initialization(self, mock_openai):
        """Test that the OpenAI client is initialized with the correct API key"""
        # Reload the module to trigger initialization with our mock
        import importlib
        importlib.reload(app)

        # Verify OpenAI was called with the api_key
        mock_openai.assert_called_once_with(api_key="sk-1234567890abcdefghijklmnopqrstuvwxYZABCDEF")

    @patch('app.client')
    def test_chat_completion_request_structure(self, mock_client):
        """Test that the chat completion is called with correct parameters"""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Test haiku response"
        mock_client.chat.completions.create.return_value = mock_response

        # Reload the module to execute the API call with our mock
        import importlib
        with patch('builtins.print'):  # Suppress print output during test
            importlib.reload(app)

        # Verify the API call was made with correct parameters
        mock_client.chat.completions.create.assert_called_once_with(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Write a haiku about debugging Python code."},
            ]
        )

    @patch('app.client')
    @patch('builtins.print')
    def test_response_output(self, mock_print, mock_client):
        """Test that the response content is printed correctly"""
        # Setup mock response
        expected_content = "Code breaks at night\nStack traces guide the way home\nBugs fixed by morning"
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = expected_content
        mock_client.chat.completions.create.return_value = mock_response

        # Reload the module to execute with our mock
        import importlib
        importlib.reload(app)

        # Verify print was called with the response content
        mock_print.assert_called_once_with(expected_content)

    def test_api_key_format(self):
        """Test that the API key follows the expected format"""
        # Check that api_key exists and starts with expected prefix
        self.assertTrue(hasattr(app, 'api_key'))
        self.assertIsInstance(app.api_key, str)
        self.assertTrue(app.api_key.startswith('sk-'))
        self.assertGreater(len(app.api_key), 20)

    @patch('app.client')
    def test_model_specification(self, mock_client):
        """Test that the correct model is specified"""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Test"
        mock_client.chat.completions.create.return_value = mock_response

        import importlib
        with patch('builtins.print'):
            importlib.reload(app)

        # Extract the model argument from the call
        call_args = mock_client.chat.completions.create.call_args
        self.assertEqual(call_args.kwargs['model'], 'gpt-4o-mini')

    @patch('app.client')
    def test_message_roles(self, mock_client):
        """Test that messages have correct roles (system and user)"""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Test"
        mock_client.chat.completions.create.return_value = mock_response

        import importlib
        with patch('builtins.print'):
            importlib.reload(app)

        # Extract messages from the call
        call_args = mock_client.chat.completions.create.call_args
        messages = call_args.kwargs['messages']

        self.assertEqual(len(messages), 2)
        self.assertEqual(messages[0]['role'], 'system')
        self.assertEqual(messages[1]['role'], 'user')

    @patch('app.client')
    def test_system_message_content(self, mock_client):
        """Test that the system message sets up the assistant correctly"""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Test"
        mock_client.chat.completions.create.return_value = mock_response

        import importlib
        with patch('builtins.print'):
            importlib.reload(app)

        call_args = mock_client.chat.completions.create.call_args
        messages = call_args.kwargs['messages']

        self.assertEqual(messages[0]['content'], 'You are a helpful assistant.')


if __name__ == '__main__':
    unittest.main()
