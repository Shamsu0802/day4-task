# compare_results.py

# ----------------------------
# Zero-Shot Results
# ----------------------------
zero_category = 78.57
zero_urgency = 71.43
zero_sentiment = 92.86

# ----------------------------
# Few-Shot Results
# ----------------------------
few_category = 78.57
few_urgency = 78.57
few_sentiment = 78.57

print("=" * 60)
print("      ZERO-SHOT vs FEW-SHOT PROMPT COMPARISON")
print("=" * 60)

print(f"{'Metric':<15}{'Zero-Shot':<15}{'Few-Shot':<15}{'Better'}")
print("-" * 60)

# Category
better = "Tie"
if zero_category > few_category:
    better = "Zero-Shot"
elif few_category > zero_category:
    better = "Few-Shot"

print(f"{'Category':<15}{zero_category:<15.2f}{few_category:<15.2f}{better}")

# Urgency
better = "Tie"
if zero_urgency > few_urgency:
    better = "Zero-Shot"
elif few_urgency > zero_urgency:
    better = "Few-Shot"

print(f"{'Urgency':<15}{zero_urgency:<15.2f}{few_urgency:<15.2f}{better}")

# Sentiment
better = "Tie"
if zero_sentiment > few_sentiment:
    better = "Zero-Shot"
elif few_sentiment > zero_sentiment:
    better = "Few-Shot"

print(f"{'Sentiment':<15}{zero_sentiment:<15.2f}{few_sentiment:<15.2f}{better}")

print("-" * 60)

# Overall Average
zero_avg = (zero_category + zero_urgency + zero_sentiment) / 3
few_avg = (few_category + few_urgency + few_sentiment) / 3

print(f"\nAverage Accuracy")
print(f"Zero-Shot : {zero_avg:.2f}%")
print(f"Few-Shot  : {few_avg:.2f}%")

print()

if zero_avg > few_avg:
    print(" Overall Best Prompting Strategy: Zero-Shot")
elif few_avg > zero_avg:
    print(" Overall Best Prompting Strategy: Few-Shot")
else:
    print(" Both strategies performed equally well.")