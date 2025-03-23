# VTU Results Scraper - Hosted Version

This web application allows you to scrape VTU (Visvesvaraya Technological University) results by providing a range of USNs. It displays the results in a table and allows downloading them as an Excel file.

## Features

- Web-based interface for easy use
- Automatic CAPTCHA solving using 2Captcha service (if API key is provided)
- Excel export of results
- Processing logs to track progress
- Responsive design

## Requirements

- Python 3.8 or higher
- Chrome browser (for Selenium)
- ChromeDriver (installed automatically by webdriver-manager)
- 2Captcha API key (optional, for automatic CAPTCHA solving)

## Installation

1. Clone this repository or download the source code
2. Install the required packages:

```bash
pip install -r requirements_hosting.txt
```

## Usage

1. Run the application:

```bash
python vtu_results_hosted.py
```

2. Open your browser and navigate to `http://localhost:5000`
3. Enter the start and end USNs (e.g., 1AT22CS001 to 1AT22CS010)
4. Click "Scrape Results" button
5. If automatic CAPTCHA solving is enabled, the application will attempt to solve CAPTCHAs automatically
6. View the results in the table and download the Excel file if needed

## Configuration

To enable automatic CAPTCHA solving, replace the `API_KEY` value in `vtu_results_hosted.py` with your 2Captcha API key:

```python
API_KEY = "YOUR_2CAPTCHA_API_KEY"  # Replace with your actual 2Captcha API key
```

You can sign up for a 2Captcha account at [2captcha.com](https://2captcha.com/).

## Deploying to a Hosting Service

### Heroku

1. Create a `Procfile` with the following content:
```
web: gunicorn vtu_results_hosted:app
```

2. Follow Heroku deployment steps:
```bash
heroku create
git add .
git commit -m "Initial commit"
git push heroku master
```

### Render

1. Create a `render.yaml` file:
```yaml
services:
  - type: web
    name: vtu-results-scraper
    env: python
    buildCommand: pip install -r requirements_hosting.txt
    startCommand: gunicorn vtu_results_hosted:app
    envVars:
      - key: PYTHON_VERSION
        value: 3.9.0
```

2. Deploy to Render using their dashboard by pointing to your GitHub repository.

## Limitations

- The application is limited to processing 10 USNs at a time to avoid timeouts
- Automatic CAPTCHA solving requires a valid 2Captcha API key and credits on your account
- The application requires Chrome browser and ChromeDriver to run

## Legal Disclaimer

This tool is for educational purposes only. Use it responsibly and in accordance with VTU's terms of service. The developer is not responsible for any misuse of this application.

## License

MIT 