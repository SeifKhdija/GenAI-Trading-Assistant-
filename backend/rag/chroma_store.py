try:
    import chromadb
except ImportError:
    chromadb = None

# Initialize with lazy loading to prevent import-time errors
_client = None
_collection = None

# Note: sentence-transformers removed due to torch/transformers compatibility issues
# The RAG functionality will use fallback keyword-based search instead


def get_client():
    global _client
    if _client is None and chromadb is not None:
        _client = chromadb.Client()
    return _client


def get_collection():
    global _collection
    if _collection is None:
        client = get_client()
        if client is not None:
            _collection = client.create_collection("market_knowledge")
    return _collection


def load_knowledge():
    """Load knowledge documents into the vector store (fallback mode without embeddings)."""
    if chromadb is None:
        print("Warning: chromadb not available. Skipping knowledge loading.")
        return
    
    collection = get_collection()
    
    if collection is None:
        return
    
    try:
        with open('backend/rag/knowledge.txt', 'r') as f:
            docs = f.readlines()

        for i, doc in enumerate(docs):
            # Store documents without embeddings (sentence-transformers not available)
            collection.add(
                ids=[str(i)],
                documents=[doc.strip()],
                metadatas=[{"source": "knowledge.txt"}]
            )
    except FileNotFoundError:
        print("Warning: knowledge.txt file not found")


def search_context(query):
    """Search for relevant context given a query (keyword-based fallback)."""
    if chromadb is None:
        print("Warning: chromadb not available")
        return []
    
    collection = get_collection()
    
    if collection is None:
        return []
    
    try:
        # Use keyword-based search since embeddings unavailable
        results = collection.query(
            query_texts=[query],
            n_results=3
        )
        return results['documents'][0] if results and 'documents' in results else []
    except Exception as e:
        print(f"Warning: Error searching context: {e}")
        return []