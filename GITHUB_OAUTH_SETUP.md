# GitHub OAuth App Setup for Drone CI

## Step-by-Step GitHub OAuth Configuration

### 1. Create GitHub OAuth App
1. Go to GitHub Settings → Developer settings → OAuth Apps
2. Click "New OAuth App"
3. Fill in:
   - **Application name**: `Drone CI - QA Garden`
   - **Homepage URL**: `http://localhost:8007`
   - **Authorization callback URL**: `http://localhost:8007/login`
4. Click "Register application"

### 2. Get Credentials
- **Client ID**: Already set as `Iv23lim14p0PKK69D5QN`
- **Client Secret**: Copy from GitHub OAuth app page

### 3. Update Environment
Edit `.env` file:
```bash
DRONE_GITHUB_CLIENT_SECRET=your_actual_secret_from_github
DRONE_RPC_SECRET=generate_random_32_char_string
```

### 4. Repository Permissions Required
- **Admin access** to the repository
- **OAuth app** must be authorized for your organization (if applicable)

### 5. Common Issues & Solutions

#### "Resource not accessible by integration"
- ✅ Verify GitHub OAuth app callback URL: `http://localhost:8007/login`
- ✅ Check repository admin permissions
- ✅ Ensure OAuth app is authorized for organization
- ✅ Restart Drone server after config changes

#### OAuth App Authorization
If repository is in an organization:
1. Go to Organization Settings → Third-party access
2. Find your Drone OAuth app
3. Click "Grant" or "Request access"

### 6. Test Commands
```bash
# Start Drone
docker-compose -f drone-compose.yml up -d

# Check setup
python drone-setup-check.py

# View logs
docker-compose -f drone-compose.yml logs drone-server
```