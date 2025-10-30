import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
from io import StringIO


class TestAppOpenAI(unittest.TestCase):
    """Unit tests for app.py OpenAI integration."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_api_key = "sk-1234567890abcdefghijklmnopqrstuvwxYZABCDEF"
        self.mock_response_content = "Debugging awaits,\nPrint statements guide the way,\nBugs vanish at dawn."

    @patch('openai.OpenAI')
    def test_openai_client_initialization(self, mock_openai_class):
        """Test that OpenAI client is initialized with the correct API key."""
        mock_client = Mock()
        mock_openai_class.return_value = mock_client

        # Import app which will initialize the client
        with patch('builtins.print'):
            import importlib
            if 'app' in sys.modules:
                importlib.reload(sys.modules['app'])
            else:
                import app

        # Verify OpenAI was called with the API key
        mock_openai_class.assert_called_once_with(api_key=self.mock_api_key)

    @patch('openai.OpenAI')
    def test_chat_completion_request(self, mock_openai_class):
        """Test that chat completion is requested with correct parameters."""
        mock_client = Mock()
        mock_response = Mock()
        mock_choice = Mock()
        mock_message = Mock()
        mock_message.content = self.mock_response_content
        mock_choice.message = mock_message
        mock_response.choices = [mock_choice]
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai_class.return_value = mock_client

        with patch('builtins.print') as mock_print:
            import importlib
            if 'app' in sys.modules:
                importlib.reload(sys.modules['app'])
            else:
                import app

        # Verify the chat completion was called with correct parameters
        mock_client.chat.completions.create.assert_called_once_with(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Write a haiku about debugging Python code."},
            ]
        )

    @patch('openai.OpenAI')
    def test_response_printing(self, mock_openai_class):
        """Test that the response content is printed correctly."""
        mock_client = Mock()
        mock_response = Mock()
        mock_choice = Mock()
        mock_message = Mock()
        mock_message.content = self.mock_response_content
        mock_choice.message = mock_message
        mock_response.choices = [mock_choice]
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai_class.return_value = mock_client

        with patch('builtins.print') as mock_print:
            import importlib
            if 'app' in sys.modules:
                importlib.reload(sys.modules['app'])
            else:
                import app

        # Verify print was called with the response content
        mock_print.assert_called_once_with(self.mock_response_content)

    @patch('openai.OpenAI')
    def test_api_error_handling(self, mock_openai_class):
        """Test behavior when OpenAI API raises an exception."""
        mock_client = Mock()
        mock_client.chat.completions.create.side_effect = Exception("API Error: Rate limit exceeded")
        mock_openai_class.return_value = mock_client

        # The current app.py doesn't handle exceptions, so this will raise
        with self.assertRaises(Exception) as context:
            import importlib
            if 'app' in sys.modules:
                importlib.reload(sys.modules['app'])
            else:
                import app

        self.assertIn("API Error", str(context.exception))

    @patch('openai.OpenAI')
    def test_empty_response_handling(self, mock_openai_class):
        """Test handling of empty response from API."""
        mock_client = Mock()
        mock_response = Mock()
        mock_choice = Mock()
        mock_message = Mock()
        mock_message.content = ""
        mock_choice.message = mock_message
        mock_response.choices = [mock_choice]
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai_class.return_value = mock_client

        with patch('builtins.print') as mock_print:
            import importlib
            if 'app' in sys.modules:
                importlib.reload(sys.modules['app'])
            else:
                import app

        # Verify print was called even with empty content
        mock_print.assert_called_once_with("")

    @patch('openai.OpenAI')
    def test_response_with_multiple_choices(self, mock_openai_class):
        """Test that first choice is used when multiple choices are returned."""
        mock_client = Mock()
        mock_response = Mock()

        # Create multiple choices
        mock_choice1 = Mock()
        mock_message1 = Mock()
        mock_message1.content = "First haiku"
        mock_choice1.message = mock_message1

        mock_choice2 = Mock()
        mock_message2 = Mock()
        mock_message2.content = "Second haiku"
        mock_choice2.message = mock_message2

        mock_response.choices = [mock_choice1, mock_choice2]
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai_class.return_value = mock_client

        with patch('builtins.print') as mock_print:
            import importlib
            if 'app' in sys.modules:
                importlib.reload(sys.modules['app'])
            else:
                import app

        # Verify only first choice is printed
        mock_print.assert_called_once_with("First haiku")

    def test_api_key_format(self):
        """Test that the API key has the expected format."""
        # This is a basic check - in real scenarios, you'd use env variables
        self.assertTrue(self.mock_api_key.startswith("sk-"))
        self.assertEqual(len(self.mock_api_key), 51)

    @patch('openai.OpenAI')
    def test_model_parameter(self, mock_openai_class):
        """Test that the correct model is specified in the request."""
        mock_client = Mock()
        mock_response = Mock()
        mock_choice = Mock()
        mock_message = Mock()
        mock_message.content = "Test response"
        mock_choice.message = mock_message
        mock_response.choices = [mock_choice]
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai_class.return_value = mock_client

        with patch('builtins.print'):
            import importlib
            if 'app' in sys.modules:
                importlib.reload(sys.modules['app'])
            else:
                import app

        # Extract the model parameter from the call
        call_kwargs = mock_client.chat.completions.create.call_args[1]
        self.assertEqual(call_kwargs['model'], "gpt-4o-mini")

    @patch('openai.OpenAI')
    def test_message_structure(self, mock_openai_class):
        """Test that messages are structured correctly with roles and content."""
        mock_client = Mock()
        mock_response = Mock()
        mock_choice = Mock()
        mock_message = Mock()
        mock_message.content = "Test response"
        mock_choice.message = mock_message
        mock_response.choices = [mock_choice]
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai_class.return_value = mock_client

        with patch('builtins.print'):
            import importlib
            if 'app' in sys.modules:
                importlib.reload(sys.modules['app'])
            else:
                import app

        # Extract the messages parameter
        call_kwargs = mock_client.chat.completions.create.call_args[1]
        messages = call_kwargs['messages']

        # Verify structure
        self.assertEqual(len(messages), 2)
        self.assertEqual(messages[0]['role'], 'system')
        self.assertIn('assistant', messages[0]['content'])
        self.assertEqual(messages[1]['role'], 'user')
        self.assertIn('haiku', messages[1]['content'])


if __name__ == '__main__':
    unittest.main()
