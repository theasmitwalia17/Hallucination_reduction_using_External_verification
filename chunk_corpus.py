import os
import json

CHUNK_SIZE = 400
OVERLAP = 80
INPUT_FOLDER = "corpus"
OUTPUT_FILE = "rag/chunks.json"

os.makedirs("rag", exist_ok=True)

chunks = []
chunk_id = 0

for filename in os.listdir(INPUT_FOLDER):

    if not filename.endswith(".txt"):
        continue

    with open(os.path.join(INPUT_FOLDER, filename), "r", encoding="utf-8") as f:
        text = f.read()

    words = text.split()

    for i in range(0, len(words), CHUNK_SIZE - OVERLAP):
        chunk = words[i:i + CHUNK_SIZE]

        if len(chunk) < 80:
            continue

        chunks.append({
            "id": str(chunk_id),
            "text": " ".join(chunk)
        })

        chunk_id += 1

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(chunks, f, indent=2)

print("Total chunks created:", len(chunks))