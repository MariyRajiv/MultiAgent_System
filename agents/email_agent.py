from ollama import Client
import json
import re

client = Client(host='http://localhost:11434')

def email_agent(raw_input_text):
    """Optimized email processing with text truncation"""
    # Truncate long text to first 2000 characters
    truncated = raw_input_text[:2000] if isinstance(raw_input_text, str) else str(raw_input_text)[:2000]
    
    prompt = f"""
Extract structured data from the email below. Respond ONLY in JSON format.

Email:
\"\"\"{truncated}\"\"\"

JSON Format:
{{
  "sender": "email@example.com",
  "subject": "Email Subject",
  "intent": "Invoice|Complaint|RFQ|Other",
  "important_dates": ["YYYY-MM-DD"],
  "requested_action": "summary text"
}}
"""

    response = client.chat(
        model="mistral",
        messages=[{"role": "user", "content": prompt}]
    )

    extracted_info = response['message']['content']
    
    # Extract JSON from response
    json_match = re.search(r'\{.*\}', extracted_info, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group(0))
        except json.JSONDecodeError:
            pass
            
    # Fallback to empty result
    return {
        "sender": "unknown",
        "subject": "No subject",
        "intent": "Other",
        "important_dates": [],
        "requested_action": "Could not process email"
    }