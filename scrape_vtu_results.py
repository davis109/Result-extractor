import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from datetime import datetime
import urllib3
import os
import webbrowser
import re

# Disable SSL verification warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_result(usn, captcha_code):
    base_url = "https://results.vtu.ac.in/DJcbcs25/"
    url = base_url + "index.php"
    
    # Headers to mimic a browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Origin': 'https://results.vtu.ac.in',
        'Referer': 'https://results.vtu.ac.in/DJcbcs25/index.php',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    # Create a session to maintain cookies
    session = requests.Session()
    session.verify = False
    
    try:
        # Get the initial page to get any tokens/cookies
        initial_response = session.get(url, headers=headers)
        initial_soup = BeautifulSoup(initial_response.text, 'html.parser')
        
        # Debug: Print form elements
        form = initial_soup.find('form')
        form_action = "resultpage.php"  # Default action
        
        if form:
            if form.get('action'):
                form_action = form.get('action')
            print(f"Form action: {form_action}")
            print(f"Form method: {form.get('method', 'No method')}")
            
            # Find the USN input field to get the correct name
            usn_input = form.find('input', {'placeholder': 'ENTER USN'})
            usn_field_name = 'lns'  # Default
            if usn_input and usn_input.get('name'):
                usn_field_name = usn_input.get('name')
                print(f"Found USN field name: {usn_field_name}")
        
        # Prepare form data
        data = {
            usn_field_name: usn,  # Use the correct field name for USN
            "captchacode": captcha_code,
            "submit": "Submit"
        }
        
        # Look for any hidden form fields
        hidden_inputs = initial_soup.find_all("input", type="hidden")
        for hidden in hidden_inputs:
            if hidden.get('name'):
                data[hidden.get('name')] = hidden.get('value', '')
                print(f"Found hidden field: {hidden.get('name')} = {hidden.get('value', '')}")
        
        # Submit the form to the correct action URL
        form_submit_url = base_url + form_action
        print(f"Submitting form to: {form_submit_url}")
        print(f"Submitting form with data: {data}")
        response = session.post(form_submit_url, data=data, headers=headers)
        
        # Debug response
        print(f"Response status: {response.status_code}")
        print(f"Response URL: {response.url}")
        
        # Debug: Save the response HTML for inspection
        with open("response.html", "w", encoding="utf-8") as f:
            f.write(response.text)
        print("Response HTML saved to response.html")
        
        # Parse the response
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Check for CAPTCHA error
        if "Invalid captcha code" in response.text:
            print("ERROR: Invalid CAPTCHA code entered")
            return None
            
        # Check for other errors
        if "alert" in response.text and "window.location.href" in response.text:
            error_match = re.search(r"alert\('([^']+)'\)", response.text)
            if error_match:
                error_message = error_match.group(1)
                print(f"ERROR: {error_message}")
                return None
        
        # Check for error messages
        error_msg = soup.find('div', {'class': 'alert-danger'})
        if error_msg:
            print(f"Error message: {error_msg.text.strip()}")
            return None
            
        # Find all tables
        tables = soup.find_all('table')
        print(f"Number of tables found: {len(tables)}")
        
        # Try to find the results table - more flexible approach
        table = None
        for t in tables:
            # Check if this looks like a results table
            if t.find('th') and 'Subject' in t.find('th').text:
                table = t
                break
            # Alternative check for class
            if t.get('class') and ('table-bordered' in t.get('class') or 'table' in t.get('class')):
                table = t
                break
        
        if not table:
            print("No results table found")
            return None
            
        # Extract student name and other details
        student_info = {}
        
        # Look for student details in various formats
        div_details = soup.find('div', {'class': 'col-md-12'})
        if div_details:
            info_divs = div_details.find_all('div', {'class': 'col-md-3'})
            for div in info_divs:
                text = div.text.strip()
                if ':' in text:
                    key, value = text.split(':', 1)
                    student_info[key.strip()] = value.strip()
        
        # Alternative way to find student info
        student_name_elem = soup.find(string=re.compile('Student Name', re.IGNORECASE))
        if student_name_elem:
            parent = student_name_elem.parent
            if parent:
                text = parent.text.strip()
                if ':' in text:
                    key, value = text.split(':', 1)
                    student_info[key.strip()] = value.strip()
        
        # Extract subject-wise marks
        results = {}
        
        if table:
            rows = table.find_all('tr')[1:]  # Skip header row
            
            for row in rows:
                cols = row.find_all('td')
                if len(cols) >= 4:  # Adjust based on actual table structure
                    subject_code = cols[0].text.strip()
                    subject_name = cols[1].text.strip() if len(cols) > 1 else ""
                    
                    # Handle different table structures
                    if len(cols) >= 6:
                        internal_marks = cols[2].text.strip()
                        external_marks = cols[3].text.strip()
                        total_marks = cols[4].text.strip()
                        result = cols[5].text.strip()
                    elif len(cols) >= 5:
                        internal_marks = cols[2].text.strip()
                        external_marks = cols[3].text.strip()
                        total_marks = cols[4].text.strip()
                        result = ""
                    else:
                        internal_marks = ""
                        external_marks = ""
                        total_marks = cols[2].text.strip() if len(cols) > 2 else ""
                        result = cols[3].text.strip() if len(cols) > 3 else ""
                    
                    # Store in results dictionary
                    results[subject_code] = {
                        'Subject Name': subject_name,
                        'Internal': internal_marks,
                        'External': external_marks,
                        'Total': total_marks,
                        'Result': result
                    }
        
        # Add student info to results
        for key, value in student_info.items():
            results[key] = value
            
        # Add USN
        results['USN'] = usn
        
        if not results:
            print(f"No marks data found in table for {usn}")
            return None
        else:
            print(f"Found data for {usn}: {len(results)} entries")
            return results
            
    except Exception as e:
        print(f"Error fetching results for {usn}: {str(e)}")
        return None

def main():
    # Generate USN list - using the correct pattern 1AT22CS
    usn_list = [f"1AT22CS{str(i).zfill(3)}" for i in range(1, 121)]
    
    # Store all results
    all_results = []
    
    # Open the website in the default browser
    print("Opening the VTU results website in your browser...")
    webbrowser.open("https://results.vtu.ac.in/DJcbcs25/index.php")
    
    print("\nINSTRUCTIONS:")
    print("1. For each USN, you'll need to enter the CAPTCHA code shown on the website")
    print("2. Type 'skip' to skip a USN")
    print("3. Type 'exit' to stop the process and save results collected so far")
    print("4. The script will process USNs from 1AT22CS001 to 1AT22CS120\n")
    
    # Process each USN
    for usn in usn_list:
        print(f"\nProcessing {usn}...")
        
        # Ask user to enter the CAPTCHA
        captcha_code = input(f"Enter the CAPTCHA code for {usn} (or 'skip' to skip, 'exit' to stop): ")
        
        if captcha_code.lower() == 'skip':
            print(f"Skipping {usn}")
            continue
            
        if captcha_code.lower() == 'exit':
            print("Exiting the script")
            break
        
        results = get_result(usn, captcha_code)
        
        if results:
            all_results.append(results)
            print(f"Successfully added results for {usn}")
        else:
            print(f"No results found for {usn} or incorrect CAPTCHA")
        
        # Ask if user wants to continue
        continue_option = input("Press Enter to continue to next USN, or type 'exit' to stop: ")
        if continue_option.lower() == 'exit':
            break
    
    # Convert to DataFrame
    if all_results:
        # Create a normalized DataFrame
        # First, extract all possible subject codes
        all_subjects = set()
        for result in all_results:
            for key in result.keys():
                if isinstance(key, str) and key.startswith(('1', '2')) and len(key) >= 6:  # Subject codes
                    all_subjects.add(key)
        
        # Create rows for the DataFrame
        rows = []
        for result in all_results:
            row = {'USN': result.get('USN', '')}
            
            # Add student info
            for key, value in result.items():
                if isinstance(key, str) and not (key.startswith(('1', '2')) and len(key) >= 6):  # Not a subject code
                    if key != 'USN':  # Already added
                        row[key] = value
            
            # Add subject marks
            for subject in all_subjects:
                if subject in result:
                    subject_data = result[subject]
                    if isinstance(subject_data, dict):
                        row[f"{subject}_Name"] = subject_data.get('Subject Name', '')
                        row[f"{subject}_Internal"] = subject_data.get('Internal', '')
                        row[f"{subject}_External"] = subject_data.get('External', '')
                        row[f"{subject}_Total"] = subject_data.get('Total', '')
                        row[f"{subject}_Result"] = subject_data.get('Result', '')
            
            rows.append(row)
        
        # Create DataFrame
        df = pd.DataFrame(rows)
        
        # Save to Excel with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        excel_filename = f"vtu_results_{timestamp}.xlsx"
        df.to_excel(excel_filename, index=False)
        print(f"\nResults saved to {excel_filename}")
        
        # Open the Excel file
        try:
            os.startfile(excel_filename)
            print(f"Excel file opened. Check {excel_filename} for the results.")
        except:
            print(f"Excel file saved but could not be opened automatically. Please open {excel_filename} manually.")
    else:
        print("\nNo results were collected!")

if __name__ == "__main__":
    main() 