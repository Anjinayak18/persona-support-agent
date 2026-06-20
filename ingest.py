import os

from src.rag_pipeline import RAGPipeline

DATA_DIR = "data"

rag = RAGPipeline()

files = os.listdir(DATA_DIR)

count = 0

for file in files:

    path = os.path.join(
        DATA_DIR,
        file
    )

    if os.path.isfile(path):

        print(f"Indexing {file}")

        rag.ingest_file(path)

        count += 1

print()
print(f"Successfully indexed {count} files")