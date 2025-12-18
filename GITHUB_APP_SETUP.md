# GitHub App Setup for Drone CI (CORRECT METHOD)

## Create GitHub App (Not OAuth App)

1. Go to: https://github.com/settings/apps/new
2. Fill in:
   - **GitHub App name**: `Drone-CI-QA-Garden`
   - **Homepage URL**: `https://krystin-unoutspoken-terica.ngrok-free.dev`
   - **Webhook URL**: `https://krystin-unoutspoken-terica.ngrok-free.dev/hook`
   - **Webhook secret**: `super-secret-secret`

## Required Permissions
Set these **Repository permissions**:
- **Actions**: Read
- **Administration**: Read  
- **Checks**: Write
- **Contents**: Read
- **Issues**: Read
- **Metadata**: Read
- **Pull requests**: Read
- **Commit statuses**: Write

## Subscribe to Events
Check these boxes:
- ✅ Push
- ✅ Pull request
- ✅ Repository

## After Creation
1. Generate and download private key
2. Note the App ID
3. Install the app on your repository

## Update Drone Config
```bash
DRONE_GITHUB_CLIENT_ID=your_app_id
DRONE_GITHUB_CLIENT_SECRET=your_private_key_content
```