import json
import re

INPUT_FILE = "evaluation/rag_verified.json"

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

total_claims = 0
false_claims = 0
responses_with_false = 0

for item in data:

    verification = item.get("verification_raw", "")

    if not verification:
        continue

    true_count = len(re.findall(r"\bTrue\b", verification))
    false_count = len(re.findall(r"\bFalse\b", verification))
    unknown_count = len(re.findall(r"\bUnknown\b", verification))

    claims_in_response = true_count + false_count + unknown_count

    if claims_in_response > 0:
        total_claims += claims_in_response

    if false_count > 0:
        responses_with_false += 1
        false_claims += false_count
    else:
        false_claims += false_count

n = len(data)

MiHR = false_claims / total_claims if total_claims > 0 else 0
MaHR = responses_with_false / n if n > 0 else 0

print("Total Responses:", n)
print("Total Claims:", total_claims)
print("False Claims:", false_claims)
print("Micro Hallucination Rate (MiHR):", round(MiHR, 4))
print("Macro Hallucination Rate (MaHR):", round(MaHR, 4))
