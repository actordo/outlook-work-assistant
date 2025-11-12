"""Configuration module for Outlook AI Assistant."""
import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field

# Load environment variables from .env file
load_dotenv()


class AzureConfig(BaseModel):
    """Azure AD configuration for Microsoft Graph API."""
    client_id: str = Field(default_factory=lambda: os.getenv("AZURE_CLIENT_ID", ""))
    client_secret: str = Field(default_factory=lambda: os.getenv("AZURE_CLIENT_SECRET", ""))
    tenant_id: str = Field(default_factory=lambda: os.getenv("AZURE_TENANT_ID", ""))
    authority: str = Field(default="https://login.microsoftonline.com")
    
    @property
    def authority_url(self) -> str:
        """Get the full authority URL."""
        return f"{self.authority}/{self.tenant_id}"


class OpenAIConfig(BaseModel):
    """OpenAI configuration for AI assistant."""
    api_key: str = Field(default_factory=lambda: os.getenv("OPENAI_API_KEY", ""))
    model: str = Field(default_factory=lambda: os.getenv("AI_MODEL", "gpt-4"))
    temperature: float = Field(default_factory=lambda: float(os.getenv("AI_TEMPERATURE", "0.7")))


class OutlookConfig(BaseModel):
    """Outlook configuration."""
    user_email: str = Field(default_factory=lambda: os.getenv("OUTLOOK_USER_EMAIL", ""))
    scopes: list = Field(default=["https://graph.microsoft.com/.default"])


class Config(BaseModel):
    """Main configuration class."""
    azure: AzureConfig = Field(default_factory=AzureConfig)
    openai: OpenAIConfig = Field(default_factory=OpenAIConfig)
    outlook: OutlookConfig = Field(default_factory=OutlookConfig)
    
    def validate(self) -> bool:
        """Validate that all required configuration is present."""
        if not self.azure.client_id:
            raise ValueError("AZURE_CLIENT_ID is required")
        if not self.azure.client_secret:
            raise ValueError("AZURE_CLIENT_SECRET is required")
        if not self.azure.tenant_id:
            raise ValueError("AZURE_TENANT_ID is required")
        if not self.openai.api_key:
            raise ValueError("OPENAI_API_KEY is required")
        if not self.outlook.user_email:
            raise ValueError("OUTLOOK_USER_EMAIL is required")
        return True


# Global config instance
config = Config()
