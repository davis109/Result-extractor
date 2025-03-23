# Deploying the VTU Results Scraper (All-in-One Version)

This guide provides step-by-step instructions for deploying the all-in-one version of the VTU Results Scraper to Render.com.

## What is the All-in-One Version?

This is a simplified version of the VTU Results Scraper with these key features:
- **Templates embedded in the Python file** - No need for external HTML files
- **Demo mode only** - Uses static sample data instead of scraping websites
- **Minimal dependencies** - No Chrome or Selenium required
- **Easy deployment** - Just a single Python file and minimal configuration

## Files for Deployment

You need just these files:
- `all_in_one_app.py` - The main application with embedded templates
- `all_in_one_requirements.txt` - Minimal dependencies
- `all_in_one_procfile` - Gunicorn configuration

## Deployment Steps

### 1. Prepare Your Repository

1. Create a GitHub repository
2. Add the files above, but rename them as follows:
   - Rename `all_in_one_app.py` to `app.py`
   - Rename `all_in_one_requirements.txt` to `requirements.txt`
   - Rename `all_in_one_procfile` to `Procfile`

### 2. Deploy to Render

1. Log in to [Render](https://render.com/)
2. Click "New" and select "Web Service"
3. Connect your GitHub repository
4. Configure the service:
   - **Name**: `vtu-results-scraper` (or your preferred name)
   - **Runtime**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: Free

5. Click "Create Web Service" and wait for deployment to complete (usually just 1-2 minutes)

### 3. Access Your Application

Once deployed, you can access your application at the URL Render provides (e.g., `https://vtu-results-scraper.onrender.com`).

## How It Works

This version is designed to be as simple as possible:

1. It uses Flask's `render_template_string` function to serve HTML directly from strings in the Python file
2. All static data is included directly in the Python file
3. Excel files are generated on-the-fly when needed
4. No external template files or database needed

## Local Development

To run the application locally:

1. Install the dependencies:
   ```bash
   pip install -r all_in_one_requirements.txt
   ```

2. Run the Flask app:
   ```bash
   python all_in_one_app.py
   ```

3. Visit `http://localhost:5000` in your browser 