import json
import chromadb
from chromadb.utils import embedding_functions

# Persistent storage folder
client = chromadb.Client(
    settings=chromadb.config.Settings(
        persist_directory="rag/chroma_db",
        is_persistent=True
    )
)

embedding_function = embedding_functions.OllamaEmbeddingFunction(
    model_name="nomic-embed-text"
)

collection = client.get_or_create_collection(
    name="finance_corpus",
    embedding_function=embedding_function
)

with open("rag/chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

print("Indexing started...")

for item in chunks:
    collection.add(
        documents=[item["text"]],
        ids=[item["id"]]
    )

print("Index built successfully.")
print("Total indexed:", collection.count())