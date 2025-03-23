# VTU Results Scraper

This web application automates the process of extracting student results from the VTU results website and saves them to an Excel file.

## Features

- Automatically enters USN numbers
- Manual CAPTCHA entry to ensure high success rate
- Extracts subject-wise marks and student details
- Saves all results to an Excel file
- Web interface for easy access

## Local Setup

1. Install the required packages:
   ```
   pip install -r requirements_web.txt
   ```

2. Run the Flask app:
   ```
   python app.py
   ```

3. Open your browser and navigate to `http://localhost:5000`

## Deployment Instructions

### Deploy to Render (100% Free)

1. Create a Render account at https://render.com/

2. Create a new Web Service:
   - Connect your GitHub repository
   - Name: `vtu-results-scraper` (or any name you prefer)
   - Runtime: Python 3
   - Build Command: `pip install -r requirements_web.txt`
   - Start Command: `gunicorn app:app`
   - Select the Free plan

3. Note that for the deployed version:
   - A Chrome window needs to be visible for CAPTCHA entry
   - You may need to use a service with a GUI environment for this to work
   - Consider using your local computer for production use if CAPTCHA is needed

## Usage

1. Enter the starting USN (e.g., 1AT22CS001)
2. Enter the ending USN (e.g., 1AT22CS010)
3. Click "Scrape Results"
4. A Chrome browser window will open automatically
5. Enter the CAPTCHA code shown in the browser window
6. Click the Submit button in the browser
7. Wait for the results to be processed
8. Repeat for each USN in the range
9. View and download the final results

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