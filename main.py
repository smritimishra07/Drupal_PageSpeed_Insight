import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
API_KEY = os.getenv("API_KEY")

# Debug: Print the loaded API key
if not API_KEY:
    raise ValueError("API_KEY is not set. Please check your .env file.")
else:
    print(f"Loaded API_KEY: {API_KEY}")

def fetch_pagespeed_insights(url):
    """
    Fetches PageSpeed Insights data for the given URL and saves it as a JSON file.
    """
    # API endpoint
    api_url = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
    
    # Parameters
    params = {
        "url": url,
        "key": API_KEY,
        "strategy": "mobile"  # You can change this to "desktop"
    }
    
    try:
        # Make the API request
        response = requests.get(api_url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Get the JSON data
        data = response.json()
        
        # Save JSON data to a file
        output_file = "output/pagespeed_insights.json"
        with open(output_file, "w") as json_file:
            json.dump(data, json_file, indent=4)
        
        print(f"Data fetched successfully! JSON saved as {output_file}.")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")

if __name__ == "__main__":
    # Input the Drupal website URL
    website_url = input("Enter the Drupal website URL (including https:// or http://): ").strip()
    
    # Fetch the PageSpeed Insights data
    fetch_pagespeed_insights(website_url)
