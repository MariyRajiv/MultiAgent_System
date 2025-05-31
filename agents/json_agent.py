import json

def json_agent(json_payload):
    """Process JSON payload with error handling"""
    target_schema = {
        "invoice_id": None,
        "customer_name": None,
        "amount": None,
        "due_date": None,
    }
    anomalies = []
    
    try:
        # Handle string input
        if isinstance(json_payload, str):
            payload = json.loads(json_payload)
        else:
            payload = json_payload
            
        # Extract values
        for key in target_schema:
            if key in payload:
                target_schema[key] = payload[key]
            else:
                anomalies.append(f"Missing field: {key}")
                
        return target_schema, anomalies
    except json.JSONDecodeError:
        return {}, ["Invalid JSON format"]