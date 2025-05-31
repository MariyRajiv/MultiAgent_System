from orchestrator import orchestrator
import os
import json

def main():
    print("🤖 Multi-Agent Document Processing System")
    print("----------------------------------------")
    print("Supported input types: PDF, JSON, Email")
    print("Type 'exit' to quit\n")
    
    while True:
        user_input = input("\nEnter document path, JSON string, or email text: ").strip()
        
        if user_input.lower() in ['exit', 'quit']:
            print("👋 Exiting system...")
            break
            
        # Detect input type
        input_type = None
        if user_input.endswith(".pdf"):
            input_type = "pdf"
            if not os.path.exists(user_input):
                print(f"❌ File not found: {user_input}")
                continue
        elif user_input.startswith(('{', '[')) or '"' in user_input[:10]:
            input_type = "json"
        
        try:
            result = orchestrator(user_input, input_type)
            print("\n📦 Processing Result:")
            print(json.dumps(result, indent=2))
        except Exception as e:
            print(f"⚠️ Error processing document: {str(e)}")
        
        print("\n" + "-"*50)

if __name__ == "__main__":
    main()

