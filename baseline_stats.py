import json
import numpy as np

with open("baseline/baseline_answers.json", "r", encoding="utf-8") as f:
    data = json.load(f)

runtimes = [item["runtime_sec"] for item in data]
lengths = [item["answer_length_words"] for item in data]

print("Baseline Summary Statistics")
print("--------------------------------")
print("Total Questions:", len(data))
print("Avg Runtime (sec):", round(np.mean(runtimes), 2))
print("Median Runtime (sec):", round(np.median(runtimes), 2))
print("Avg Answer Length (words):", round(np.mean(lengths), 2))
print("Median Answer Length (words):", round(np.median(lengths), 2))