from ollama import Client
import json
import re

client = Client()

def classify_format_and_intent(raw_input_text):
    """Optimized classification with text truncation"""
    # Truncate long text to first 1000 characters
    truncated = raw_input_text[:1000] if isinstance(raw_input_text, str) else str(raw_input_text)[:1000]
    
    prompt = f"""
Classify the following input by format and intent. Respond ONLY in JSON format.
Input:
\"\"\"{truncated}\"\"\"

JSON Format:
{{
  "format": "PDF|JSON|Email",
  "intent": "Invoice|RFQ|Complaint|Regulation|Other"
}}
"""

    response = client.chat(
        model="mistral",
        messages=[{"role": "user", "content": prompt}]
    )

    classification_text = response['message']['content']
    
    # Extract JSON from response
    json_match = re.search(r'\{.*\}', classification_text, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group(0))
        except json.JSONDecodeError:
            pass
            
    # Fallback to simple detection
    format = "PDF" if ".pdf" in truncated.lower() else "JSON" if "{" in truncated else "Email"
    intent = "Other"
    return {"format": format, "intent": intent}