import os
import shutil

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from app.exceptions import PolicyNotFoundException
from app.config import (
    POLICY_FILE,
    CHROMA_DB_PATH,
    EMBEDDING_MODEL,
)


class PolicyRetriever:
    """
    Handles:
    1. Loading travel policy
    2. Chunking
    3. Embedding generation
    4. ChromaDB creation
    5. Semantic retrieval
    """

    _embeddings = None
    _vectordb = None

    def __init__(self):

        if PolicyRetriever._embeddings is None:

            print("Loading embedding model...")

            PolicyRetriever._embeddings = HuggingFaceEmbeddings(
                model_name=EMBEDDING_MODEL
            )

        self.embeddings = PolicyRetriever._embeddings


    ###########################################################
    # Load Policy Document
    ###########################################################

    def load_documents(self):

        if not os.path.exists(POLICY_FILE):
            raise PolicyNotFoundException(
                f"Policy file not found: {POLICY_FILE}"
            )

        loader = TextLoader(POLICY_FILE, encoding="utf-8")

        documents = loader.load()

        return documents

    ###########################################################
    # Split into Chunks
    ###########################################################

    def split_documents(self, documents):

        splitter = RecursiveCharacterTextSplitter(

            chunk_size=300,

            chunk_overlap=30,

            separators=[
                "\n\n",
                "\n",
                ".",
                " ",
                ""
            ]
        )

        chunks = splitter.split_documents(documents)

        return chunks

    ###########################################################
    # Delete Existing ChromaDB
    ###########################################################

    def delete_vector_db(self):

        if os.path.exists(CHROMA_DB_PATH):
            shutil.rmtree(CHROMA_DB_PATH)

            print("Existing ChromaDB deleted.")

    ###########################################################
    # Create Vector Database
    ###########################################################

    def create_vector_db(self):

        self.delete_vector_db()

        docs = self.load_documents()

        chunks = self.split_documents(docs)

        vectordb = Chroma.from_documents(

            documents=chunks,

            embedding=self.embeddings,

            persist_directory=CHROMA_DB_PATH

        )

        print(f"Created Vector DB with {len(chunks)} chunks.")

        return vectordb


    def load_vector_db(self):

        if not os.path.exists(CHROMA_DB_PATH):

            print("Vector database not found.")

            print("Creating ChromaDB...")

            self.create_vector_db()

        vectordb = Chroma(

            persist_directory=CHROMA_DB_PATH,

            embedding_function=self.embeddings

        )

        return vectordb

    ###########################################################
    # Retrieve Similar Chunks
    ###########################################################

    def retrieve(self, query, k=3):

        db = self.load_vector_db()

        results = db.similarity_search(
            query,
            k=k
        )

        return results
        
    ###########################################################
    # Retrieve with Similarity Score
    ###########################################################

    def retrieve_with_score(self, query, k=3):

        vectordb = self.load_vector_db()

        results = vectordb.similarity_search_with_score(

            query,

            k=k

        )

        return results

    ###########################################################
    # Pretty Print Results
    ###########################################################

    def print_results(self, query):

        print("=" * 70)

        print("QUERY : ", query)

        print("=" * 70)

        docs = self.retrieve(query)

        for i, doc in enumerate(docs, start=1):

            print(f"\nChunk {i}")

            print("-" * 50)

            print(doc.page_content)

        print("=" * 70)