import json
import os
from openai import OpenAI
from prompts import LOGISTICS_SYSTEM_PROMPT
from config import OPENAI_API_KEY

# Initialize the client
# We use the key from your config file
client = OpenAI(api_key=OPENAI_API_KEY)

def extract_logistics_data(invoice_text: str) -> dict:
    """
    Sends invoice text to LLM and returns structured JSON data.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Fast and cheap model
            messages=[
                {"role": "system", "content": LOGISTICS_SYSTEM_PROMPT},
                {"role": "user", "content": invoice_text}
            ],
            temperature=0  # 0 means "be strict, don't be creative"
        )

        # Extract the content from the AI's answer
        ai_content = response.choices[0].message.content
        
        # Parse the text into a real Python dictionary
        return json.loads(ai_content)

    except Exception as e:
        print(f"Error calling AI: {e}")
        return {}