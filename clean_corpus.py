import os
import re

INPUT_FOLDER = "corpus"
MIN_WORDS = 200  # discard very small docs

cleaned_docs = 0
removed_docs = 0

print("--- Step 1: Cleaning and Filtering ---")

# Step 1: Process files (Clean content and remove short ones)
for filename in os.listdir(INPUT_FOLDER):
    path = os.path.join(INPUT_FOLDER, filename)

    if not filename.endswith(".txt"):
        continue

    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
    except Exception as e:
        print(f"Skipping {filename}: Error reading file.")
        continue

    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()

    # Remove weird symbols (basic cleanup)
    text = re.sub(r'[^a-zA-Z0-9.,;:()\-\'\"%$ ]+', '', text)

    word_count = len(text.split())

    if word_count < MIN_WORDS:
        os.remove(path)
        removed_docs += 1
        # print(f"Removed: {filename} ({word_count} words)") # Uncomment to see details
    else:
        # Overwrite the file with cleaned text
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        cleaned_docs += 1

print(f"Cleaning complete. Kept: {cleaned_docs}, Removed: {removed_docs}")
print("\n--- Step 2: Renaming Files ---")

# Step 2: Rename remaining files sequentially
# We get the list of files again because some were deleted in Step 1
remaining_files = [f for f in os.listdir(INPUT_FOLDER) if f.endswith(".txt")]

# Sort them to ensure deterministic order (optional, but good practice)
remaining_files.sort()

count = 1
for filename in remaining_files:
    old_path = os.path.join(INPUT_FOLDER, filename)

    # Define new filename
    new_filename = f"file{count}.txt"
    new_path = os.path.join(INPUT_FOLDER, new_filename)

    # Rename
    # Check if name is actually changing to avoid errors if file1.txt already exists
    if old_path != new_path:
        try:
            os.rename(old_path, new_path)
        except OSError as e:
            print(f"Error renaming {filename}: {e}")

    count += 1

print(f"Renaming complete. Files are now named file1.txt through file{count - 1}.txt")