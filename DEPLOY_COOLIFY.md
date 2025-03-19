# Deploying to Coolify on Hetzner

A concise guide for deploying this FastAPI application on Hetzner using Coolify.

## Prerequisites

1. A Hetzner server
2. Coolify installed on your server
3. A Git repository with this code

## Installing Coolify

```bash
ssh root@your-server-ip
wget -q https://get.coolify.io -O /tmp/install.sh && bash /tmp/install.sh
```

Access the Coolify dashboard at `https://your-server-ip` and create your admin account.

## Deployment Steps

1. **Push Your Code to Git**
   - Ensure all changes are committed and pushed

2. **Add Your Repository to Coolify**
   - Log in to Coolify dashboard
   - Navigate to "Sources" → "Add New Source"
   - Select your Git provider and repository

3. **Create a New Service**
   - Go to "Services" → "New Service"
   - Select "Application" and your repository

4. **Deploy**
   - Coolify will automatically detect the `.coolify.yaml` configuration
   - Click "Deploy" to start the deployment process

## Verifying Deployment

- **Check the health endpoint**: `curl https://your-url.com/health`
- **API Documentation**: Available at `https://your-url.com/docs`

## Troubleshooting

- Check logs in the Coolify dashboard if deployment fails
- Ensure ports are correctly configured (80 for production)
- Verify all required environment variables are set 