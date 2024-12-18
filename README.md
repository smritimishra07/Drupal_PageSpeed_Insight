Workflow Description

1. Setup

Environment Preparation:

Install required Python libraries: requests, python-dotenv.

Store the API key securely in a .env file to ensure secure and reusable credentials management.

Directory Structure:

An output folder is created automatically by the script to save JSON reports.

2. Data Fetching

API Call Configuration:

URL: https://www.googleapis.com/pagespeedonline/v5/runPagespeed

Parameters:

url: The website URL entered by the user.

key: API key from .env file.

strategy: Set to desktop (can be changed to mobile if required).

Data Retrieval:

A GET request is made to the PageSpeed Insights API.

If successful, the JSON response is saved locally for further analysis.

Error Handling:

The script gracefully handles errors such as invalid API keys, incorrect URLs, or connectivity issues.

3. Parsing the Report

Focus on Savings:

Metrics with overallSavingsMs greater than 0 are identified as potential optimization areas.

Output Metrics:

Key metrics like LCP, FID, CLS, TBT, etc., are displayed.

Recommendations (e.g., reduce unused JavaScript, optimize images) are highlighted.

4. User Interaction

The user enters the URL of the Drupal website.

The script fetches, saves, and parses the performance report.

Outputs are displayed in the terminal for immediate review and stored as a JSON file for detailed analysis.

Expected Outcomes

Automated Reporting:

Quick and consistent generation of performance reports.

Actionable Insights:

Highlight optimization opportunities with potential performance savings.

Comprehensive Analysis:

JSON reports can be used for deeper analysis or integrated into dashboards.
