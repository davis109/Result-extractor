# Deploying VTU Results Scraper to Render

This guide provides step-by-step instructions for deploying the VTU Results Scraper application to Render.com.

## Prerequisites

- A free [Render](https://render.com) account
- Your code pushed to a GitHub or GitLab repository (or you can use the manual deploy option)

## Deployment Steps

### 1. Prepare Your Repository

Ensure your repository includes these essential files:

- `vtu_results_hosted.py` - Main application file
- `requirements.txt` - Python dependencies
- `Procfile` - Defines the start command
- `build.sh` - Script to run during build
- `chrome-installer.sh` - Script to install Chrome
- `templates/` - Directory containing HTML templates
- `render.yaml` - (Optional) For Blueprint deployment

### 2. Create a New Web Service on Render

1. Log in to your [Render Dashboard](https://dashboard.render.com/)
2. Click **New** and select **Web Service**
3. Connect your repository:
   - Connect your GitHub/GitLab account or
   - Use the **Public Git repository** option with your repo URL

### 3. Configure the Web Service

Fill in the following details:
- **Name**: `vtu-results-scraper` (or choose your own)
- **Region**: Choose the region closest to your users
- **Branch**: `main` (or your preferred branch)
- **Runtime**: `Python 3`
- **Build Command**: `bash build.sh`
- **Start Command**: `gunicorn vtu_results_hosted:app`
- **Plan**: Free

### 4. Add Environment Variables

Click on the **Advanced** button and add these environment variables:

- `PYTHON_VERSION`: `3.11.7`
- `DEVELOPMENT`: `True`
- `MANUAL_CAPTCHA`: `True`
- `FORCE_DEMO`: `False` (Set to `True` to force demo mode without Selenium)

### 5. Create and Deploy

Click the **Create Web Service** button to start the deployment process.

The initial build may take 5-10 minutes as it sets up the environment and installs Chrome.

### 6. Monitor the Deployment

1. Watch the build logs for any errors
2. Once deployed, Render will provide a URL (e.g., `https://vtu-results-scraper.onrender.com`)
3. Visit this URL to access your application

## Troubleshooting

### Chrome Installation Issues

If Chrome fails to install or operate correctly:

1. Check the build logs for specific errors
2. You may need to set `FORCE_DEMO=True` to bypass Selenium/Chrome requirements
3. Consider modifying `chrome-installer.sh` with updated installation instructions

### Memory or Performance Issues

Render's free tier has limited resources:

1. Restrict the number of concurrent USNs being processed
2. Use the demo mode if the full application is too resource-intensive
3. Consider upgrading to a paid plan for better performance

### Application Errors

If the application encounters errors after successful deployment:

1. Check the logs from the Render dashboard
2. Verify that all required environment variables are set correctly
3. Try enabling `FORCE_DEMO=True` to see if the issue is related to Selenium

## Additional Notes

- The application will enter sleep mode after 15 minutes of inactivity on the free tier
- The first request after inactivity may take 30-50 seconds to wake up the service
- Chrome runs in a special configuration on Render to accommodate their containerized environment
- Manual CAPTCHA entry is the most reliable method, especially in the cloud environment 