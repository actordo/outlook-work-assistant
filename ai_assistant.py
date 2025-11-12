"""AI Assistant module for providing intelligent email assistance."""
from typing import List, Dict, Optional
from openai import OpenAI
from config import config


class AIAssistant:
    """AI Assistant for email management and assistance."""
    
    def __init__(self):
        """Initialize the AI Assistant."""
        self.client = OpenAI(api_key=config.openai.api_key)
        self.model = config.openai.model
        self.temperature = config.openai.temperature
    
    def summarize_email(self, email_content: Dict) -> str:
        """
        Summarize an email message.
        
        Args:
            email_content: Dictionary containing email details
        
        Returns:
            Summary of the email
        """
        subject = email_content.get("subject", "No subject")
        body = email_content.get("bodyPreview", email_content.get("body", {}).get("content", ""))
        sender = email_content.get("from", {}).get("emailAddress", {}).get("address", "Unknown")
        
        prompt = f"""Summarize the following email in a concise manner:

From: {sender}
Subject: {subject}

Email Content:
{body}

Provide a brief summary highlighting the key points and any action items."""
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a helpful email assistant that summarizes emails concisely."},
                {"role": "user", "content": prompt}
            ],
            temperature=self.temperature
        )
        
        return response.choices[0].message.content
    
    def generate_reply(self, email_content: Dict, context: Optional[str] = None) -> str:
        """
        Generate a reply to an email.
        
        Args:
            email_content: Dictionary containing email details
            context: Optional context or instructions for the reply
        
        Returns:
            Generated reply text
        """
        subject = email_content.get("subject", "No subject")
        body = email_content.get("bodyPreview", email_content.get("body", {}).get("content", ""))
        sender = email_content.get("from", {}).get("emailAddress", {}).get("address", "Unknown")
        
        prompt = f"""Generate a professional reply to the following email:

From: {sender}
Subject: {subject}

Email Content:
{body}

{f'Additional context: {context}' if context else ''}

Generate a polite and professional reply."""
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a professional email assistant that helps write email replies."},
                {"role": "user", "content": prompt}
            ],
            temperature=self.temperature
        )
        
        return response.choices[0].message.content
    
    def categorize_emails(self, emails: List[Dict]) -> Dict[str, List[Dict]]:
        """
        Categorize a list of emails by topic or urgency.
        
        Args:
            emails: List of email dictionaries
        
        Returns:
            Dictionary with categories as keys and lists of emails as values
        """
        if not emails:
            return {}
        
        # Create a summary of emails for categorization
        email_summaries = []
        for idx, email in enumerate(emails):
            subject = email.get("subject", "No subject")
            preview = email.get("bodyPreview", "")
            sender = email.get("from", {}).get("emailAddress", {}).get("address", "Unknown")
            email_summaries.append(f"{idx}. From: {sender}, Subject: {subject}, Preview: {preview[:100]}")
        
        prompt = f"""Categorize the following emails into categories like 'Urgent', 'Action Required', 'Informational', 'Meeting', 'Newsletter', etc.

Emails:
{chr(10).join(email_summaries)}

Return a JSON object where keys are category names and values are lists of email indices (0-based)."""
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are an email categorization assistant. Return only valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        
        try:
            import json
            categories = json.loads(response.choices[0].message.content)
            
            # Map indices back to email objects
            result = {}
            for category, indices in categories.items():
                result[category] = [emails[i] for i in indices if i < len(emails)]
            
            return result
        except (json.JSONDecodeError, KeyError, IndexError):
            # Fallback: return all emails in a single category
            return {"Uncategorized": emails}
    
    def extract_action_items(self, email_content: Dict) -> List[str]:
        """
        Extract action items from an email.
        
        Args:
            email_content: Dictionary containing email details
        
        Returns:
            List of action items
        """
        subject = email_content.get("subject", "No subject")
        body = email_content.get("bodyPreview", email_content.get("body", {}).get("content", ""))
        
        prompt = f"""Extract any action items or tasks from the following email:

Subject: {subject}

Email Content:
{body}

List each action item as a separate bullet point. If there are no action items, respond with "No action items found." """
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are an assistant that extracts action items from emails."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        
        content = response.choices[0].message.content
        
        # Parse the response into a list
        if "No action items found" in content:
            return []
        
        # Split by newlines and filter out empty lines
        action_items = [line.strip().lstrip('•-*').strip() 
                       for line in content.split('\n') 
                       if line.strip() and not line.strip().startswith('#')]
        
        return [item for item in action_items if item]
    
    def draft_email(self, to: str, subject: str, context: str) -> str:
        """
        Draft a new email based on context.
        
        Args:
            to: Recipient email address
            subject: Email subject
            context: Context or instructions for the email
        
        Returns:
            Generated email body
        """
        prompt = f"""Draft a professional email with the following details:

To: {to}
Subject: {subject}

Context/Instructions:
{context}

Generate a complete, professional email body."""
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a professional email writing assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=self.temperature
        )
        
        return response.choices[0].message.content
