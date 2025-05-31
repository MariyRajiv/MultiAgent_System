import uuid
import re
import time
from datetime import datetime

from shared_memory import SharedMemory
from agents.classifier_agent import classify_format_and_intent
from agents.email_agent import email_agent
from agents.json_agent import json_agent
from agents.pdf_utils import extract_text_from_pdf

def orchestrator(input_data, input_type=None, conversation_id=None):
    start_time = time.time()
    
    if conversation_id is None:
        conversation_id = str(uuid.uuid4())

    # Step 1: Extract raw text if PDF
    if input_type == "pdf" or (not input_type and isinstance(input_data, str) and input_data.endswith(".pdf")):
        print("⏳ Extracting text from PDF...")
        raw_text = extract_text_from_pdf(input_data)
        print(f"✅ PDF text extracted ({len(raw_text)} characters)")
    elif input_type == "json" or (not input_type and (isinstance(input_data, dict) or (isinstance(input_data, str) and re.match(r'^\s*\{', input_data)))):
        raw_text = input_data
    else:
        raw_text = input_data  # email or plain text

    # Step 2: Classify format + intent
    print("🔍 Classifying document...")
    classification = classify_format_and_intent(raw_text[:5000])  # Only use first 5000 chars for classification
    print(f"📋 Classification: {classification['format']} | {classification['intent']}")

    # Log classification
    shared_memory = SharedMemory()
    shared_memory.log_entry(conversation_id, {
        "timestamp": datetime.now().isoformat(),
        "step": "classification",
        "format": classification.get("format"),
        "intent": classification.get("intent"),
        "raw_input_snippet": str(raw_text)[:200]
    })

    # Step 3: Route based on classification
    fmt = classification.get("format", "").lower()
    result = None

    if fmt == "json":
        print("🔄 Processing JSON...")
        result, anomalies = json_agent(raw_text)
        shared_memory.log_entry(conversation_id, {
            "timestamp": datetime.now().isoformat(),
            "step": "json_agent",
            "result": result,
            "anomalies": anomalies
        })
    else:  # email or pdf
        print("📧 Processing email content...")
        result = email_agent(raw_text[:8000])  # Only use first 8000 chars for processing
        shared_memory.log_entry(conversation_id, {
            "timestamp": datetime.now().isoformat(),
            "step": "email_agent" if fmt == "email" else "pdf_agent",
            "extracted": result
        })
    
    elapsed = time.time() - start_time
    print(f"⏱️ Processing completed in {elapsed:.2f} seconds")
    return result