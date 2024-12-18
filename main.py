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
    """
    print("\nParsing report for metrics with savings > 0...\n")
    
    results = []
    audits = data.get("lighthouseResult", {}).get("audits", {})

    for audit_id, audit_data in audits.items():
        # Check if 'metricSavings' exists and contains an 'LCP' key
        metric_savings = audit_data.get("metricSavings", {})
        lcp_value = metric_savings.get("LCP", 0)
        fcp_value = metric_savings.get("FCP", 0)
        tbt_value = metric_savings.get("TBT", 0)
        cls_value = metric_savings.get("CLS", 0)

        # Add to results if LCP > 0
        if any(value > 0 for value in [lcp_value, fcp_value, tbt_value, cls_value]):
            #print(audit_data.get("id"))
            results.append({
                "id": audit_data.get("id"),
                "title": audit_data.get("title"),
                "metric_savings":audit_data.get("metricSavings", {}),
                "details": audit_data.get("details", {}).get("items", [])
            })
    
    print(results)
if __name__ == "__main__":
    website_url = input("Enter the Drupal website URL (including https:// or http://): ").strip()
    fetch_pagespeed_insights(website_url)
