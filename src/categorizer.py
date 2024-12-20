CATEGORIES = {
    "server_side": [
        "uses-text-compression",
        "server-response-time",
        "uses-long-cache-ttl"
    ],
    "client_side": [
        "uses-optimized-images",
        "uses-responsive-images",
        "efficient-animated-content"
    ],
    "configuration": [
        "redirects",
        "uses-http2",
        "no-document-write"
    ],
    "custom_code": [
        "render-blocking-resources",
        "unused-css-rules",
        "unused-javascript"
    ],
    "third_party": [
        "third-party-summary",
        "legacy-javascript"
    ]
}

def categorize_issue(audit_id: str) -> str:
    """Categorizes the issue based on the audit ID."""
    for category, issues in CATEGORIES.items():
        if audit_id in issues:
            return category.replace("_", " ").title()
    return "Uncategorized"