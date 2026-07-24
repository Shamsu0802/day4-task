# Day 4 Task - LLM Powered Ticket Classification (Structured Output)

## What this is

`support_tickets_raw.csv` contains **45 real-looking customer support
tickets** (just `ticket_id` and `ticket_text`, no labels). Your job is to
build a pipeline that calls an LLM to classify each ticket into structured
fields — this is the same triage step your final project will
likely need, so treat this as building a real, reusable component.

`support_tickets_validation_sample.csv` has **14 of those same tickets with
gold labels** already filled in, so you can measure your own accuracy while
you iterate. The other 31 are unlabeled you'll run your final pipeline
against all 45, but you won't know if you got the unlabeled ones right until
the afternoon review.

## The schema

For each ticket, extract:

```json
{
  "ticket_id": "TCK001",
  "category": "Billing | Technical Issue | Account Access | Feature Request | Complaint | General Inquiry",
  "urgency": "Low | Medium | High | Critical",
  "sentiment": "Positive | Neutral | Negative"
}
```

Every output must use **exactly one** of the listed values per field
no free text, no invented categories, no explanations mixed into the JSON.

## What to do

### 1. Get an LLM call working with structured output
Use whichever API you have access to (OpenAI, Anthropic, Groq, Gemini, etc).
Get a single ticket classified correctly and returned as valid JSON before
scaling up to all 45.

### 2. Design and compare two different prompt strategies
Try two meaningfully different approaches for example:
- Zero shot instruction vs. few shot with 2 to 3 worked examples
- Asking for the answer directly vs. asking the model to briefly reason
  first, then output the final JSON
- A single combined prompt vs. one prompt per field

Run both strategies across the 14 labeled tickets and compare accuracy
per field (category / urgency / sentiment). Pick a winner and explain why.

### 3. Validate every response before trusting it
Don't assume the model will always behave. Before accepting a response:
- Check it's valid JSON
- Check every field value is actually one of the allowed options
- Decide what your code does if the model returns something invalid,
  off schema, or refuses to answer the actual task

### 4. Run your winning strategy on all 45 tickets
Save the full output as `ticket_classifications.json` (or `.csv` your
choice), one row/object per ticket.

### 5. Write a short report (`LLM_REPORT.md`)
Cover: the two prompts you tried (include the actual prompt text), your
accuracy comparison on the 14 labeled tickets, which one you chose and why,
what your validation logic does with a bad response, and anything unusual
you noticed in any of the 45 tickets while reviewing outputs.

### 6. Deliverables
- Your pipeline code
- Both prompt versions you tested
- `ticket_classifications.json` (all 45 tickets)
- `LLM_REPORT.md`
- Incremental commits, not one dump at the end


## What we're looking for

- Whether you can actually get structured, schema valid output from an LLM,
  not just readable prose
- Whether your two prompt strategies are genuinely different approaches,
  not trivial rewordings
- Whether you validate model output rather than trusting it blindly
- Whether your accuracy comparison is real (measured against the 14 labeled
  tickets) rather than a guess


## This afternoon

Live walkthrough: you'll show both prompts your accuracy comparison, and
your validation logic. Expect a live request to run your pipeline against a
new ticket I give you on the spot and questions about anything unusual your
pipeline may have produced on tickets outside the labeled sample.
