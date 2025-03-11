from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
import os

# Load and chunk the scraped data
def load_and_chunk_data():
    documents = []
    for filename in os.listdir("data"):
        with open(f"data/{filename}", "r", encoding="utf-8") as f:
            text = f.read()
            documents.append(text)
    
    # Split into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.create_documents(documents)
    return chunks

# Build ChromaDB
def build_vector_store():
    chunks = load_and_chunk_data()
    
    # Use sentence-transformers for embeddings
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # Store in ChromaDB
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory="./chroma_db_multiplePage"
    )
    vector_store.persist()  # Save to disk
    print("Vector store created and persisted.")
    return vector_store

if __name__ == "__main__":
    build_vector_store()



# from langchain_community.vectorstores import Chroma
# from langchain_community.embeddings import HuggingFaceEmbeddings

# # Load the embedding model (same one used during indexing)
# embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# # Load the existing ChromaDB vector store
# vector_store = Chroma(
#     persist_directory="./chroma_db_multiplePage",  # Ensure this matches your stored DB path
#     embedding_function=embeddings
# )

# # Get stored document count correctly
# doc_count = vector_store._collection.count()
# print(f"Total stored documents: {doc_count}")
