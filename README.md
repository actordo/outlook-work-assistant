# Outlook Assistant

AI-powered assistant for Microsoft Work Outlook accounts. This tool leverages OpenAI's GPT models and Microsoft Graph API to provide intelligent email management capabilities.

## Features

- 📧 **Email Management**: List, read, and organize emails from your Work Outlook account
- 🤖 **AI-Powered Summaries**: Get concise summaries of lengthy emails
- ✍️ **Reply Generation**: Generate professional email replies with AI assistance
- 📂 **Smart Categorization**: Automatically categorize emails by topic and urgency
- ✅ **Action Item Extraction**: Extract tasks and action items from emails
- 📝 **Draft Composition**: Create email drafts with AI assistance
- 🔐 **Secure Authentication**: Uses Microsoft Azure AD for secure access

## Prerequisites

- Python 3.8 or higher
- Microsoft Azure AD application registration
- OpenAI API key
- Work/Office 365 Outlook account

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/actordo/outlook-assistant.git
cd outlook-assistant
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Register Azure AD Application

1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to **Azure Active Directory** > **App registrations** > **New registration**
3. Set a name (e.g., "Outlook AI Assistant")
4. Select **Accounts in this organizational directory only**
5. Click **Register**
6. Note down the **Application (client) ID** and **Directory (tenant) ID**
7. Go to **Certificates & secrets** > **New client secret**
8. Create a secret and note down the **Value**
9. Go to **API permissions** > **Add a permission** > **Microsoft Graph** > **Application permissions**
10. Add the following permissions:
    - `Mail.Read`
    - `Mail.ReadWrite`
    - `Mail.Send`
    - `User.Read.All`
11. Click **Grant admin consent** for your organization

### 4. Configure Environment Variables

Copy the example environment file and fill in your credentials:

```bash
cp .env.example .env
```

Edit `.env` with your actual values:

```env
AZURE_CLIENT_ID=your_client_id_here
AZURE_CLIENT_SECRET=your_client_secret_here
AZURE_TENANT_ID=your_tenant_id_here
OPENAI_API_KEY=your_openai_api_key_here
OUTLOOK_USER_EMAIL=your_work_email@company.com
```

## Usage

The assistant provides several commands for different tasks:

### List Recent Emails

```bash
python main.py list --limit 10
```

### Summarize an Email

```bash
python main.py summarize <message_id>
```

### Generate Reply

```bash
python main.py reply <message_id> --context "Accept the meeting invitation"
```

### Categorize Inbox

```bash
python main.py categorize --limit 20
```

### Extract Action Items

```bash
python main.py actions <message_id>
```

### Draft New Email

```bash
python main.py draft recipient@example.com "Meeting Follow-up" "Draft a follow-up email for yesterday's project meeting"
```

### Show Mail Folders

```bash
python main.py folders
```

## Configuration Options

You can customize the AI behavior by setting these optional environment variables:

- `AI_MODEL`: OpenAI model to use (default: `gpt-4`)
- `AI_TEMPERATURE`: Temperature for AI responses (default: `0.7`)

## Security Best Practices

- ⚠️ **Never commit** your `.env` file to version control
- 🔑 Store credentials securely (use environment variables or secret management tools)
- 🔒 Regularly rotate your Azure AD client secrets
- 📝 Follow the principle of least privilege when assigning API permissions
- 🛡️ Use Azure AD Conditional Access policies for additional security

## Troubleshooting

### Authentication Errors

If you encounter authentication errors:
1. Verify your Azure AD credentials in `.env`
2. Ensure admin consent is granted for API permissions
3. Check that your Azure AD app is not expired

### API Rate Limits

Microsoft Graph API has rate limits. If you hit limits:
- Reduce the number of emails processed at once
- Add delays between API calls
- Check your [Azure AD service limits](https://docs.microsoft.com/en-us/graph/throttling)

### OpenAI API Errors

- Verify your OpenAI API key is valid
- Check your OpenAI account has available credits
- Ensure you're using a supported model

## Architecture

The application consists of three main modules:

1. **config.py**: Configuration management using Pydantic models
2. **outlook_client.py**: Microsoft Graph API client for Outlook operations
3. **ai_assistant.py**: OpenAI integration for AI-powered features
4. **main.py**: CLI interface and orchestration

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is provided as-is for educational and productivity purposes.

## Disclaimer

This tool requires access to your Work Outlook account. Always review generated content before sending emails or taking actions. The AI may occasionally produce incorrect or inappropriate responses.