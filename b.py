import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
API_KEY = os.getenv("API_KEY")

if not API_KEY:
    raise ValueError("API_KEY is not set. Please check your .env file.")
else:
    print(f"Loaded API_KEY: {API_KEY}")

def fetch_pagespeed_insights(url):
    """
    Fetches PageSpeed Insights data for the given URL and saves it as a JSON file.
    """
    api_url = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
    params = {
        "url": url,
        "key": API_KEY,
        "strategy": "desktop"  # You can change this to "desktop"
    }
    
    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Ensure the output directory exists
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)
        
        # Save raw JSON data to a file
        output_file = os.path.join(output_dir, "pagespeed_insights.json")
        with open(output_file, "w") as json_file:
            json.dump(data, json_file, indent=4)
        
        print(f"Data fetched successfully! JSON saved as {output_file}.")
        
        # Parse the JSON for metrics with savings > 0
        parse_report(data)
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")

def parse_report(data):
    """
    Parses the PageSpeed Insights report and displays IDs with saving-matrix > 0 for various parameters.
    Categorizes issues into predefined criteria.
    """
    print("\nParsing report for metrics with savings > 0...\n")
    
    results = []
    audits = data.get("lighthouseResult", {}).get("audits", {})

    for audit_id, audit_data in audits.items():
        # Check if 'metricSavings' exists and contains any savings
        metric_savings = audit_data.get("metricSavings", {})
        if metric_savings and any(value > 0 for value in metric_savings.values()):
            # Categorize issue
            category = categorize_issue(audit_id)
            results.append({
                "id": audit_data.get("id"),
                "title": audit_data.get("title"),
                "category": category,
                "metric_savings": metric_savings,
                "details": audit_data.get("details", {}).get("items", [])
            })
    
    if results:
        for result in results:
            print(f"Issue ID: {result['id']}")
            print(f"Title: {result['title']}")
            print(f"Category: {result['category']}")
            print(f"Metric Savings: {result['metric_savings']}")
            print("-" * 50)
    else:
        print("No audits found with savings greater than zero.")

def categorize_issue(audit_id):
    """
    Categorizes the issue based on the audit ID.
    """
    server_side_issues = [
        "uses-text-compression", "server-response-time", "uses-long-cache-ttl"
    ]
    client_side_issues = [
        "uses-optimized-images", "uses-responsive-images", "efficient-animated-content"
    ]
    configuration_issues = [
        "redirects", "uses-http2", "no-document-write"
    ]
    custom_code_issues = [
        "render-blocking-resources", "unused-css-rules", "unused-javascript"
    ]
    third_party_dependencies_issues = [
        "third-party-summary", "legacy-javascript"
    ]

    if audit_id in server_side_issues:
        return "Server-side"
    elif audit_id in client_side_issues:
        return "Client-side"
    elif audit_id in configuration_issues:
        return "Configuration"
    elif audit_id in custom_code_issues:
        return "Custom Code"
    elif audit_id in third_party_dependencies_issues:
        return "Third-party Dependencies"
    else:
        return "Uncategorized"

if __name__ == "__main__":
    website_url = input("Enter the Drupal website URL (including https:// or http://): ").strip()
    fetch_pagespeed_insights(website_url)