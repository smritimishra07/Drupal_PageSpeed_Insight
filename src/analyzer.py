from typing import List, Dict, Any
from .categorizer import categorize_issue
from .solutions_db import DRUPAL_SOLUTIONS
from .ai_advisor import get_ai_recommendations

def print_known_solutions(issues: List[Dict[str, Any]]) -> None:
    """Prints solutions for known issues."""
    print("\n=== Solutions for Known Issues ===")
    for issue in issues:
        print(f"\nIssue: {issue['title']}")
        print(f"Category: {issue['category']}")
        print("Solutions:")
        
        for i, solution in enumerate(issue["solutions"], 1):
            print(f"\n{i}. {solution['title']}")
            print("Implementation:")
            print(solution["code"].strip())

def analyze_issues(results: List[Dict[str, Any]]) -> None:
    """Analyzes and provides solutions for Drupal performance issues."""
    known_issues = []
    unknown_issues = []
    
    for result in results:
        result["category"] = categorize_issue(result["id"])
        if result["id"] in DRUPAL_SOLUTIONS:
            known_issues.append({
                **result,
                "solutions": DRUPAL_SOLUTIONS[result["id"]]["solutions"]
            })
        else:
            unknown_issues.append(result)
    
    if known_issues:
        print_known_solutions(known_issues)
    
    if unknown_issues:
        get_ai_recommendations(unknown_issues)