import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from database import documents_collection

# Load AI Model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Function to fetch documents asynchronously
async def get_doc_texts():
    """ Fetch all documents and return their content """
    cursor = documents_collection.find({})
    return [doc["content"] async for doc in cursor]  # ✅ Async comprehension inside async function

async def create_faiss_index():
    """ Create FAISS index with document embeddings """
    doc_texts = await get_doc_texts()  # ✅ Now properly awaited

    if not doc_texts:
        return None  # No documents to index

    doc_embeddings = embedding_model.encode(doc_texts)  # Convert text to embeddings
    index = faiss.IndexFlatL2(doc_embeddings.shape[1])  # Create FAISS index
    index.add(np.array(doc_embeddings))  # Add embeddings

    return index

# Initialize FAISS index (must be awaited somewhere)
faiss_index = None

async def initialize_index():
    """ Initialize FAISS index at startup """
    global faiss_index
    faiss_index = await create_faiss_index()

async def search_documents(query: str):
    """ Search FAISS index for similar documents """
    global faiss_index
    if faiss_index is None:
        return {"error": "No documents indexed"}

    query_embedding = embedding_model.encode([query])  # Encode query
    D, I = faiss_index.search(np.array(query_embedding), k=5)  # Search index

    results = []
    cursor = documents_collection.find({})
    async for doc in cursor:
        if doc["_id"] in I[0]:  # Check if document is in results
            results.append(doc["filename"])

    return {"results": results}
