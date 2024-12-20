import json
from typing import List, Dict, Any
from groq import Groq
from .config import GROQ_API_KEY

def get_ai_recommendations(issues: List[Dict[str, Any]]) -> None:
    """Gets AI recommendations for unknown issues using GROQ."""
    if not GROQ_API_KEY:
        print("Warning: GROQ_API_KEY not set. Skipping AI recommendations.")
        return
    
    try:
        groq = Groq(api_key=GROQ_API_KEY)
        
        # Create a simplified version of issues to reduce token count
        simplified_issues = [{
            "id": issue["id"],
            "title": issue["title"],
            "description": issue["description"]
        } for issue in issues]
        
        prompt = f"""Analyze these Drupal performance issues and provide specific solutions:
        {json.dumps(simplified_issues, indent=2)}
        
        For each issue, provide:
        1. A brief explanation
        2. One specific solution
        3. Implementation steps"""
        
        completion = groq.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a Drupal performance optimization expert. Provide concise, actionable solutions."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model="mixtral-8x7b-32768",
            temperature=0.3,
            max_tokens=1024  # Reduced token limit
        )
        
        print("\n=== AI Recommendations for Unknown Issues ===")
        print(completion.choices[0].message.content)
        
    except Exception as e:
        print(f"Error getting AI recommendations: {e}")