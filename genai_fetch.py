import json
import os
import re
import google.genai as genai
import datetime

today = datetime.date.today().strftime("%B %d, %Y")
# ✅ Load Gemini API key from env
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
gemini_client = genai.Client(api_key=GEMINI_API_KEY)

def extract_json(text):
    """
    Extracts the first valid JSON array from the Gemini output.
    Handles cases with triple backticks, extra text, or markdown formatting.
    """
    # Try to match a JSON array inside ```json ... ```
    match = re.search(r"```json\s*(\[.*?\])\s*```", text, re.DOTALL)
    if not match:
        # Fallback: match any JSON array in the text
        match = re.search(r"(\[.*\])", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError as e:
            print("⚠️ JSONDecodeError while parsing:", e)
            return []
    return []

def get_tournaments(sport):
    prompt = f"""Today's date is {today}
    Give me a list of real upcoming {sport} tournaments in India,check if they are in upcoming future(post august 2025), not before that, across any level (local, state, national, etc). 
    For each event, provide:
    - Tournament Name
    - Level
    - Start Date
    - End Date
    - Official URL
    - Streaming link (if any)
    - Image link (if any)
    - Summary (max 50 words)

    Return in JSON format.
    """
    
    try:
        resp = gemini_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        
        # Log raw Gemini response for debugging
        print("\n=== RAW GEMINI RESPONSE ===")
        print(resp)
        print("===========================\n")
        
        # Gemini SDK stores text in a nested structure
        try:
            raw_text = resp.candidates[0].content.parts[0].text
        except Exception:
            raw_text = getattr(resp, "text", "")
        
        print("\n=== RAW TEXT EXTRACTED ===")
        print(raw_text)
        print("==========================\n")

        # Extract clean JSON
        data = extract_json(raw_text)
        return data

    except Exception as e:
        print("❌ Gemini API Error:", e)
        return []
