"""Tests for Outlook client module."""
import pytest
from unittest.mock import Mock, patch, MagicMock
from outlook_client import OutlookClient


class TestOutlookClient:
    """Test OutlookClient class."""
    
    @patch('outlook_client.msal.ConfidentialClientApplication')
    @patch('outlook_client.config')
    def test_client_initialization(self, mock_config, mock_msal):
        """Test OutlookClient initialization."""
        # Setup mock config
        mock_config.azure.client_id = 'test-client'
        mock_config.azure.client_secret = 'test-secret'
        mock_config.azure.authority_url = 'https://login.microsoftonline.com/test'
        mock_config.outlook.scopes = ['https://graph.microsoft.com/.default']
        
        # Setup mock MSAL app
        mock_app = Mock()
        mock_app.acquire_token_for_client.return_value = {'access_token': 'test-token'}
        mock_msal.return_value = mock_app
        
        # Initialize client
        client = OutlookClient()
        
        # Verify MSAL was called correctly
        mock_msal.assert_called_once_with(
            'test-client',
            authority='https://login.microsoftonline.com/test',
            client_credential='test-secret'
        )
        
        # Verify token was acquired
        assert client.access_token == 'test-token'
    
    @patch('outlook_client.msal.ConfidentialClientApplication')
    @patch('outlook_client.config')
    def test_authentication_failure(self, mock_config, mock_msal):
        """Test authentication failure handling."""
        # Setup mock config
        mock_config.azure.client_id = 'test-client'
        mock_config.azure.client_secret = 'test-secret'
        mock_config.azure.authority_url = 'https://login.microsoftonline.com/test'
        mock_config.outlook.scopes = ['https://graph.microsoft.com/.default']
        
        # Setup mock MSAL app to fail
        mock_app = Mock()
        mock_app.acquire_token_for_client.return_value = {
            'error': 'invalid_client',
            'error_description': 'Invalid client credentials'
        }
        mock_msal.return_value = mock_app
        
        # Should raise exception
        with pytest.raises(Exception, match="Authentication failed"):
            OutlookClient()
    
    @patch('outlook_client.requests.get')
    @patch('outlook_client.msal.ConfidentialClientApplication')
    @patch('outlook_client.config')
    def test_get_messages(self, mock_config, mock_msal, mock_get):
        """Test getting messages."""
        # Setup mocks
        mock_config.azure.client_id = 'test-client'
        mock_config.azure.client_secret = 'test-secret'
        mock_config.azure.authority_url = 'https://login.microsoftonline.com/test'
        mock_config.outlook.scopes = ['https://graph.microsoft.com/.default']
        mock_config.outlook.user_email = 'test@example.com'
        
        mock_app = Mock()
        mock_app.acquire_token_for_client.return_value = {'access_token': 'test-token'}
        mock_msal.return_value = mock_app
        
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'value': [
                {'id': '1', 'subject': 'Test Email 1'},
                {'id': '2', 'subject': 'Test Email 2'}
            ]
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        # Test
        client = OutlookClient()
        messages = client.get_messages(limit=2)
        
        assert len(messages) == 2
        assert messages[0]['subject'] == 'Test Email 1'
        assert messages[1]['subject'] == 'Test Email 2'
    
    @patch('outlook_client.requests.post')
    @patch('outlook_client.msal.ConfidentialClientApplication')
    @patch('outlook_client.config')
    def test_send_message(self, mock_config, mock_msal, mock_post):
        """Test sending a message."""
        # Setup mocks
        mock_config.azure.client_id = 'test-client'
        mock_config.azure.client_secret = 'test-secret'
        mock_config.azure.authority_url = 'https://login.microsoftonline.com/test'
        mock_config.outlook.scopes = ['https://graph.microsoft.com/.default']
        mock_config.outlook.user_email = 'test@example.com'
        
        mock_app = Mock()
        mock_app.acquire_token_for_client.return_value = {'access_token': 'test-token'}
        mock_msal.return_value = mock_app
        
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 204
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response
        
        # Test
        client = OutlookClient()
        result = client.send_message(
            to='recipient@example.com',
            subject='Test Subject',
            body='Test Body'
        )
        
        assert result == {}
        mock_post.assert_called_once()
    
    @patch('outlook_client.requests.patch')
    @patch('outlook_client.msal.ConfidentialClientApplication')
    @patch('outlook_client.config')
    def test_mark_as_read(self, mock_config, mock_msal, mock_patch):
        """Test marking a message as read."""
        # Setup mocks
        mock_config.azure.client_id = 'test-client'
        mock_config.azure.client_secret = 'test-secret'
        mock_config.azure.authority_url = 'https://login.microsoftonline.com/test'
        mock_config.outlook.scopes = ['https://graph.microsoft.com/.default']
        mock_config.outlook.user_email = 'test@example.com'
        
        mock_app = Mock()
        mock_app.acquire_token_for_client.return_value = {'access_token': 'test-token'}
        mock_msal.return_value = mock_app
        
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'id': 'message-123', 'isRead': True}
        mock_response.raise_for_status = Mock()
        mock_patch.return_value = mock_response
        
        # Test
        client = OutlookClient()
        result = client.mark_as_read('message-123')
        
        assert result['isRead'] is True
        mock_patch.assert_called_once()
