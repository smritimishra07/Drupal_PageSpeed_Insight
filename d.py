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