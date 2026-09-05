import os
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()

KB_PATH = os.path.join(os.path.dirname(__file__), "..", "knowledge_base", "lab_reference.txt")
INDEX_PATH = os.path.join(os.path.dirname(__file__), "..", "faiss_index")


def build_vector_store():
    """Reads the reference text, splits it into paragraphs (one per lab test),
    embeds each with Google's embedding model, and saves a FAISS index to disk."""
    with open(KB_PATH, "r", encoding="utf-8") as f:
        text = f.read()

    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks = [Document(page_content=p) for p in paragraphs]

    embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")
    vector_store = FAISS.from_documents(chunks, embeddings)
    vector_store.save_local(INDEX_PATH)

    return vector_store


def load_vector_store():
    """Loads the FAISS index from disk, building it first if it doesn't exist yet."""
    embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")

    if not os.path.exists(INDEX_PATH):
        return build_vector_store()

    return FAISS.load_local(
        INDEX_PATH, embeddings, allow_dangerous_deserialization=True
    )


if __name__ == "__main__":
    build_vector_store()
    print("Vector store built and saved to", INDEX_PATH)