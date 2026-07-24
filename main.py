import os
import json
import pandas as pd
from dotenv import load_dotenv
from google import genai

# Load API Key
load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Read CSV
df = pd.read_csv("support_tickets_raw.csv")

# Read first ticket
ticket = df.iloc[0]

ticket_id = ticket["ticket_id"]
ticket_text = ticket["ticket_text"]

prompt = f"""
You are a customer support ticket classifier.

Classify the ticket into the following fields.

Category:
- Billing
- Technical Issue
- Account Access
- Feature Request
- Complaint
- General Inquiry

Urgency:
- Low
- Medium
- High
- Critical

Sentiment:
- Positive
- Neutral
- Negative

Return ONLY valid JSON.

Ticket ID: {ticket_id}

Ticket:
{ticket_text}
"""

response = client.models.generate_content(
    model="models/gemini-flash-latest",
    contents=prompt
)

print(response.text)