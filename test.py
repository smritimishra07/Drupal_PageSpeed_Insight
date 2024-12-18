import requests
import csv
import os
from dotenv import load_dotenv

# Load the API key from .env file
load_dotenv()
API_KEY = os.getenv("API_KEY")

if not API_KEY:
    print("Error: API_KEY not found in .env file.")
    exit()

# API endpoint
API_URL = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"

# Function to fetch PageSpeed Insights data
def fetch_pagespeed_data(url, strategy="desktop"):
    params = {
        "url": url,
        "key": API_KEY,
        "strategy": strategy
    }
    response = requests.get(API_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data for {url}: {response.status_code}")
        return None

# Function to parse required metrics from the API response
def parse_metrics(data):
    try:
        lighthouse = data["lighthouseResult"]
        metrics = {
            "URL": data["id"],
            "Performance": lighthouse["categories"]["performance"]["score"] * 100,
            "Accessibility": lighthouse["categories"]["accessibility"]["score"] * 100,
            "Best Practices": lighthouse["categories"]["best-practices"]["score"] * 100,
            "SEO": lighthouse["categories"]["seo"]["score"] * 100,
            "LCP": lighthouse["audits"]["largest-contentful-paint"]["numericValue"] / 1000,
            "FID": lighthouse["audits"].get("first-input-delay", {}).get("numericValue", "N/A"),
            "CLS": lighthouse["audits"]["cumulative-layout-shift"]["numericValue"],
            "Speed Index": lighthouse["audits"]["speed-index"]["numericValue"] / 1000,
            "TBT": lighthouse["audits"]["total-blocking-time"]["numericValue"] / 1000,
            "TTFB": lighthouse["audits"]["server-response-time"]["numericValue"] / 1000,
        }
        return metrics
    except KeyError as e:
        print(f"Error parsing metrics: {e}")
        return {}

# Function to generate report for user-provided URLs
def generate_report():
    print("Enter website URLs (comma-separated) or type 'exit' to quit:")
    user_input = input()
    
    if user_input.lower() == "exit":
        print("Exiting...")
        return

    # Split URLs and strip whitespace
    websites = [url.strip() for url in user_input.split(",")]

    results = []
    for url in websites:
        print(f"Fetching data for: {url}")
        data = fetch_pagespeed_data(url)
        if data:
            metrics = parse_metrics(data)
            results.append(metrics)
    
    if results:
        # Save results to a CSV file
        with open("pagespeed_report.csv", "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=results[0].keys())
            writer.writeheader()
            writer.writerows(results)
        
        print("Report saved to 'pagespeed_report.csv'.")
    else:
        print("No data fetched. Please check the URLs and try again.")

# Run the script
generate_report()
