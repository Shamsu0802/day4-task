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
# Load Validation Dataset
# ----------------------------
df = pd.read_csv("support_tickets_validation_sample.csv")

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
# Few-Shot Prompt
# ----------------------------
def get_few_shot_prompt(ticket_id, ticket_text):
    return f"""
You are a customer support ticket classifier.

Learn from the examples below and classify the given ticket.

Example 1

Ticket:
I was charged twice for my subscription this month.

Output:
{{
    "ticket_id": "EX001",
    "category": "Billing",
    "urgency": "High",
    "sentiment": "Negative"
}}

Example 2

Ticket:
I forgot my password and cannot log into my account.

Output:
{{
    "ticket_id": "EX002",
    "category": "Account Access",
    "urgency": "Medium",
    "sentiment": "Negative"
}}

Example 3

Ticket:
The mobile app crashes every time I open it.

Output:
{{
    "ticket_id": "EX003",
    "category": "Technical Issue",
    "urgency": "High",
    "sentiment": "Negative"
}}

Example 4

Ticket:
Please add dark mode to the application.

Output:
{{
    "ticket_id": "EX004",
    "category": "Feature Request",
    "urgency": "Low",
    "sentiment": "Positive"
}}

Now classify this ticket.

Rules:
- Return ONLY valid JSON.
- Choose EXACTLY ONE category.
- Do not explain your answer.
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
# Accuracy Counters
# ----------------------------
category_correct = 0
urgency_correct = 0
sentiment_correct = 0

total = len(df)

print(f"Evaluating {total} tickets using Few-Shot Prompting...\n")

# ----------------------------
# Process Each Ticket
# ----------------------------
for _, ticket in df.iterrows():

    ticket_id = ticket["ticket_id"]
    ticket_text = ticket["ticket_text"]

    prompt = get_few_shot_prompt(ticket_id, ticket_text)

    response = None

    # Retry up to 3 times
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
            print(f"Retry {attempt + 1}/3 for {ticket_id}")
            print("Error:", e)

            if attempt < 2:
                time.sleep(3)

    if response is None:
        print(f"❌ Skipping {ticket_id}\n")
        continue

    try:

        response_text = response.choices[0].message.content.strip()

        # Remove markdown if present
        response_text = response_text.replace("```json", "")
        response_text = response_text.replace("```", "")
        response_text = response_text.strip()

        print(f"\n{ticket_id}")
        print(response_text)

        result = json.loads(response_text)

        # Validate labels
        if result["category"] not in valid_categories:
            print("❌ Invalid category")
            continue

        if result["urgency"] not in valid_urgencies:
            print("❌ Invalid urgency")
            continue

        if result["sentiment"] not in valid_sentiments:
            print("❌ Invalid sentiment")
            continue

        print("✅ Valid Response")

        # Compare with ground truth
        if result["category"] == ticket["category"]:
            category_correct += 1

        if result["urgency"] == ticket["urgency"]:
            urgency_correct += 1

        if result["sentiment"] == ticket["sentiment"]:
            sentiment_correct += 1

    except Exception as e:
        print(f"❌ Error parsing {ticket_id}")
        print(e)

    time.sleep(1)

# ----------------------------
# Final Results
# ----------------------------
print("\n==============================")
print("Few-Shot Evaluation Results")
print("==============================")

print(
    f"Category Accuracy : {category_correct}/{total} ({category_correct/total*100:.2f}%)"
)
print(
    f"Urgency Accuracy  : {urgency_correct}/{total} ({urgency_correct/total*100:.2f}%)"
)
print(
    f"Sentiment Accuracy: {sentiment_correct}/{total} ({sentiment_correct/total*100:.2f}%)"
)