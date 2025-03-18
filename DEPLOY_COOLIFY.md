# Deploying to Coolify on Hetzner

This guide provides step-by-step instructions for deploying this FastAPI application on a Hetzner server using Coolify.

## Prerequisites

1. A Hetzner server (Cloud or Dedicated)
2. Coolify installed on your server
3. A Git repository with your code (GitHub, GitLab, etc.)

## Installing Coolify on Hetzner (If Not Already Installed)

1. SSH into your Hetzner server:
   ```bash
   ssh root@your-server-ip
   ```

2. Install Coolify using the official one-liner:
   ```bash
   wget -q https://get.coolify.io -O /tmp/install.sh && bash /tmp/install.sh
   ```

3. Follow the prompts to complete the installation.

4. Access the Coolify dashboard via `https://your-server-ip` and set up your admin account.

## Deploying Your FastAPI Application

### 1. Push Your Code to Git

Make sure your code is pushed to a Git repository (GitHub, GitLab, etc.).

### 2. Add Your Repository to Coolify

1. Log in to your Coolify dashboard
2. Navigate to "Sources" in the sidebar
3. Click "Add New Source"
4. Select your Git provider (GitHub, GitLab, etc.)
5. Authenticate with your Git provider if needed
6. Select the repository containing this FastAPI application

### 3. Create a New Service

1. From the Coolify dashboard, click "Services" in the sidebar
2. Click "New Service"
3. Select "Application"
4. Choose your repository from the list

### 4. Configure the Service

When configuring your service, use the following settings:

- **Template**: Python
- **Name**: Choose a name for your service (e.g., "fastapi-api")
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn main:app --host 0.0.0.0 --port 80`
- **Port**: 80

Alternatively, Coolify should automatically detect the `.coolify.yaml` file in the repository and apply the configuration.

### 5. Environment Variables

Add any necessary environment variables. For basic setup, you can leave this as is since our `.coolify.yaml` already defines the necessary variables.

### 6. Deploy

Click the "Deploy" button to start the deployment process. You can monitor the deployment logs in real-time.

### 7. Access Your API

Once deployment is complete, you'll be provided with a URL to access your API. The URL will be in the format:
- `https://fastapi-api-xxxx.your-coolify-domain.com`

## Verifying Deployment

### Check the Health Endpoint

```bash
curl https://your-coolify-url.com/health
```

Expected response:
```json
{"status": "healthy"}
```

### Explore the API Documentation

Open a web browser and navigate to:
```
https://your-coolify-url.com/docs
```

This will open the interactive Swagger UI documentation, where you can test all the API endpoints directly in your browser.

## Troubleshooting

### Common Issues

1. **Port Configuration**:
   - Ensure the port in the start command matches the exposed port (80)

2. **Build Failures**:
   - Check the build logs for any errors
   - Verify requirements.txt contains all necessary dependencies

3. **Runtime Errors**:
   - Check the logs for any runtime errors
   - Verify environment variables are correctly set

### Viewing Logs

1. Go to your service in the Coolify dashboard
2. Click on "Logs" to view real-time logs
3. Use these logs to diagnose any issues

## Updating Your Deployment

To update your deployment after pushing changes to your Git repository:

1. Go to your service in the Coolify dashboard
2. Click "Redeploy" to deploy the latest changes

Coolify also supports automatic deployments on Git push if you enable webhooks. 