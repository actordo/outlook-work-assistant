# Quick Start Guide

Get up and running with Outlook AI Assistant in 5 minutes!

## Prerequisites

- Python 3.8+
- pip package manager
- An Azure AD account with admin access
- OpenAI API key

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Set Up Azure AD App

1. Visit [Azure Portal](https://portal.azure.com)
2. Go to **Azure Active Directory** → **App registrations** → **New registration**
3. Name your app (e.g., "Outlook AI Assistant")
4. Select "Accounts in this organizational directory only"
5. Click **Register**

### Configure API Permissions

1. In your app, go to **API permissions**
2. Click **Add a permission** → **Microsoft Graph** → **Application permissions**
3. Add these permissions:
   - `Mail.Read`
   - `Mail.ReadWrite`
   - `Mail.Send`
   - `User.Read.All`
4. Click **Grant admin consent**

### Get Credentials

1. Copy your **Application (client) ID**
2. Copy your **Directory (tenant) ID**
3. Go to **Certificates & secrets** → **New client secret**
4. Copy the secret **Value** (not the ID)

## Step 3: Configure Environment

Create a `.env` file:

```bash
cp .env.example .env
```

Edit `.env` with your credentials:

```env
AZURE_CLIENT_ID=<your-client-id>
AZURE_CLIENT_SECRET=<your-client-secret>
AZURE_TENANT_ID=<your-tenant-id>
OPENAI_API_KEY=<your-openai-key>
OUTLOOK_USER_EMAIL=<your-work-email>
```

## Step 4: Test the Setup

List your recent emails:

```bash
python main.py list --limit 5
```

## Common Commands

### View Help
```bash
python main.py --help
```

### List Recent Emails
```bash
python main.py list --limit 10
```

### Get Email Summary
```bash
python main.py summarize <message-id>
```

### Categorize Inbox
```bash
python main.py categorize --limit 20
```

### Generate Reply
```bash
python main.py reply <message-id> --context "Accept the invitation"
```

### Draft New Email
```bash
python main.py draft recipient@example.com "Subject" "Context for the email"
```

## Troubleshooting

### "Authentication failed" Error

- Verify your Azure AD credentials in `.env`
- Ensure admin consent is granted for API permissions
- Check that your client secret hasn't expired

### "OPENAI_API_KEY is required" Error

- Make sure your `.env` file exists
- Verify the OpenAI API key is correct
- Check that you have credits in your OpenAI account

### No Emails Returned

- Verify your `OUTLOOK_USER_EMAIL` is correct
- Ensure you have emails in your inbox
- Check API permissions are granted

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check [CONTRIBUTING.md](CONTRIBUTING.md) if you want to contribute
- Explore different AI models and temperature settings

## Need Help?

Open an issue on GitHub with:
- Your error message
- Python version
- Steps to reproduce

Happy emailing! 📧🤖
