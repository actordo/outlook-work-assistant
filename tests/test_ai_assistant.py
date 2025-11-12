"""Tests for AI assistant module."""
import pytest
from unittest.mock import Mock, patch, MagicMock
from ai_assistant import AIAssistant


class TestAIAssistant:
    """Test AIAssistant class."""
    
    @patch('ai_assistant.OpenAI')
    @patch('ai_assistant.config')
    def test_assistant_initialization(self, mock_config, mock_openai):
        """Test AIAssistant initialization."""
        mock_config.openai.api_key = 'test-key'
        mock_config.openai.model = 'gpt-4'
        mock_config.openai.temperature = 0.7
        
        assistant = AIAssistant()
        
        mock_openai.assert_called_once_with(api_key='test-key')
        assert assistant.model == 'gpt-4'
        assert assistant.temperature == 0.7
    
    @patch('ai_assistant.OpenAI')
    @patch('ai_assistant.config')
    def test_summarize_email(self, mock_config, mock_openai):
        """Test email summarization."""
        mock_config.openai.api_key = 'test-key'
        mock_config.openai.model = 'gpt-4'
        mock_config.openai.temperature = 0.7
        
        # Setup mock OpenAI client
        mock_client = Mock()
        mock_completion = Mock()
        mock_choice = Mock()
        mock_message = Mock()
        mock_message.content = "This is a summary of the email."
        mock_choice.message = mock_message
        mock_completion.choices = [mock_choice]
        mock_client.chat.completions.create.return_value = mock_completion
        mock_openai.return_value = mock_client
        
        # Test
        assistant = AIAssistant()
        email_content = {
            'subject': 'Test Subject',
            'bodyPreview': 'Test body content',
            'from': {
                'emailAddress': {
                    'address': 'sender@example.com'
                }
            }
        }
        
        summary = assistant.summarize_email(email_content)
        
        assert summary == "This is a summary of the email."
        mock_client.chat.completions.create.assert_called_once()
    
    @patch('ai_assistant.OpenAI')
    @patch('ai_assistant.config')
    def test_generate_reply(self, mock_config, mock_openai):
        """Test reply generation."""
        mock_config.openai.api_key = 'test-key'
        mock_config.openai.model = 'gpt-4'
        mock_config.openai.temperature = 0.7
        
        # Setup mock OpenAI client
        mock_client = Mock()
        mock_completion = Mock()
        mock_choice = Mock()
        mock_message = Mock()
        mock_message.content = "Thank you for your email. I will review and respond."
        mock_choice.message = mock_message
        mock_completion.choices = [mock_choice]
        mock_client.chat.completions.create.return_value = mock_completion
        mock_openai.return_value = mock_client
        
        # Test
        assistant = AIAssistant()
        email_content = {
            'subject': 'Meeting Request',
            'bodyPreview': 'Can we schedule a meeting?',
            'from': {
                'emailAddress': {
                    'address': 'sender@example.com'
                }
            }
        }
        
        reply = assistant.generate_reply(email_content)
        
        assert "Thank you for your email" in reply
        mock_client.chat.completions.create.assert_called_once()
    
    @patch('ai_assistant.OpenAI')
    @patch('ai_assistant.config')
    def test_extract_action_items(self, mock_config, mock_openai):
        """Test action item extraction."""
        mock_config.openai.api_key = 'test-key'
        mock_config.openai.model = 'gpt-4'
        mock_config.openai.temperature = 0.7
        
        # Setup mock OpenAI client
        mock_client = Mock()
        mock_completion = Mock()
        mock_choice = Mock()
        mock_message = Mock()
        mock_message.content = "• Review the document\n• Send feedback by Friday\n• Schedule follow-up meeting"
        mock_choice.message = mock_message
        mock_completion.choices = [mock_choice]
        mock_client.chat.completions.create.return_value = mock_completion
        mock_openai.return_value = mock_client
        
        # Test
        assistant = AIAssistant()
        email_content = {
            'subject': 'Action Items',
            'bodyPreview': 'Please review the document and send feedback.'
        }
        
        action_items = assistant.extract_action_items(email_content)
        
        assert len(action_items) == 3
        assert "Review the document" in action_items[0]
        assert "Send feedback by Friday" in action_items[1]
        assert "Schedule follow-up meeting" in action_items[2]
    
    @patch('ai_assistant.OpenAI')
    @patch('ai_assistant.config')
    def test_extract_action_items_none_found(self, mock_config, mock_openai):
        """Test action item extraction when no items found."""
        mock_config.openai.api_key = 'test-key'
        mock_config.openai.model = 'gpt-4'
        mock_config.openai.temperature = 0.7
        
        # Setup mock OpenAI client
        mock_client = Mock()
        mock_completion = Mock()
        mock_choice = Mock()
        mock_message = Mock()
        mock_message.content = "No action items found."
        mock_choice.message = mock_message
        mock_completion.choices = [mock_choice]
        mock_client.chat.completions.create.return_value = mock_completion
        mock_openai.return_value = mock_client
        
        # Test
        assistant = AIAssistant()
        email_content = {
            'subject': 'FYI',
            'bodyPreview': 'Just keeping you informed.'
        }
        
        action_items = assistant.extract_action_items(email_content)
        
        assert len(action_items) == 0
    
    @patch('ai_assistant.OpenAI')
    @patch('ai_assistant.config')
    def test_draft_email(self, mock_config, mock_openai):
        """Test email drafting."""
        mock_config.openai.api_key = 'test-key'
        mock_config.openai.model = 'gpt-4'
        mock_config.openai.temperature = 0.7
        
        # Setup mock OpenAI client
        mock_client = Mock()
        mock_completion = Mock()
        mock_choice = Mock()
        mock_message = Mock()
        mock_message.content = "Dear Team,\n\nI hope this email finds you well.\n\nBest regards"
        mock_choice.message = mock_message
        mock_completion.choices = [mock_choice]
        mock_client.chat.completions.create.return_value = mock_completion
        mock_openai.return_value = mock_client
        
        # Test
        assistant = AIAssistant()
        body = assistant.draft_email(
            to='team@example.com',
            subject='Team Update',
            context='Send a general team update'
        )
        
        assert "Dear Team" in body
        mock_client.chat.completions.create.assert_called_once()
