import json
import random

random.seed(42)

with open("HaluEval-2.0-master\data\Finance.json", "r", encoding="utf-8") as f:
    data = json.load(f)

random.shuffle(data)

train = data[:600]
test = data[600:1100]

with open("train_q.json", "w") as f:
    json.dump(train, f, indent=2)

with open("test_q.json", "w") as f:
    json.dump(test, f, indent=2)

print("Train Q:", len(train))
print("Test Q:", len(test))
