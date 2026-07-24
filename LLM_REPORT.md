# LLM Report

## Prompt Strategy 1 – Zero-Shot Prompt

### Prompt

```text
You are a customer support ticket classifier.

Return ONLY valid JSON.

Choose EXACTLY ONE category.

Schema:

{
    "ticket_id": "<ticket_id>",
    "category": "Billing | Technical Issue | Account Access | Feature Request | Complaint | General Inquiry",
    "urgency": "Low | Medium | High | Critical",
    "sentiment": "Positive | Neutral | Negative"
}

Ticket:
<ticket_text>
```

---

## Prompt Strategy 2 – Few-Shot Prompt

### Prompt

```text
You are a customer support ticket classifier.

Here are some examples.

Example 1

Ticket:
I was charged twice for my subscription.

Output:
{
    "ticket_id":"EX001",
    "category":"Billing",
    "urgency":"High",
    "sentiment":"Negative"
}

Example 2

Ticket:
I forgot my password and cannot log in.

Output:
{
    "ticket_id":"EX002",
    "category":"Account Access",
    "urgency":"Medium",
    "sentiment":"Negative"
}

Example 3

Ticket:
Please add dark mode to the application.

Output:
{
    "ticket_id":"EX003",
    "category":"Feature Request",
    "urgency":"Low",
    "sentiment":"Positive"
}

Now classify this ticket.

Return ONLY JSON.

Schema:

{
    "ticket_id":"<ticket_id>",
    "category":"Billing | Technical Issue | Account Access | Feature Request | Complaint | General Inquiry",
    "urgency":"Low | Medium | High | Critical",
    "sentiment":"Positive | Neutral | Negative"
}

Ticket:
<ticket_text>
```

---

## Accuracy Comparison (14 Validation Tickets)

| Strategy | Category | Urgency | Sentiment |
|----------|---------:|---------:|----------:|
| Zero-Shot | 78.57% | 71.43% | 92.86% |
| Few-Shot | 78.57% | 78.57% | 78.57% |

---

## Selected Strategy

I selected **Zero-Shot Prompting** because it achieved the better overall performance. Although the Few-Shot prompt slightly improved urgency prediction, the Zero-Shot prompt produced much better sentiment accuracy and gave the highest average accuracy across all three fields.

---

## Validation Logic

After receiving the model response, I validated it before using the output.

The validation checks were:

- The response must be valid JSON.
- The category must be one of the allowed categories.
- The urgency must be one of the allowed urgency levels.
- The sentiment must be one of the allowed sentiment values.

If the response failed any of these checks, it was treated as an invalid response and skipped.

---

## Observations from the 45 Tickets

- Most tickets were classified correctly and returned valid JSON.
- Some tickets contained information that could fit more than one category, making them slightly ambiguous.
- The model consistently followed the required JSON format after prompt refinement.
- Overall, the generated classifications were consistent across the dataset.