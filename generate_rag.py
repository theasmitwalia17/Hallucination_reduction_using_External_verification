import json
import subprocess
import time
import chromadb
from chromadb.utils import embedding_functions

MODEL = "llama3-finance"
TOP_K = 3
OUTPUT_FILE = "rag/rag_answers.json"

# Load persistent DB
client = chromadb.Client(
    settings=chromadb.config.Settings(
        persist_directory="rag/chroma_db",
        is_persistent=True
    )
)

embedding_function = embedding_functions.OllamaEmbeddingFunction(
    model_name="nomic-embed-text"
)

collection = client.get_collection(
    name="finance_corpus",
    embedding_function=embedding_function
)

with open("data/test_q.json", "r", encoding="utf-8") as f:
    questions = json.load(f)

results = []

total_start = time.time()

for item in questions:

    qid = item["id"]
    question = item["user_query"]

    # Retrieve top-k context
    retrieval = collection.query(
        query_texts=[question],
        n_results=TOP_K
    )

    context = "\n\n".join(retrieval["documents"][0])

    prompt = f"""
    
    You are a highly experienced and certified financial expert assistant.
Your goal is to provide precise, objective, and actionable financial information.

Instructions:
1. Analysis: Carefully analyze the user's financial question for key details and context.
2. Accuracy: Provide answer based strictly on verified financial principles and data. If you do not know the answer or if the information is speculative, explicitly state that.
3. Clarity: Avoid unnecessary jargon. If technical terms are required, briefly explain them.
4. Formatting: Use Markdown (bolding, bullet points) to structure your response for readability.
5. Disclaimer: Remind the user that this is for informational purposes and does not constitute professional investment advice.

Constraint: Do not hallucinate or fabricate numbers, dates, or market data.

Context:
{context}

Question:
{question}

Answer:
"""

    start = time.time()

    process = subprocess.run(
        ["ollama", "run", MODEL],
        input=prompt,
        text=True,
        capture_output=True,
        encoding="utf-8",
        errors="ignore"
    )

    end = time.time()

    answer = process.stdout.strip()
    runtime = round(end - start, 2)

    results.append({
        "id": qid,
        "question": question,
        "answer": answer,
        "runtime_sec": runtime,
        "answer_length_words": len(answer.split())
    })

    print(f"Done: {qid} | {runtime}s")

    time.sleep(0.5)

total_end = time.time()

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)

print("RAG generation complete.")
print("Total runtime (minutes):", round((total_end - total_start)/60, 2))