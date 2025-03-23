# VTU Results Scraper Web Application

A web application for scraping and downloading VTU exam results. This application provides both automatic CAPTCHA solving (with a 2Captcha API key) and manual CAPTCHA entry options.

## Features

- Scrape VTU results for a range of USNs
- Interactive mode for manual CAPTCHA entry
- Automatic CAPTCHA solving (requires 2Captcha API key)
- Export results to Excel
- Mobile-friendly interface
- Demo mode without Selenium

## Deployment on Render

### Prerequisites

- A [Render](https://render.com) account
- [Git](https://git-scm.com/downloads) installed on your computer

### Steps to Deploy

1. **Prepare your repository**

   Make sure your repository includes the following files:
   - `vtu_results_hosted.py`
   - `requirements.txt`
   - `Procfile`
   - `chrome-installer.sh`
   - `runtime.txt`
   - `templates/index.html`
   - `templates/demo.html`

2. **Create a new Web Service on Render**

   - Log in to your [Render Dashboard](https://dashboard.render.com/)
   - Click on "New" and select "Web Service"
   - Connect your GitHub/GitLab repository or use the public repository URL
   - Configure your web service with the following settings:
     - **Name**: VTU Results Scraper (or any name you prefer)
     - **Runtime**: Python
     - **Build Command**: `pip install -r requirements.txt && bash chrome-installer.sh`
     - **Start Command**: `gunicorn vtu_results_hosted:app`
     - **Instance Type**: Free (or paid if you need more resources)

3. **Configure Environment Variables**

   Add the following environment variables:
   - `FORCE_DEMO`: Set to `True` if you want to force demo mode
   - `DEVELOPMENT`: Set to `True` for development features
   - `MANUAL_CAPTCHA`: Set to `True` to enable manual CAPTCHA entry

4. **Deploy the Service**

   - Click "Create Web Service"
   - Wait for the build and deployment process to complete

5. **Access Your Web Application**

   - After the deployment is complete, Render will provide a URL to access your web application
   - Visit the URL to use your VTU Results Scraper

## Local Development

1. Clone the repository
2. Install the requirements: `pip install -r requirements.txt`
3. Run the application: `python vtu_results_hosted.py`
4. Visit `http://localhost:5000` in your browser

## Notes for Render Deployment

- The free tier of Render may have limitations in terms of processing power and RAM
- The Chrome installation may take some time during the build process
- The application will run in manual CAPTCHA mode by default
- Set `FORCE_DEMO=True` if you want to avoid the Selenium requirement

## Manual CAPTCHA vs Automatic Processing

This application supports two modes:

1. **Manual CAPTCHA (Default)**: 
   - A Chrome browser window opens for you to enter the CAPTCHA manually
   - Higher success rate as human verification passes CAPTCHA checks
   - Requires user interaction for each USN

2. **Automatic Processing** (Requires code modification):
   - For development or testing purposes only
   - Attempts to solve CAPTCHA automatically (low success rate)
   - Can be enabled by changing `manual_captcha=True` to `False` in app.py

## Notes

- The application respects the website by adding delays between requests
- Using automated CAPTCHA solving services may be against the website's terms of service
- Use this application responsibly and for educational purposes only

## Troubleshooting

- If the browser window doesn't appear, check your Chrome installation
- If the application fails to extract results, the website structure may have changed
- For deployment issues, consider running the application locally with `python app.py` 