"""Outlook AI Assistant - AI-powered assistant for Microsoft Work Outlook accounts."""

__version__ = "1.0.0"
__author__ = "Outlook Assistant Team"
__license__ = "MIT"

from config import Config
from outlook_client import OutlookClient
from ai_assistant import AIAssistant

__all__ = ["Config", "OutlookClient", "AIAssistant", "__version__"]
