import requests
import json
import re
from config import GEMINI_API_KEY
from prompts import LOGISTICS_SYSTEM_PROMPT

def extract_logistics_data(invoice_text: str) -> dict:
    # We use the generic alias "gemini-flash-latest" found in your list.
    # This points to the stable version (1.5) which usually has an open Free Tier.
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={GEMINI_API_KEY}"
    
    headers = {"Content-Type": "application/json"}
    
    final_prompt = (
        f"{LOGISTICS_SYSTEM_PROMPT}\n\n"
        "INSTRUCTIONS: Analyze the invoice below. "
        "Return ONLY valid JSON. Do not write 'Here is the JSON' or use Markdown.\n\n"
        f"INVOICE TEXT:\n{invoice_text}"
    )
    
    payload = {
        "contents": [{
            "parts": [{"text": final_prompt}]
        }]
    }

    print(f"🔌 Connecting to Google AI (Stable Flash)...")
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        
        # If blocked, print the raw error
        if response.status_code != 200:
            print(f"❌ GOOGLE REFUSED: {response.status_code}")
            print(response.text)
            return {}

        # If success, process the Real Data
        data = response.json()
        ai_text = data["candidates"][0]["content"]["parts"][0]["text"]
        
        # Clean the text
        clean_text = re.sub(r"```json|```", "", ai_text).strip()
        
        print("✅ Real AI Success!")
        return json.loads(clean_text)

    except Exception as e:
        print(f"❌ Connection Error: {e}")
        return {}