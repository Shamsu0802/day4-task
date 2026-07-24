import os
import json
import pandas as pd
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Allowed values
ALLOWED_CATEGORIES = {
    "Billing",
    "Technical Issue",
    "Account Access",
    "Feature Request",
    "Complaint",
    "General Inquiry"
}

ALLOWED_URGENCY = {
    "Low",
    "Medium",
    "High",
    "Critical"
}

ALLOWED_SENTIMENT = {
    "Positive",
    "Neutral",
    "Negative"
}

# Read first ticket
df = pd.read_csv("support_tickets_raw.csv")
ticket = df.iloc[0]

ticket_id = ticket["ticket_id"]
ticket_text = ticket["ticket_text"]

prompt = f"""
You are a customer support ticket classifier.

Return ONLY valid JSON.

Schema:

{{
"ticket_id":"{ticket_id}",
"category":"Billing | Technical Issue | Account Access | Feature Request | Complaint | General Inquiry",
"urgency":"Low | Medium | High | Critical",
"sentiment":"Positive | Neutral | Negative"
}}

Ticket:

{ticket_text}
"""

response = client.models.generate_content(
    model="models/gemini-flash-latest",
    contents=prompt
)

response_text = response.text.strip()

print("LLM Response:")
print(response_text)

# ----------------------------
# Validation
# ----------------------------

try:
    result = json.loads(response_text)

    if result["category"] not in ALLOWED_CATEGORIES:
        raise ValueError("Invalid category")

    if result["urgency"] not in ALLOWED_URGENCY:
        raise ValueError("Invalid urgency")

    if result["sentiment"] not in ALLOWED_SENTIMENT:
        raise ValueError("Invalid sentiment")

    print("\n✅ Response is VALID")

except Exception as e:
    print("\n❌ Invalid response")
    print(e)##