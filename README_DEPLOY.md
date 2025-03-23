# VTU Results Scraper - Demo Deployment

This is a simplified version of the VTU Results Scraper that uses static demo data. It's designed to be easily deployed to Render without requiring Chrome or Selenium.

## Files for Deployment

- `static_app.py` - The main Flask application file
- `simple_requirements.txt` - Minimal Python dependencies
- `simple_build.sh` - Build script for Render
- `simple_procfile` - Procfile for Render
- `templates/` - HTML templates directory
  - `index.html` - Main interface
  - `demo.html` - Demo interface

## How to Deploy to Render

1. **Create a Git Repository**
   - Push all the files above to a Git repository (GitHub, GitLab, etc.)

2. **Sign Up for Render**
   - Create an account at [render.com](https://render.com)

3. **Create a New Web Service**
   - From your Render dashboard, click "New" → "Web Service"
   - Connect your Git repository or use the public repository URL

4. **Configure the Web Service**
   - **Name**: `vtu-results-scraper` (or your preferred name)
   - **Runtime**: Python
   - **Build Command**: `bash simple_build.sh`
   - **Start Command**: `gunicorn static_app:app`
   - **Plan**: Free

5. **Deploy**
   - Click "Create Web Service"
   - Wait for the deployment to complete (usually takes 1-2 minutes)

6. **Access Your Application**
   - Once deployed, Render will provide a URL (e.g., `https://vtu-results-scraper.onrender.com`)
   - Visit this URL to access your application

## Important Notes

- This is a demo version that uses static data
- The Excel download functionality still works
- No need for Chrome installation or Selenium configuration
- No CAPTCHA solving - everything works with fake/demo data

## Local Development

To run the application locally:

1. Install the dependencies:
   ```bash
   pip install -r simple_requirements.txt
   ```

2. Run the Flask app:
   ```bash
   python static_app.py
   ```

3. Visit `http://localhost:5000` in your browser 