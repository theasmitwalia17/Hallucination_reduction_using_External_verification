import chromadb
from chromadb.utils import embedding_functions

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

query = "What is a treasury bond?"

results = collection.query(
    query_texts=[query],
    n_results=3
)

print("\nTop 3 Retrieved Chunks:\n")

for i, doc in enumerate(results["documents"][0]):
    print(f"---- Retrieved {i+1} ----")
    print(doc[:500])
    print("\n")