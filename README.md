# Integrations-Watcher

A Flask application that receives and processes GitHub webhook events, storing them in MongoDB.

## Local Deployment Instructions

### Prerequisites

- Python 3.9+
- MongoDB 8.0+
- Git

### Step 1: Create Virtual Environment

```bash
python3 -m venv webhook-repo
source webhook-repo/bin/activate
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Configure Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
# MongoDB Connection String
# Format: mongodb://username:password@host:port/database
MONGO_URI=your_mongo_uri

# GitHub Webhook Secret
# This is the secret key configured in your GitHub webhook settings
GITHUB_SECRET=your_github_webhook_secret
```
### Step 4: Run the Application

With your virtual environment activated:

```bash
python run.py
```

