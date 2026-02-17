import json
import subprocess
import time
import re

MODEL = "llama3.1"

INPUT_FILE = "evaluation/rag_claims.json"
OUTPUT_FILE = "evaluation/rag_verified.json"

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

results = []

for item in data:

    qid = item["id"]
    claims_text = item["claims_raw"]

    if "NO_FACTS" in claims_text:
        results.append({
            "id": qid,
            "verified_claims": []
        })
        continue

    prompt = f"""
For each claim below, label it as:
True
False
Unknown

Claims:
{claims_text}
"""

    process = subprocess.run(
        ["ollama", "run", MODEL],
        input=prompt,
        text=True,
        capture_output=True,
        encoding="utf-8",
        errors="ignore"
    )

    verification = process.stdout.strip()

    results.append({
        "id": qid,
        "verification_raw": verification
    })

    print("Verified:", qid)
    time.sleep(0.5)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)

print("Verification complete.")