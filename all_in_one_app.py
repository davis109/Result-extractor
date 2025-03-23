from flask import Flask, render_template_string, request, jsonify, send_file
import os
import pandas as pd
from datetime import datetime
import time

# Create Flask app
app = Flask(__name__)

# HTML Templates embedded directly in the Python file
INDEX_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VTU Results Scraper</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            padding-top: 20px;
            padding-bottom: 20px;
            background-color: #f8f9fa;
        }
        .container {
            max-width: 800px;
        }
        .card {
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        #results-section {
            display: none;
        }
        #loading {
            display: none;
            margin: 20px 0;
        }
        footer {
            text-align: center;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #eee;
            color: #777;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="card">
            <div class="card-header bg-primary text-white">
                <h1 class="h3 mb-0">VTU Results Scraper</h1>
            </div>
            <div class="card-body">
                <p class="lead">Enter the USN range to scrape results from VTU website</p>
                
                <div id="api-key-status" class="alert alert-warning mb-3">
                    <strong>Demo Mode:</strong> This application is running in demo mode. Results shown are sample data only.
                </div>
                
                <form id="scraper-form">
                    <div class="row mb-3">
                        <div class="col-md-6">
                            <label for="start-usn" class="form-label">Start USN</label>
                            <input type="text" class="form-control" id="start-usn" placeholder="e.g. 1AT22CS001" required>
                        </div>
                        <div class="col-md-6">
                            <label for="end-usn" class="form-label">End USN</label>
                            <input type="text" class="form-control" id="end-usn" placeholder="e.g. 1AT22CS010" required>
                        </div>
                    </div>
                    
                    <div class="form-check mb-3">
                        <input class="form-check-input" type="checkbox" id="interactive-mode" checked>
                        <label class="form-check-label" for="interactive-mode">
                            Interactive Mode (Type CAPTCHA manually in the browser window)
                        </label>
                        <div class="form-text">
                            Enable this to solve CAPTCHAs manually. A Chrome window will open for each USN.
                        </div>
                    </div>
                    
                    <div class="d-grid">
                        <button type="submit" class="btn btn-primary">Scrape Results</button>
                    </div>
                </form>
                
                <div id="loading" class="text-center">
                    <div class="spinner-border text-primary" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                    <p class="mt-2">Scraping VTU results, please wait...</p>
                    <p class="text-muted">This may take a few minutes depending on the number of USNs</p>
                    
                    <!-- Skip/Exit Controls -->
                    <div class="mt-3 mb-2 d-flex justify-content-center gap-2">
                        <button id="skip-usn-btn" class="btn btn-warning">Skip Current USN</button>
                        <button id="exit-process-btn" class="btn btn-danger">Stop & Save Results</button>
                    </div>
                </div>
                
                <div id="logs-section" class="mt-3" style="display: none;">
                    <h5>Processing Logs:</h5>
                    <div id="logs-content" class="border p-2" style="max-height: 200px; overflow-y: auto; font-family: monospace; font-size: 0.8rem; background-color: #f5f5f5;"></div>
                </div>
                
                <div id="error-message" class="alert alert-danger mt-3" style="display: none;"></div>
            </div>
        </div>
        
        <div id="results-section" class="card">
            <div class="card-header bg-success text-white">
                <h2 class="h4 mb-0">Results</h2>
            </div>
            <div class="card-body">
                <p id="results-count" class="mb-3"></p>
                <div class="table-responsive">
                    <table class="table table-striped" id="results-table">
                        <thead>
                            <tr>
                                <th>USN</th>
                                <th>Name</th>
                                <th>Semester</th>
                                <th>Total Marks</th>
                                <th>Result</th>
                            </tr>
                        </thead>
                        <tbody id="results-body"></tbody>
                    </table>
                </div>
                <div class="d-grid gap-2 d-md-flex justify-content-md-center mt-3">
                    <button id="download-excel" class="btn btn-success">Download Excel</button>
                </div>
            </div>
        </div>
        
        <footer>
            <p>VTU Results Scraper - For educational purposes only</p>
            <p>© {{ current_year }}</p>
            <p><a href="/demo">View Demo (No Selenium Required)</a></p>
        </footer>
    </div>

    <script>
        document.addEventListener('DOMContentLoaded', function() {
            // Set the API status to demo mode
            const apiKeyStatus = document.getElementById('api-key-status');
            apiKeyStatus.className = 'alert alert-info mb-3';
            apiKeyStatus.innerHTML = '<strong>Demo Mode:</strong> This application is running in demo mode with sample data.';
            
            // Add event listeners for skip and exit buttons
            document.getElementById('skip-usn-btn').addEventListener('click', skipCurrentUSN);
            document.getElementById('exit-process-btn').addEventListener('click', exitProcess);
        });
        
        // Function to skip the current USN
        async function skipCurrentUSN() {
            try {
                const response = await fetch('/api/run_script', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ 
                        start_usn: document.getElementById('start-usn').value, 
                        end_usn: document.getElementById('end-usn').value,
                        interactive_mode: document.getElementById('interactive-mode').checked,
                        skip_usn: true
                    }),
                });
                
                const result = await response.json();
                
                // Update logs
                if (result.logs && result.logs.length > 0) {
                    const logsContent = document.getElementById('logs-content');
                    logsContent.innerHTML = result.logs.join('<br>');
                    document.getElementById('logs-section').style.display = 'block';
                }
                
                if (response.ok) {
                    displayResults(result);
                } else {
                    let errorMessage = result.message || 'An error occurred while processing the skip request';
                    showError(errorMessage);
                }
            } catch (error) {
                showError('Failed to connect to the server. Please try again later.');
                console.error(error);
            } finally {
                document.getElementById('loading').style.display = 'none';
            }
        }
        
        // Function to exit the process and save current results
        async function exitProcess() {
            try {
                const response = await fetch('/api/run_script', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ 
                        start_usn: document.getElementById('start-usn').value, 
                        end_usn: document.getElementById('end-usn').value,
                        interactive_mode: document.getElementById('interactive-mode').checked,
                        exit_process: true
                    }),
                });
                
                const result = await response.json();
                
                // Update logs
                if (result.logs && result.logs.length > 0) {
                    const logsContent = document.getElementById('logs-content');
                    logsContent.innerHTML = result.logs.join('<br>');
                    document.getElementById('logs-section').style.display = 'block';
                }
                
                if (response.ok) {
                    displayResults(result);
                } else {
                    let errorMessage = result.message || 'An error occurred while processing the exit request';
                    showError(errorMessage);
                }
            } catch (error) {
                showError('Failed to connect to the server. Please try again later.');
                console.error(error);
            } finally {
                document.getElementById('loading').style.display = 'none';
            }
        }

        document.getElementById('scraper-form').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const startUsn = document.getElementById('start-usn').value;
            const endUsn = document.getElementById('end-usn').value;
            
            document.getElementById('error-message').style.display = 'none';
            document.getElementById('loading').style.display = 'block';
            document.getElementById('results-section').style.display = 'none';
            document.getElementById('logs-section').style.display = 'none';
            
            try {
                // Try using the run_script endpoint first (for compatibility with original UI)
                const response = await fetch('/api/run_script', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ 
                        start_usn: startUsn, 
                        end_usn: endUsn,
                        interactive_mode: document.getElementById('interactive-mode').checked
                    }),
                });
                
                const result = await response.json();
                
                // Display logs if available
                if (result.logs && result.logs.length > 0) {
                    const logsContent = document.getElementById('logs-content');
                    logsContent.innerHTML = result.logs.join('<br>');
                    document.getElementById('logs-section').style.display = 'block';
                }
                
                if (response.ok) {
                    displayResults(result);
                } else {
                    let errorMessage = result.message || 'An error occurred while scraping results';
                    showError(errorMessage);
                }
            } catch (error) {
                showError('Failed to connect to the server. Please try again later.');
                console.error(error);
            } finally {
                document.getElementById('loading').style.display = 'none';
            }
        });
        
        function displayResults(data) {
            const resultsBody = document.getElementById('results-body');
            resultsBody.innerHTML = '';
            
            document.getElementById('results-count').textContent = `Found ${data.data.length} results`;
            
            data.data.forEach(student => {
                const row = document.createElement('tr');
                
                const usnCell = document.createElement('td');
                usnCell.textContent = student.USN;
                row.appendChild(usnCell);
                
                const nameCell = document.createElement('td');
                nameCell.textContent = student.Name;
                row.appendChild(nameCell);
                
                const semesterCell = document.createElement('td');
                semesterCell.textContent = student.Semester;
                row.appendChild(semesterCell);
                
                const totalCell = document.createElement('td');
                totalCell.textContent = student.Total;
                row.appendChild(totalCell);
                
                const resultCell = document.createElement('td');
                resultCell.textContent = student.Result;
                resultCell.className = student.Result === 'PASS' ? 'text-success fw-bold' : 'text-danger fw-bold';
                row.appendChild(resultCell);
                
                resultsBody.appendChild(row);
            });
            
            document.getElementById('results-section').style.display = 'block';
            
            // Setup download button
            document.getElementById('download-excel').onclick = function() {
                window.location.href = '/download/' + data.filename;
            };
        }
        
        function showError(message) {
            const errorElement = document.getElementById('error-message');
            errorElement.textContent = message;
            errorElement.style.display = 'block';
        }
    </script>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

DEMO_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VTU Results Scraper - Demo</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            padding-top: 20px;
            padding-bottom: 20px;
            background-color: #f8f9fa;
        }
        .container {
            max-width: 800px;
        }
        .card {
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        #results-section {
            display: none;
        }
        #loading {
            display: none;
            margin: 20px 0;
        }
        footer {
            text-align: center;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #eee;
            color: #777;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="card">
            <div class="card-header bg-primary text-white">
                <h1 class="h3 mb-0">VTU Results Scraper - Demo Mode</h1>
            </div>
            <div class="card-body">
                <div class="alert alert-info mb-3">
                    <strong>Demo Mode:</strong> This is the demo version of the VTU Results Scraper. 
                    It shows sample data only and does not connect to the actual VTU website.
                    No Selenium or Chrome browser is required.
                </div>
                
                <p class="lead">Enter any USN range to see demo results</p>
                
                <form id="demo-form">
                    <div class="row mb-3">
                        <div class="col-md-6">
                            <label for="start-usn" class="form-label">Start USN</label>
                            <input type="text" class="form-control" id="start-usn" placeholder="e.g. 1AT22CS001" value="1AT22CS001" required>
                        </div>
                        <div class="col-md-6">
                            <label for="end-usn" class="form-label">End USN</label>
                            <input type="text" class="form-control" id="end-usn" placeholder="e.g. 1AT22CS010" value="1AT22CS005" required>
                        </div>
                    </div>
                    
                    <div class="d-grid">
                        <button type="submit" class="btn btn-primary">Generate Demo Results</button>
                    </div>
                </form>
                
                <div id="loading" class="text-center">
                    <div class="spinner-border text-primary" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                    <p class="mt-2">Generating demo results, please wait...</p>
                    
                    <!-- Skip/Exit Controls -->
                    <div class="mt-3 mb-2 d-flex justify-content-center gap-2">
                        <button id="skip-usn-btn" class="btn btn-warning">Skip Current USN</button>
                        <button id="exit-process-btn" class="btn btn-danger">Stop & Save Results</button>
                    </div>
                </div>
                
                <div id="logs-section" class="mt-3" style="display: none;">
                    <h5>Demo Logs:</h5>
                    <div id="logs-content" class="border p-2" style="max-height: 200px; overflow-y: auto; font-family: monospace; font-size: 0.8rem; background-color: #f5f5f5;"></div>
                </div>
                
                <div id="error-message" class="alert alert-danger mt-3" style="display: none;"></div>
            </div>
        </div>
        
        <div id="results-section" class="card">
            <div class="card-header bg-success text-white">
                <h2 class="h4 mb-0">Demo Results</h2>
            </div>
            <div class="card-body">
                <p id="results-count" class="mb-3"></p>
                <div class="table-responsive">
                    <table class="table table-striped" id="results-table">
                        <thead>
                            <tr>
                                <th>USN</th>
                                <th>Name</th>
                                <th>Semester</th>
                                <th>Total Marks</th>
                                <th>Result</th>
                            </tr>
                        </thead>
                        <tbody id="results-body"></tbody>
                    </table>
                </div>
                <div class="d-grid gap-2 d-md-flex justify-content-md-center mt-3">
                    <button id="download-excel" class="btn btn-success">Download Excel</button>
                </div>
            </div>
        </div>
        
        <footer>
            <p>VTU Results Scraper - For educational purposes only</p>
            <p>© {{ current_year }}</p>
            <p><a href="/">Back to Main Page</a></p>
        </footer>
    </div>

    <script>
        document.getElementById('demo-form').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const startUsn = document.getElementById('start-usn').value;
            const endUsn = document.getElementById('end-usn').value;
            
            document.getElementById('error-message').style.display = 'none';
            document.getElementById('loading').style.display = 'block';
            document.getElementById('results-section').style.display = 'none';
            document.getElementById('logs-section').style.display = 'none';
            
            try {
                const response = await fetch('/api/run_script', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ 
                        start_usn: startUsn, 
                        end_usn: endUsn,
                        interactive_mode: false
                    }),
                });
                
                const result = await response.json();
                
                // Display logs if available
                if (result.logs && result.logs.length > 0) {
                    const logsContent = document.getElementById('logs-content');
                    logsContent.innerHTML = result.logs.join('<br>');
                    document.getElementById('logs-section').style.display = 'block';
                }
                
                if (response.ok) {
                    displayResults(result);
                } else {
                    let errorMessage = result.message || 'An error occurred while generating demo results';
                    showError(errorMessage);
                }
            } catch (error) {
                showError('Failed to connect to the server. Please try again later.');
                console.error(error);
            } finally {
                document.getElementById('loading').style.display = 'none';
            }
        });
        
        // Add event listeners for skip and exit buttons
        document.addEventListener('DOMContentLoaded', function() {
            document.getElementById('skip-usn-btn').addEventListener('click', skipCurrentUSN);
            document.getElementById('exit-process-btn').addEventListener('click', exitProcess);
        });
        
        // Function to skip the current USN
        async function skipCurrentUSN() {
            try {
                const response = await fetch('/api/run_script', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ 
                        start_usn: document.getElementById('start-usn').value, 
                        end_usn: document.getElementById('end-usn').value,
                        interactive_mode: false,
                        skip_usn: true
                    }),
                });
                
                const result = await response.json();
                
                // Update logs
                if (result.logs && result.logs.length > 0) {
                    const logsContent = document.getElementById('logs-content');
                    logsContent.innerHTML = result.logs.join('<br>');
                    document.getElementById('logs-section').style.display = 'block';
                }
                
                if (response.ok) {
                    displayResults(result);
                } else {
                    let errorMessage = result.message || 'An error occurred while processing the skip request';
                    showError(errorMessage);
                }
            } catch (error) {
                showError('Failed to connect to the server. Please try again later.');
                console.error(error);
            } finally {
                document.getElementById('loading').style.display = 'none';
            }
        }
        
        // Function to exit the process and save current results
        async function exitProcess() {
            try {
                const response = await fetch('/api/run_script', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ 
                        start_usn: document.getElementById('start-usn').value, 
                        end_usn: document.getElementById('end-usn').value,
                        interactive_mode: false,
                        exit_process: true
                    }),
                });
                
                const result = await response.json();
                
                // Update logs
                if (result.logs && result.logs.length > 0) {
                    const logsContent = document.getElementById('logs-content');
                    logsContent.innerHTML = result.logs.join('<br>');
                    document.getElementById('logs-section').style.display = 'block';
                }
                
                if (response.ok) {
                    displayResults(result);
                } else {
                    let errorMessage = result.message || 'An error occurred while processing the exit request';
                    showError(errorMessage);
                }
            } catch (error) {
                showError('Failed to connect to the server. Please try again later.');
                console.error(error);
            } finally {
                document.getElementById('loading').style.display = 'none';
            }
        }
        
        function displayResults(data) {
            const resultsBody = document.getElementById('results-body');
            resultsBody.innerHTML = '';
            
            document.getElementById('results-count').textContent = `Generated ${data.data.length} demo results`;
            
            data.data.forEach(student => {
                const row = document.createElement('tr');
                
                const usnCell = document.createElement('td');
                usnCell.textContent = student.USN;
                row.appendChild(usnCell);
                
                const nameCell = document.createElement('td');
                nameCell.textContent = student.Name;
                row.appendChild(nameCell);
                
                const semesterCell = document.createElement('td');
                semesterCell.textContent = student.Semester;
                row.appendChild(semesterCell);
                
                const totalCell = document.createElement('td');
                totalCell.textContent = student.Total;
                row.appendChild(totalCell);
                
                const resultCell = document.createElement('td');
                resultCell.textContent = student.Result;
                resultCell.className = student.Result === 'PASS' ? 'text-success fw-bold' : 'text-danger fw-bold';
                row.appendChild(resultCell);
                
                resultsBody.appendChild(row);
            });
            
            document.getElementById('results-section').style.display = 'block';
            
            // Setup download button
            document.getElementById('download-excel').onclick = function() {
                window.location.href = '/download/' + data.filename;
            };
        }
        
        function showError(message) {
            const errorElement = document.getElementById('error-message');
            errorElement.textContent = message;
            errorElement.style.display = 'block';
        }
    </script>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

# Demo data for testing
DEMO_DATA = [
    {
        "USN": "1AT22CS001",
        "Name": "ADITYA KUMAR",
        "Semester": "4",
        "Total": "625/800",
        "Result": "PASS",
        "SGPA": "8.75"
    },
    {
        "USN": "1AT22CS002",
        "Name": "AKSHAY SHARMA",
        "Semester": "4",
        "Total": "710/800",
        "Result": "PASS",
        "SGPA": "9.25"
    },
    {
        "USN": "1AT22CS003",
        "Name": "ANANYA PATEL",
        "Semester": "4",
        "Total": "590/800",
        "Result": "PASS",
        "SGPA": "8.00"
    },
    {
        "USN": "1AT22CS004",
        "Name": "ANIRUDH REDDY",
        "Semester": "4",
        "Total": "450/800",
        "Result": "FAIL",
        "SGPA": "5.50"
    },
    {
        "USN": "1AT22CS005",
        "Name": "BHAVANA SINGH",
        "Semester": "4",
        "Total": "680/800",
        "Result": "PASS",
        "SGPA": "8.85"
    }
]

# Demo logs for display
DEMO_LOGS = [
    "Starting process for 5 USNs",
    "Processing 1AT22CS001...",
    "Accessing VTU Results website",
    "Successfully extracted details for 1AT22CS001",
    "Processing 1AT22CS002...",
    "Accessing VTU Results website",
    "Successfully extracted details for 1AT22CS002",
    "Processing 1AT22CS003...",
    "Accessing VTU Results website",
    "Successfully extracted details for 1AT22CS003",
    "Processing 1AT22CS004...",
    "Accessing VTU Results website",
    "Successfully extracted details for 1AT22CS004",
    "Processing 1AT22CS005...",
    "Accessing VTU Results website",
    "Successfully extracted details for 1AT22CS005",
    "All USNs processed successfully",
    "Generating Excel file..."
]

# Global variable to store the last excel filename
last_excel_filename = None

@app.route('/')
def index():
    """Render the main page."""
    return render_template_string(INDEX_HTML, current_year=datetime.now().year)

@app.route('/demo')
def demo():
    """Render the demo page."""
    return render_template_string(DEMO_HTML, current_year=datetime.now().year)

@app.route('/api/check_api_key', methods=['GET'])
def check_api_key():
    """Check if 2Captcha API key is configured."""
    return jsonify({'api_key_configured': False})

@app.route('/api/run_script', methods=['POST'])
def run_script():
    """API endpoint for running the script."""
    try:
        global last_excel_filename
        
        data = request.json
        start_usn = data.get('start_usn')
        end_usn = data.get('end_usn')
        interactive_mode = data.get('interactive_mode', False)
        skip_usn = data.get('skip_usn', False)  # New parameter for skipping current USN
        exit_process = data.get('exit_process', False)  # New parameter for exiting the process
        
        if not start_usn or not end_usn:
            return jsonify({'error': 'Start and end USN required'}), 400
        
        # If exit_process is True, return early with partial results
        if exit_process:
            # Generate a unique filename for this session
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            last_excel_filename = f"results_{timestamp}_partial.xlsx"
            
            # Use a subset of the demo data (simulating partial results)
            partial_data = DEMO_DATA[:2]  # Just the first 2 records
            
            # Create DataFrame and save to Excel
            df = pd.DataFrame(partial_data)
            df.to_excel(last_excel_filename, index=False)
            
            # Return success response with partial data
            logs = DEMO_LOGS[:5] + ["Process exited by user request", "Generating partial results Excel file..."]
            return jsonify({
                'status': 'success',
                'message': 'Process exited with partial results',
                'data': partial_data,
                'filename': last_excel_filename,
                'logs': logs
            })
        
        # If skip_usn is True, simulate skipping the current USN
        if skip_usn:
            logs = DEMO_LOGS.copy()
            logs.insert(4, "User requested to skip USN 1AT22CS002")
            logs.remove("Successfully extracted details for 1AT22CS002")
            
            # Filter out the skipped USN from results
            filtered_data = [item for item in DEMO_DATA if item['USN'] != '1AT22CS002']
            
            # Generate a unique filename for this session
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            last_excel_filename = f"results_{timestamp}.xlsx"
            
            # Create DataFrame and save to Excel
            df = pd.DataFrame(filtered_data)
            df.to_excel(last_excel_filename, index=False)
            
            # Return success response with filtered data
            return jsonify({
                'status': 'success',
                'message': 'Results scraped successfully (Demo Mode, with skipped USN)',
                'data': filtered_data,
                'filename': last_excel_filename,
                'logs': logs
            })
        
        # Regular processing (no skip or exit)
        # Generate a unique filename for this session
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        last_excel_filename = f"results_{timestamp}.xlsx"
        
        # Simulate processing delay
        time.sleep(2)
        
        # Create DataFrame and save to Excel
        df = pd.DataFrame(DEMO_DATA)
        df.to_excel(last_excel_filename, index=False)
        
        # Return success response with demo data
        return jsonify({
            'status': 'success',
            'message': 'Results scraped successfully (Demo Mode)',
            'data': DEMO_DATA,
            'filename': last_excel_filename,
            'logs': DEMO_LOGS
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'An unexpected error occurred: {str(e)}'
        }), 500

@app.route('/download/<filename>')
def download_file(filename):
    """Download the Excel file."""
    try:
        return send_file(filename, as_attachment=True)
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error downloading file: {str(e)}'
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True) 