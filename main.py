"""Main application entry point for Outlook AI Assistant."""
import argparse
import sys
from typing import Optional
from outlook_client import OutlookClient
from ai_assistant import AIAssistant
from config import config


class OutlookAssistant:
    """Main Outlook AI Assistant application."""
    
    def __init__(self):
        """Initialize the Outlook Assistant."""
        try:
            config.validate()
            self.outlook = OutlookClient()
            self.ai = AIAssistant()
            print("✓ Outlook AI Assistant initialized successfully")
        except Exception as e:
            print(f"✗ Error initializing Outlook AI Assistant: {e}")
            sys.exit(1)
    
    def list_recent_emails(self, limit: int = 10):
        """List recent emails from inbox."""
        print(f"\n📧 Fetching {limit} most recent emails...\n")
        try:
            messages = self.outlook.get_messages(folder="inbox", limit=limit)
            
            if not messages:
                print("No messages found.")
                return
            
            for idx, message in enumerate(messages, 1):
                sender = message.get("from", {}).get("emailAddress", {}).get("name", "Unknown")
                subject = message.get("subject", "No subject")
                received = message.get("receivedDateTime", "Unknown date")
                is_read = message.get("isRead", False)
                status = "📖 Read" if is_read else "📬 Unread"
                
                print(f"{idx}. {status} | From: {sender}")
                print(f"   Subject: {subject}")
                print(f"   Received: {received}")
                print()
            
            return messages
        except Exception as e:
            print(f"✗ Error fetching emails: {e}")
            return []
    
    def summarize_email(self, message_id: str):
        """Summarize a specific email."""
        print(f"\n🤖 Generating summary...\n")
        try:
            message = self.outlook.get_message_details(message_id)
            summary = self.ai.summarize_email(message)
            
            print("Summary:")
            print("-" * 60)
            print(summary)
            print("-" * 60)
        except Exception as e:
            print(f"✗ Error summarizing email: {e}")
    
    def generate_reply(self, message_id: str, context: Optional[str] = None):
        """Generate a reply to a specific email."""
        print(f"\n🤖 Generating reply...\n")
        try:
            message = self.outlook.get_message_details(message_id)
            reply = self.ai.generate_reply(message, context)
            
            print("Generated Reply:")
            print("-" * 60)
            print(reply)
            print("-" * 60)
        except Exception as e:
            print(f"✗ Error generating reply: {e}")
    
    def categorize_inbox(self, limit: int = 20):
        """Categorize inbox emails."""
        print(f"\n🤖 Categorizing {limit} recent emails...\n")
        try:
            messages = self.outlook.get_messages(folder="inbox", limit=limit)
            
            if not messages:
                print("No messages to categorize.")
                return
            
            categories = self.ai.categorize_emails(messages)
            
            for category, emails in categories.items():
                print(f"\n📂 {category} ({len(emails)} emails):")
                for email in emails:
                    subject = email.get("subject", "No subject")
                    sender = email.get("from", {}).get("emailAddress", {}).get("name", "Unknown")
                    print(f"  • {subject} (from {sender})")
        except Exception as e:
            print(f"✗ Error categorizing emails: {e}")
    
    def extract_actions(self, message_id: str):
        """Extract action items from an email."""
        print(f"\n🤖 Extracting action items...\n")
        try:
            message = self.outlook.get_message_details(message_id)
            action_items = self.ai.extract_action_items(message)
            
            if not action_items:
                print("No action items found in this email.")
            else:
                print("Action Items:")
                print("-" * 60)
                for idx, item in enumerate(action_items, 1):
                    print(f"{idx}. {item}")
                print("-" * 60)
        except Exception as e:
            print(f"✗ Error extracting action items: {e}")
    
    def draft_email(self, to: str, subject: str, context: str):
        """Draft a new email with AI assistance."""
        print(f"\n🤖 Drafting email...\n")
        try:
            body = self.ai.draft_email(to, subject, context)
            
            print("Draft Email:")
            print("-" * 60)
            print(f"To: {to}")
            print(f"Subject: {subject}")
            print()
            print(body)
            print("-" * 60)
            
            # Optionally create draft in Outlook
            response = input("\nSave as draft in Outlook? (y/n): ")
            if response.lower() == 'y':
                self.outlook.create_draft(to, subject, body, body_type="Text")
                print("✓ Draft saved to Outlook")
        except Exception as e:
            print(f"✗ Error drafting email: {e}")
    
    def show_folders(self):
        """Show all mail folders."""
        print("\n📁 Mail folders:\n")
        try:
            folders = self.outlook.get_folders()
            for folder in folders:
                name = folder.get("displayName", "Unknown")
                total = folder.get("totalItemCount", 0)
                unread = folder.get("unreadItemCount", 0)
                print(f"  • {name} (Total: {total}, Unread: {unread})")
        except Exception as e:
            print(f"✗ Error fetching folders: {e}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="AI Assistant for Work Outlook accounts",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # List emails command
    list_parser = subparsers.add_parser("list", help="List recent emails")
    list_parser.add_argument("--limit", type=int, default=10, help="Number of emails to fetch")
    
    # Summarize email command
    summarize_parser = subparsers.add_parser("summarize", help="Summarize an email")
    summarize_parser.add_argument("message_id", help="Message ID to summarize")
    
    # Generate reply command
    reply_parser = subparsers.add_parser("reply", help="Generate reply to an email")
    reply_parser.add_argument("message_id", help="Message ID to reply to")
    reply_parser.add_argument("--context", help="Additional context for the reply")
    
    # Categorize emails command
    categorize_parser = subparsers.add_parser("categorize", help="Categorize inbox emails")
    categorize_parser.add_argument("--limit", type=int, default=20, help="Number of emails to categorize")
    
    # Extract action items command
    actions_parser = subparsers.add_parser("actions", help="Extract action items from an email")
    actions_parser.add_argument("message_id", help="Message ID to extract actions from")
    
    # Draft email command
    draft_parser = subparsers.add_parser("draft", help="Draft a new email with AI")
    draft_parser.add_argument("to", help="Recipient email address")
    draft_parser.add_argument("subject", help="Email subject")
    draft_parser.add_argument("context", help="Context or instructions for the email")
    
    # Show folders command
    subparsers.add_parser("folders", help="Show all mail folders")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Initialize the assistant
    assistant = OutlookAssistant()
    
    # Execute the requested command
    if args.command == "list":
        assistant.list_recent_emails(args.limit)
    elif args.command == "summarize":
        assistant.summarize_email(args.message_id)
    elif args.command == "reply":
        assistant.generate_reply(args.message_id, args.context)
    elif args.command == "categorize":
        assistant.categorize_inbox(args.limit)
    elif args.command == "actions":
        assistant.extract_actions(args.message_id)
    elif args.command == "draft":
        assistant.draft_email(args.to, args.subject, args.context)
    elif args.command == "folders":
        assistant.show_folders()


if __name__ == "__main__":
    main()
