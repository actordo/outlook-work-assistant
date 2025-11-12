"""Outlook client module for interacting with Microsoft Graph API."""
import json
from typing import List, Dict, Optional
import msal
import requests
from config import config


class OutlookClient:
    """Client for interacting with Outlook via Microsoft Graph API."""
    
    GRAPH_API_ENDPOINT = "https://graph.microsoft.com/v1.0"
    
    def __init__(self):
        """Initialize the Outlook client."""
        self.config = config
        self.access_token = None
        self._authenticate()
    
    def _authenticate(self) -> None:
        """Authenticate with Microsoft Graph API using MSAL."""
        app = msal.ConfidentialClientApplication(
            self.config.azure.client_id,
            authority=self.config.azure.authority_url,
            client_credential=self.config.azure.client_secret,
        )
        
        # Acquire token for the application
        result = app.acquire_token_for_client(scopes=self.config.outlook.scopes)
        
        if "access_token" in result:
            self.access_token = result["access_token"]
        else:
            raise Exception(f"Authentication failed: {result.get('error_description', 'Unknown error')}")
    
    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict:
        """Make an authenticated request to Microsoft Graph API."""
        if not self.access_token:
            raise Exception("Not authenticated. Please authenticate first.")
        
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        url = f"{self.GRAPH_API_ENDPOINT}{endpoint}"
        
        if method.upper() == "GET":
            response = requests.get(url, headers=headers)
        elif method.upper() == "POST":
            response = requests.post(url, headers=headers, json=data)
        elif method.upper() == "PATCH":
            response = requests.patch(url, headers=headers, json=data)
        elif method.upper() == "DELETE":
            response = requests.delete(url, headers=headers)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")
        
        response.raise_for_status()
        
        # Some endpoints return empty responses
        if response.status_code == 204:
            return {}
        
        return response.json()
    
    def get_messages(self, folder: str = "inbox", limit: int = 10) -> List[Dict]:
        """
        Get messages from a specific folder.
        
        Args:
            folder: The folder to retrieve messages from (default: inbox)
            limit: Maximum number of messages to retrieve (default: 10)
        
        Returns:
            List of message dictionaries
        """
        endpoint = f"/users/{self.config.outlook.user_email}/mailFolders/{folder}/messages"
        params = f"?$top={limit}&$select=subject,from,receivedDateTime,bodyPreview,isRead"
        
        result = self._make_request("GET", endpoint + params)
        return result.get("value", [])
    
    def get_message_details(self, message_id: str) -> Dict:
        """
        Get detailed information about a specific message.
        
        Args:
            message_id: The ID of the message
        
        Returns:
            Message details dictionary
        """
        endpoint = f"/users/{self.config.outlook.user_email}/messages/{message_id}"
        return self._make_request("GET", endpoint)
    
    def send_message(self, to: str, subject: str, body: str, body_type: str = "HTML") -> Dict:
        """
        Send an email message.
        
        Args:
            to: Recipient email address
            subject: Email subject
            body: Email body content
            body_type: Body content type (HTML or Text)
        
        Returns:
            Response dictionary
        """
        message = {
            "message": {
                "subject": subject,
                "body": {
                    "contentType": body_type,
                    "content": body
                },
                "toRecipients": [
                    {
                        "emailAddress": {
                            "address": to
                        }
                    }
                ]
            }
        }
        
        endpoint = f"/users/{self.config.outlook.user_email}/sendMail"
        return self._make_request("POST", endpoint, message)
    
    def create_draft(self, to: str, subject: str, body: str, body_type: str = "HTML") -> Dict:
        """
        Create a draft email message.
        
        Args:
            to: Recipient email address
            subject: Email subject
            body: Email body content
            body_type: Body content type (HTML or Text)
        
        Returns:
            Created draft message dictionary
        """
        message = {
            "subject": subject,
            "body": {
                "contentType": body_type,
                "content": body
            },
            "toRecipients": [
                {
                    "emailAddress": {
                        "address": to
                    }
                }
            ]
        }
        
        endpoint = f"/users/{self.config.outlook.user_email}/messages"
        return self._make_request("POST", endpoint, message)
    
    def mark_as_read(self, message_id: str) -> Dict:
        """
        Mark a message as read.
        
        Args:
            message_id: The ID of the message
        
        Returns:
            Response dictionary
        """
        endpoint = f"/users/{self.config.outlook.user_email}/messages/{message_id}"
        data = {"isRead": True}
        return self._make_request("PATCH", endpoint, data)
    
    def get_folders(self) -> List[Dict]:
        """
        Get all mail folders.
        
        Returns:
            List of folder dictionaries
        """
        endpoint = f"/users/{self.config.outlook.user_email}/mailFolders"
        result = self._make_request("GET", endpoint)
        return result.get("value", [])
