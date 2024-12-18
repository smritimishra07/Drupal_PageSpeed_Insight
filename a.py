from google.colab import files
import json

# Step 1: Upload the JSON file
uploaded = files.upload()

def parse_lighthouse_json(filename):
    """
    Parses the Lighthouse JSON file to find audits where metricSavings.LCP > 0.

    Args:
        file_path (str): The path to the JSON file.

    Returns:
        list: A list of audit items where metricSavings.LCP > 0.
    """
    with open(filename, 'r') as file:
            data = json.load(file)

    results = []
    # Navigate to the audits section
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
            results.append({
                "id": audit_data.get("id"),
                "title": audit_data.get("title"),
                "metric_savings":audit_data.get("metricSavings", {}),
                "details": audit_data.get("details", {}).get("items", [])
            })

    return results


filename = list(uploaded.keys())[0]
result = parse_lighthouse_json(filename)
for entry in result:
    print(entry)