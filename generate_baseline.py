import json
import subprocess
import time
import os
import sys

# --- CONFIGURATION ---
MODEL = "llama3-finance"

# Use os.path.join for reliable paths on Windows/Linux
# Assuming your script is running from the project root or you want absolute paths:
BASE_DIR = r"C:\Users\theas\OneDrive\Desktop\major project"
DATA_FILE = os.path.join(BASE_DIR, "data", "test_q.json")
PROMPT_FILE = os.path.join(BASE_DIR, "baseline_prompt.txt")
OUTPUT_FILE = os.path.join(BASE_DIR, "baseline", "baseline_answers.json")

# Ensure the output directory actually exists
os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

# --- LOAD INPUT DATA ---
print(f"Loading data from: {DATA_FILE}")

try:
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        questions = json.load(f)
except FileNotFoundError:
    print(f"❌ Error: Input file not found at {DATA_FILE}")
    sys.exit(1)

try:
    with open(PROMPT_FILE, "r", encoding="utf-8") as f:
        prompt_template = f.read()
except FileNotFoundError:
    print(f"❌ Error: Prompt file not found at {PROMPT_FILE}")
    sys.exit(1)

# --- RESUME LOGIC ---
# If file exists and isn't empty, load it to resume
results = []
completed_ids = set()

if os.path.exists(OUTPUT_FILE) and os.path.getsize(OUTPUT_FILE) > 0:
    try:
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            results = json.load(f)
            # Create a set of IDs that are already done
            completed_ids = {item.get("id") for item in results}
        print(f"🔄 Resuming. Already completed: {len(results)} items.")
    except json.JSONDecodeError:
        print("⚠️ Warning: Output file exists but is corrupted. Starting fresh.")

total_start = time.time()

# --- MAIN LOOP ---
print(f"🚀 Starting generation for {len(questions) - len(completed_ids)} remaining items...\n")

for i, item in enumerate(questions):
    qid = item.get("id")

    # Validation: Skip items without an ID
    if qid is None:
        print(f"⚠️ Skipping item at index {i}: Missing 'id' field")
        continue

    # Skip if already done
    if qid in completed_ids:
        continue

    question = item.get("user_query", "")

    # Insert question into template
    prompt = prompt_template.replace("{QUESTION}", question)

    print(f"Processing ID: {qid}...", end="", flush=True)
    start = time.time()

    try:
        # Run Ollama via subprocess
        # encoding='utf-8' is CRITICAL for Windows to handle special chars
        process = subprocess.run(
            ["ollama", "run", MODEL],
            input=prompt,
            text=True,
            capture_output=True,
            encoding="utf-8",
            check=False  # We handle errors manually below
        )

        if process.returncode != 0:
            print(f" ❌ Error: Ollama exited with code {process.returncode}")
            print(f"Stderr: {process.stderr}")
            continue  # Skip saving this failed attempt

        answer = process.stdout.strip()

    except Exception as e:
        print(f" ❌ Subprocess crash: {e}")
        continue

    end = time.time()
    runtime = round(end - start, 2)

    # Append new result
    results.append({
        "id": qid,
        "question": question,
        "answer": answer,
        "answer_length_chars": len(answer),
        "answer_length_words": len(answer.split()),
        "runtime_sec": runtime
    })

    # Mark as done in memory
    completed_ids.add(qid)

    # --- SAVE CHECKPOINT ---
    # We save the whole list every time.
    # ensure_ascii=False makes the JSON readable (keeps emojis/currency symbols)
    try:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"\n❌ Error saving file: {e}")

    print(f" ✅ Done ({runtime}s | {len(answer.split())} words)")

    # Small sleep to let the system cool down slightly
    time.sleep(0.1)

total_end = time.time()

print("\n" + "=" * 40)
print("🎉 Baseline generation complete.")
print(f"Total Questions Processed: {len(results)}")
print(f"Total Runtime: {round((total_end - total_start) / 60, 2)} minutes")
print(f"Saved to: {OUTPUT_FILE}")