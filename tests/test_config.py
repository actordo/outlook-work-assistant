"""Tests for configuration module."""
import os
import pytest
from unittest.mock import patch
from config import Config, AzureConfig, OpenAIConfig, OutlookConfig


class TestAzureConfig:
    """Test AzureConfig class."""
    
    def test_azure_config_defaults(self):
        """Test AzureConfig with default values."""
        config = AzureConfig()
        assert config.authority == "https://login.microsoftonline.com"
    
    @patch.dict(os.environ, {
        'AZURE_CLIENT_ID': 'test-client-id',
        'AZURE_CLIENT_SECRET': 'test-secret',
        'AZURE_TENANT_ID': 'test-tenant'
    })
    def test_azure_config_from_env(self):
        """Test AzureConfig loads from environment variables."""
        config = AzureConfig()
        assert config.client_id == 'test-client-id'
        assert config.client_secret == 'test-secret'
        assert config.tenant_id == 'test-tenant'
    
    def test_authority_url_property(self):
        """Test authority_url property."""
        config = AzureConfig(tenant_id='test-tenant-123')
        assert config.authority_url == 'https://login.microsoftonline.com/test-tenant-123'


class TestOpenAIConfig:
    """Test OpenAIConfig class."""
    
    @patch.dict(os.environ, {
        'OPENAI_API_KEY': 'test-key',
        'AI_MODEL': 'gpt-3.5-turbo',
        'AI_TEMPERATURE': '0.5'
    })
    def test_openai_config_from_env(self):
        """Test OpenAIConfig loads from environment variables."""
        config = OpenAIConfig()
        assert config.api_key == 'test-key'
        assert config.model == 'gpt-3.5-turbo'
        assert config.temperature == 0.5
    
    def test_openai_config_defaults(self):
        """Test OpenAIConfig default values."""
        config = OpenAIConfig()
        assert config.model == 'gpt-4'
        assert config.temperature == 0.7


class TestOutlookConfig:
    """Test OutlookConfig class."""
    
    @patch.dict(os.environ, {'OUTLOOK_USER_EMAIL': 'test@example.com'})
    def test_outlook_config_from_env(self):
        """Test OutlookConfig loads from environment variables."""
        config = OutlookConfig()
        assert config.user_email == 'test@example.com'
    
    def test_outlook_config_scopes(self):
        """Test OutlookConfig has correct default scopes."""
        config = OutlookConfig()
        assert config.scopes == ["https://graph.microsoft.com/.default"]


class TestConfig:
    """Test main Config class."""
    
    def test_config_structure(self):
        """Test Config has required nested configurations."""
        config = Config()
        assert isinstance(config.azure, AzureConfig)
        assert isinstance(config.openai, OpenAIConfig)
        assert isinstance(config.outlook, OutlookConfig)
    
    @patch.dict(os.environ, {
        'AZURE_CLIENT_ID': 'test-client',
        'AZURE_CLIENT_SECRET': 'test-secret',
        'AZURE_TENANT_ID': 'test-tenant',
        'OPENAI_API_KEY': 'test-key',
        'OUTLOOK_USER_EMAIL': 'test@example.com'
    })
    def test_config_validation_success(self):
        """Test config validation succeeds with all required values."""
        config = Config()
        assert config.validate() is True
    
    def test_config_validation_missing_azure_client_id(self):
        """Test config validation fails without AZURE_CLIENT_ID."""
        config = Config()
        with pytest.raises(ValueError, match="AZURE_CLIENT_ID is required"):
            config.validate()
    
    @patch.dict(os.environ, {'AZURE_CLIENT_ID': 'test-client'})
    def test_config_validation_missing_azure_client_secret(self):
        """Test config validation fails without AZURE_CLIENT_SECRET."""
        config = Config()
        with pytest.raises(ValueError, match="AZURE_CLIENT_SECRET is required"):
            config.validate()
    
    @patch.dict(os.environ, {
        'AZURE_CLIENT_ID': 'test-client',
        'AZURE_CLIENT_SECRET': 'test-secret'
    })
    def test_config_validation_missing_azure_tenant_id(self):
        """Test config validation fails without AZURE_TENANT_ID."""
        config = Config()
        with pytest.raises(ValueError, match="AZURE_TENANT_ID is required"):
            config.validate()
    
    @patch.dict(os.environ, {
        'AZURE_CLIENT_ID': 'test-client',
        'AZURE_CLIENT_SECRET': 'test-secret',
        'AZURE_TENANT_ID': 'test-tenant'
    })
    def test_config_validation_missing_openai_key(self):
        """Test config validation fails without OPENAI_API_KEY."""
        config = Config()
        with pytest.raises(ValueError, match="OPENAI_API_KEY is required"):
            config.validate()
    
    @patch.dict(os.environ, {
        'AZURE_CLIENT_ID': 'test-client',
        'AZURE_CLIENT_SECRET': 'test-secret',
        'AZURE_TENANT_ID': 'test-tenant',
        'OPENAI_API_KEY': 'test-key'
    })
    def test_config_validation_missing_user_email(self):
        """Test config validation fails without OUTLOOK_USER_EMAIL."""
        config = Config()
        with pytest.raises(ValueError, match="OUTLOOK_USER_EMAIL is required"):
            config.validate()
