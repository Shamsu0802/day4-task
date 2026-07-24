import os
import json
import time
import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI

# ----------------------------
# Load API Key
# ----------------------------
load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

# ----------------------------
# Load Raw Dataset
# ----------------------------
df = pd.read_csv("support_tickets_raw.csv")

# ----------------------------
# Allowed Labels
# ----------------------------
valid_categories = [
    "Billing",
    "Technical Issue",
    "Account Access",
    "Feature Request",
    "Complaint",
    "General Inquiry"
]

valid_urgencies = [
    "Low",
    "Medium",
    "High",
    "Critical"
]

valid_sentiments = [
    "Positive",
    "Neutral",
    "Negative"
]

# ----------------------------
# Zero-Shot Prompt
# ----------------------------
def get_zero_shot_prompt(ticket_id, ticket_text):
    return f"""
You are a customer support ticket classifier.

Classify the following customer support ticket.

Rules:
- Choose EXACTLY ONE category.
- Return ONLY valid JSON.
- Do not include explanations.
- Do not use markdown.

Schema:

{{
    "ticket_id": "{ticket_id}",
    "category": "Billing | Technical Issue | Account Access | Feature Request | Complaint | General Inquiry",
    "urgency": "Low | Medium | High | Critical",
    "sentiment": "Positive | Neutral | Negative"
}}

Ticket:
{ticket_text}
"""

# ----------------------------
# Store Predictions
# ----------------------------
predictions = []

print(f"Classifying {len(df)} tickets...\n")

# ----------------------------
# Process Each Ticket
# ----------------------------
for _, ticket in df.iterrows():

    ticket_id = ticket["ticket_id"]
    ticket_text = ticket["ticket_text"]

    prompt = get_zero_shot_prompt(ticket_id, ticket_text)

    response = None

    # Retry API call up to 3 times
    for attempt in range(3):
        try:
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0
            )
            break

        except Exception as e:
            print(f"Retry {attempt+1}/3 for {ticket_id}")
            print(e)

            if attempt < 2:
                time.sleep(3)

    if response is None:
        print(f"Skipping {ticket_id}")
        continue

    try:

        response_text = response.choices[0].message.content.strip()

        response_text = response_text.replace("```json", "")
        response_text = response_text.replace("```", "")
        response_text = response_text.strip()

        result = json.loads(response_text)

        if result["category"] not in valid_categories:
            print(f"Invalid category for {ticket_id}")
            continue

        if result["urgency"] not in valid_urgencies:
            print(f"Invalid urgency for {ticket_id}")
            continue

        if result["sentiment"] not in valid_sentiments:
            print(f"Invalid sentiment for {ticket_id}")
            continue

        predictions.append({
            "ticket_id": ticket_id,
            "ticket_text": ticket_text,
            "category": result["category"],
            "urgency": result["urgency"],
            "sentiment": result["sentiment"]
        })

        print(f"✅ {ticket_id} classified")

    except Exception as e:
        print(f"Error parsing {ticket_id}")
        print(e)

    time.sleep(1)

# ----------------------------
# Save Predictions
# ----------------------------
output_df = pd.DataFrame(predictions)

output_df.to_csv("classified_tickets.csv", index=False)

print("\n==============================")
print("Classification Complete")
print("==============================")
print(f"Total Tickets Classified: {len(output_df)}")
print("Results saved to classified_tickets.csv")