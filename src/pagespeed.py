import json
import os
import requests
from typing import List, Dict, Any
from .config import PAGESPEED_API_KEY
from .analyzer import analyze_issues

def fetch_pagespeed_insights(url: str) -> None:
    """Fetches PageSpeed Insights data for the given URL."""
    if not PAGESPEED_API_KEY:
        raise ValueError("PAGESPEED_API_KEY is not set in .env file")
    
    api_url = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
    params = {
        "url": url,
        "key": PAGESPEED_API_KEY,
        "strategy": "desktop"
    }
    
    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Save raw data
        os.makedirs("output", exist_ok=True)
        with open("output/pagespeed_insights.json", "w") as f:
            json.dump(data, f, indent=4)
        
        # Parse and analyze results
        results = []
        audits = data.get("lighthouseResult", {}).get("audits", {})
        
        for audit_id, audit_data in audits.items():
            metric_savings = audit_data.get("metricSavings", {})
            if any(value > 0 for value in metric_savings.values()):
                results.append({
                    "id": audit_data.get("id"),
                    "title": audit_data.get("title"),
                    "metric_savings": metric_savings,
                    "description": audit_data.get("description", "No description available."),
                    "details": audit_data.get("details", {}).get("items", [])
                })
        
        if results:
            analyze_issues(results)
        else:
            print("No performance issues found.")
            
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")