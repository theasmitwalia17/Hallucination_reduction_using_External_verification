import json
import subprocess
import time

MODEL = "llama3.1"   # use base model as judge (NOT fine-tuned one)

INPUT_FILE = "rag/rag_answers.json"
OUTPUT_FILE = "evaluation/rag_claims.json"

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    answers = json.load(f)

results = []

for item in answers:

    qid = item["id"]
    answer = item["answer"]

    prompt = f"""
Extract all factual claims from the following answer.
List them as numbered statements.
If no factual claims exist, return: NO_FACTS

Answer:
{answer}
"""

    process = subprocess.run(
        ["ollama", "run", MODEL],
        input=prompt,
        text=True,
        capture_output=True,
        encoding="utf-8",
        errors="ignore"
    )

    claims = process.stdout.strip()

    results.append({
        "id": qid,
        "claims_raw": claims
    })

    print("Extracted:", qid)
    time.sleep(0.5)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)

print("Claim extraction complete.")
