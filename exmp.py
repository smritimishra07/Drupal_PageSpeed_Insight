# import json
# import os
# from typing import List, Dict, Any
# import requests
# from groq import Groq
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()

# # Known solutions database
# DRUPAL_SOLUTIONS = {
#     "server-response-time": {
#         "solutions": [
#             {
#                 "title": "Enable Drupal Cache",
#                 "code": """
# # In settings.php
# $settings['cache']['bins']['render'] = 'cache.backend.memory';
# $settings['cache']['bins']['dynamic_page_cache'] = 'cache.backend.memory';
# $settings['cache']['bins']['page'] = 'cache.backend.memory';
#                 """
#             },
#             {
#                 "title": "Enable Redis Cache",
#                 "code": """
# # In settings.php
# $settings['redis.connection']['interface'] = 'PhpRedis';
# $settings['redis.connection']['host'] = '127.0.0.1';
# $settings['cache']['default'] = 'cache.backend.redis';
#                 """
#             }
#         ]
#     },
#     "uses-text-compression": {
#         "solutions": [
#             {
#                 "title": "Enable Gzip Compression",
#                 "code": """
# # In .htaccess
# <IfModule mod_deflate.c>
#   AddOutputFilterByType DEFLATE text/html text/plain text/xml text/css text/javascript application/javascript application/x-javascript application/json
# </IfModule>
#                 """
#             }
#         ]
#     },
#     "uses-long-cache-ttl": {
#         "solutions": [
#             {
#                 "title": "Configure Browser Caching",
#                 "code": """
# # In .htaccess
# <IfModule mod_expires.c>
#   ExpiresActive On
#   ExpiresByType image/jpg "access plus 1 year"
#   ExpiresByType image/jpeg "access plus 1 year"
#   ExpiresByType image/png "access plus 1 year"
#   ExpiresByType image/gif "access plus 1 year"
#   ExpiresByType text/css "access plus 1 month"
#   ExpiresByType application/javascript "access plus 1 month"
# </IfModule>
#                 """
#             }
#         ]
#     }
# }

# def categorize_issue(audit_id: str) -> str:
#     """Categorizes the issue based on the audit ID."""
#     categories = {
#         "server_side": [
#             "uses-text-compression",
#             "server-response-time",
#             "uses-long-cache-ttl"
#         ],
#         "client_side": [
#             "uses-optimized-images",
#             "uses-responsive-images",
#             "efficient-animated-content"
#         ],
#         "configuration": [
#             "redirects",
#             "uses-http2",
#             "no-document-write"
#         ],
#         "custom_code": [
#             "render-blocking-resources",
#             "unused-css-rules",
#             "unused-javascript"
#         ],
#         "third_party": [
#             "third-party-summary",
#             "legacy-javascript"
#         ]
#     }
    
#     for category, issues in categories.items():
#         if audit_id in issues:
#             return category.replace("_", " ").title()
    
#     return "Uncategorized"

# def get_ai_recommendations(issues: List[Dict[str, Any]]) -> None:
#     """Gets AI recommendations for unknown issues using GROQ."""
#     api_key = os.getenv("GROQ_API_KEY")
    
#     if not api_key:
#         print("Warning: GROQ_API_KEY not set. Skipping AI recommendations.")
#         return
    
#     try:
#         groq = Groq(api_key=api_key)
        
#         prompt = f"""As a Drupal expert, analyze these performance issues and provide specific solutions:
#         {json.dumps(issues, indent=2)}
        
#         Provide detailed, practical solutions that can be implemented in Drupal."""
        
#         completion = groq.chat.completions.create(
#             messages=[
#                 {
#                     "role": "system",
#                     "content": "You are a Drupal performance optimization expert. Provide specific, actionable solutions for performance issues."
#                 },
#                 {
#                     "role": "user",
#                     "content": prompt
#                 }
#             ],
#             model="mixtral-8x7b-32768",
#             temperature=0.3,
#             max_tokens=2048
#         )
        
#         print("\n=== AI Recommendations for Unknown Issues ===")
#         print(completion.choices[0].message.content)
        
#     except Exception as e:
#         print(f"Error getting AI recommendations: {e}")

# def print_known_solutions(issues: List[Dict[str, Any]]) -> None:
#     """Prints solutions for known issues."""
#     print("\n=== Solutions for Known Issues ===")
#     for issue in issues:
#         print(f"\nIssue: {issue['title']}")
#         print(f"Category: {issue['category']}")
#         print("Solutions:")
        
#         for i, solution in enumerate(issue["solutions"], 1):
#             print(f"\n{i}. {solution['title']}")
#             print("Implementation:")
#             print(solution["code"].strip())

# def analyze_issues(results: List[Dict[str, Any]]) -> None:
#     """Analyzes and provides solutions for Drupal performance issues."""
#     known_issues = []
#     unknown_issues = []
    
#     # Categorize issues
#     for result in results:
#         result["category"] = categorize_issue(result["id"])
#         if result["id"] in DRUPAL_SOLUTIONS:
#             known_issues.append({
#                 **result,
#                 "solutions": DRUPAL_SOLUTIONS[result["id"]]["solutions"]
#             })
#         else:
#             unknown_issues.append(result)
    
#     # Handle known issues
#     if known_issues:
#         print_known_solutions(known_issues)
    
#     # Handle unknown issues
#     if unknown_issues:
#         get_ai_recommendations(unknown_issues)

# def fetch_pagespeed_insights(url: str) -> None:
#     """Fetches PageSpeed Insights data for the given URL."""
#     api_key = os.getenv("PAGESPEED_API_KEY")
    
#     if not api_key:
#         raise ValueError("PAGESPEED_API_KEY is not set in .env file")
    
#     api_url = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
#     params = {
#         "url": url,
#         "key": api_key,
#         "strategy": "desktop"
#     }
    
#     try:
#         response = requests.get(api_url, params=params)
#         response.raise_for_status()
#         data = response.json()
        
#         # Save raw data
#         os.makedirs("output", exist_ok=True)
#         with open("output/pagespeed_insights.json", "w") as f:
#             json.dump(data, f, indent=4)
        
#         # Parse and analyze results
#         results = []
#         audits = data.get("lighthouseResult", {}).get("audits", {})
        
#         for audit_id, audit_data in audits.items():
#             metric_savings = audit_data.get("metricSavings", {})
#             if any(value > 0 for value in metric_savings.values()):
#                 results.append({
#                     "id": audit_data.get("id"),
#                     "title": audit_data.get("title"),
#                     "metric_savings": metric_savings,
#                     "description": audit_data.get("description", "No description available."),
#                     "details": audit_data.get("details", {}).get("items", [])
#                 })
        
#         if results:
#             analyze_issues(results)
#         else:
#             print("No performance issues found.")
            
#     except requests.exceptions.RequestException as e:
#         print(f"Error fetching data: {e}")

# def main():
#     """Main entry point for the Drupal performance analyzer."""
#     try:
#         website_url = input("Enter the Drupal website URL (including https:// or http://): ").strip()
#         fetch_pagespeed_insights(website_url)
#     except KeyboardInterrupt:
#         print("\nAnalysis cancelled by user.")
#     except Exception as e:
#         print(f"An error occurred: {e}")

# if __name__ == "__main__":
#     main()


from src.pagespeed import fetch_pagespeed_insights

def main():
    """Main entry point for the Drupal performance analyzer."""
    try:
        website_url = input("Enter the Drupal website URL (including https:// or http://): ").strip()
        fetch_pagespeed_insights(website_url)
    except KeyboardInterrupt:
        print("\nAnalysis cancelled by user.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()