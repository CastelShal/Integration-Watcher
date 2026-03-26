# TStax Webhook Repository

A Flask application that receives and processes GitHub webhook events, storing them in MongoDB.

## Local Deployment Instructions

### Prerequisites

- Python 3.9+
- MongoDB 8.0+
- Git

### Step 1: Clone and Setup

```bash
git clone git@github.com:CastelShal/TStax-Webhook-Repo.git
cd TStax-Webhook-Repo
```

### Step 2: Create Virtual Environment

```bash
python3 -m venv webhook-repo
source webhook-repo/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
# MongoDB Connection String
# Format: mongodb://username:password@host:port/database
MONGO_URI=your_mongo_uri

# GitHub Webhook Secret
# This is the secret key configured in your GitHub webhook settings
GITHUB_SECRET=your_github_webhook_secret
```
### Step 5: Run the Application

With your virtual environment activated:

```bash
python run.py
```

The application will start and be accessible at:
- **Application URL**: `http://localhost:5000`
- **Webhook Receiver Endpoint**: `http://localhost:5000/webhook/receiver`
- **Events Viewer**: `http://localhost:5000/event`
