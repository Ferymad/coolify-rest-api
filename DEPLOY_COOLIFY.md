# Deploying to Coolify on Hetzner

A concise guide for deploying this FastAPI application on Hetzner using Coolify.

## Prerequisites

1. A Hetzner server
2. Coolify installed on your server
3. A Git repository with this code
4. PostgreSQL database (managed by Coolify)

## Installing Coolify

```bash
ssh root@your-server-ip
wget -q https://get.coolify.io -O /tmp/install.sh && bash /tmp/install.sh
```

Access the Coolify dashboard at `https://your-server-ip` and create your admin account.

## Database Setup

1. **Create PostgreSQL Database**
   - In Coolify dashboard, go to "Resources" → "Databases"
   - Click "Add New Database"
   - Select "PostgreSQL"
   - Set the following credentials:
     - Username: postgres
     - Password: (generate a secure password)
     - Database: mydb
   - Save the credentials

2. **Configure Environment Variables**
   - In your service settings, add the following environment variables:
     ```
     POSTGRES_USER=postgres
     POSTGRES_PASSWORD=(your-database-password)
     POSTGRES_DB=mydb
     POSTGRES_PORT=5432
     POSTGRES_HOST=(your-database-host)
     ```

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
   - Link the PostgreSQL database resource

4. **Deploy**
   - Coolify will automatically detect the `.coolify.yaml` configuration
   - Click "Deploy" to start the deployment process

## Verifying Deployment

- **Check the health endpoint**: `curl https://your-url.com/health`
- **API Documentation**: Available at `https://your-url.com/docs`
- **Test database connection**: Create a new item using the `/items` endpoint

## Troubleshooting

- Check logs in the Coolify dashboard if deployment fails
- Ensure ports are correctly configured (80 for production)
- Verify all required environment variables are set
- Check database connection logs if items operations fail 