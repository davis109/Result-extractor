# VTU Results Scraper

This script automates the process of extracting student results from the VTU results website and saves them to an Excel file.

## Features

- Automatically enters USN numbers
- Can automatically solve CAPTCHAs with a 2Captcha API key
- Extracts subject-wise marks and student details
- Saves all results to an Excel file

## Requirements

- Python 3.6+
- Chrome browser
- ChromeDriver (automatically installed with selenium-manager)
- Required Python packages (install using `pip install -r requirements.txt`)

## Setup

1. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

2. For automatic CAPTCHA solving (optional):
   - Sign up at [2Captcha](https://2captcha.com/)
   - Get an API key
   - Update the `API_KEY` variable in `selenium_vtu_results.py`

## Usage

1. Run the script:
   ```
   python selenium_vtu_results.py
   ```

2. The script will:
   - Open Chrome browser
   - Navigate to the VTU results page
   - Process USNs from 1AT22CS001 to 1AT22CS120
   - Save results to an Excel file

3. If you don't have a 2Captcha API key:
   - You'll need to manually enter the CAPTCHA for each USN
   - Press Enter in the terminal after submitting each form
   - Type 'skip' to skip a USN
   - Type 'exit' to stop the process and save results collected so far

## Notes

- The script respects the website by adding delays between requests
- Using automated CAPTCHA solving services may be against the website's terms of service
- Use this script responsibly and for educational purposes only

## Troubleshooting

- If the script can't find the USN input field, try updating the selectors in the code
- If the CAPTCHA solving fails, you can still enter it manually
- If the script can't extract results, check if the website structure has changed 