import os
import chromadb

from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.config import (
    CHROMA_DB_DIR,
    COLLECTION_NAME,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    TOP_K
)

load_dotenv()


class RAGPipeline:

    def __init__(self):

        self.embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

        self.chroma_client = chromadb.PersistentClient(
            path=CHROMA_DB_DIR
        )

        self.collection = self.chroma_client.get_or_create_collection(
            name=COLLECTION_NAME
        )

    def get_embedding(self, text):
        return self.embedding_model.encode(text).tolist()


    def load_document(self, filepath):

        ext = os.path.splitext(filepath)[1].lower()

        if ext in [".txt", ".md"]:

            with open(
                filepath,
                "r",
                encoding="utf-8"
            ) as f:
                return f.read()

        elif ext == ".pdf":

            reader = PdfReader(filepath)

            text = ""

            for page in reader.pages:

                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

            return text

        return ""

    def ingest_file(self, filepath):

        text = self.load_document(filepath)

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP
        )

        chunks = splitter.split_text(text)

        filename = os.path.basename(filepath)

        for idx, chunk in enumerate(chunks):

            embedding = self.get_embedding(chunk)

            self.collection.add(
                ids=[f"{filename}_{idx}"],
                embeddings=[embedding],
                documents=[chunk],
                metadatas=[
                    {
                        "source": filename,
                        "chunk": idx
                    }
                ]
            )

    def retrieve(self, query):

        query_embedding = self.get_embedding(query)

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=TOP_K
        )

        retrieved = []

        docs = results["documents"][0]
        metas = results["metadatas"][0]
        distances = results["distances"][0]

        for doc, meta, dist in zip(
            docs,
            metas,
            distances
        ):

            retrieved.append(
                {
                    "text": doc,
                    "source": meta["source"],
                    "score": round(1 - dist, 3)
                }
            )

        return retrieved