"""Data preprocessing and indexing script."""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.config import settings
from app.services.preprocessing import PreprocessingService
from app.infrastructure.embedding import create_embedding_model
from app.infrastructure.vector_store import create_vector_store


def main():
    """Main preprocessing and indexing function."""
    print("="  * 60)
    print("Perso.ai Chatbot - Data Preprocessing & Indexing")
    print("=" * 60)
    
    # Step 1: Load and preprocess data
    print("\n[Step 1] Loading Q&A data...")
    preprocessor = PreprocessingService(settings.data_file)
    
    try:
        chunks = preprocessor.create_chunks()
        print(f"Created {len(chunks)} chunks from data")
        
        if not preprocessor.validate_chunks(chunks):
            print("Error: Chunk validation failed")
            return
        print("Chunk validation passed")
        
    except Exception as e:
        print(f"Error preprocessing data: {e}")
        return
    
    # Step 2: Initialize embedding model
    print("\n[Step 2] Initializing embedding model...")
    try:
        embedding_model = create_embedding_model(
            api_key=settings.gemini_api_key,
            model_name=settings.embedding_model,
            dimension=settings.embedding_dimension
        )
        print(f"Loaded embedding model: {settings.embedding_model}")
        print(f"Embedding dimension: {embedding_model.get_dimension()}")
        
    except Exception as e:
        print(f"Error loading embedding model: {e}")
        return
    
    # Step 3: Generate embeddings
    print("\n[Step 3] Generating embeddings...")
    try:
        contents = [chunk["content"] for chunk in chunks]
        embeddings = embedding_model.encode(contents)
        print(f"Generated {len(embeddings)} embeddings")
        print(f"Embedding shape: {embeddings.shape}")
        
    except Exception as e:
        print(f"Error generating embeddings: {e}")
        return
    
    # Step 4: Initialize Qdrant
    print("\n[Step 4] Connecting to Qdrant...")
    try:
        vector_store = create_vector_store(
            host=settings.qdrant_host,
            port=settings.qdrant_port,
            collection_name=settings.qdrant_collection_name,
            embedding_dimension=settings.embedding_dimension,
            api_key=settings.qdrant_api_key
        )
        
        if not vector_store.health_check():
            print("Error: Cannot connect to Qdrant")
            print("Make sure Qdrant is running: docker run -p 6333:6333 qdrant/qdrant")
            return
        
        print(f"Connected to Qdrant at {settings.qdrant_host}:{settings.qdrant_port}")
        
    except Exception as e:
        print(f"Error connecting to Qdrant: {e}")
        return
    
    # Step 5: Create collection
    print("\n[Step 5] Creating Qdrant collection...")
    try:
        response = input(f"Collection '{settings.qdrant_collection_name}' will be created/recreated. Continue? (y/n): ")
        if response.lower() != 'y':
            print("Aborted by user")
            return
        
        vector_store.create_collection(recreate=True)
        print(f"Created collection: {settings.qdrant_collection_name}")
        
    except Exception as e:
        print(f"Error creating collection: {e}")
        return
    
    # Step 6: Index documents
    print("\n[Step 6] Indexing documents...")
    try:
        success = vector_store.index_documents(embeddings, chunks)
        
        if success:
            print(f"Successfully indexed {len(chunks)} documents")
            
            info = vector_store.get_collection_info()
            print(f"\nCollection Information:")
            print(f"  Name: {info.get('name')}")
            print(f"  Points: {info.get('points_count')}")
            print(f"  Vectors: {info.get('vectors_count')}")
            print(f"  Status: {info.get('status')}")
        else:
            print("Error: Indexing failed")
            return
            
    except Exception as e:
        print(f"Error indexing documents: {e}")
        return
    
    # Step 7: Test search
    print("\n[Step 7] Testing search...")
    try:
        test_query = "Perso.ai는 무엇인가요?"
        print(f"Test query: {test_query}")

        query_embedding = embedding_model.encode([test_query])[0]
        results = vector_store.search(query_embedding, top_k=3)
        
        print(f"\nFound {len(results)} results:")
        for i, result in enumerate(results, 1):
            print(f"\n  Result {i}:")
            print(f"    Score: {result['score']:.3f}")
            print(f"    Question: {result['question'][:50]}...")
            print(f"    Answer: {result['answer'][:80]}...")
            
    except Exception as e:
        print(f"Error testing search: {e}")
        return
    
    print("\n" + "=" * 60)
    print("Preprocessing and indexing completed successfully")
    print("=" * 60)
    print("\nYou can now start the API server:")
    print("  uvicorn app.main:app --reload")


if __name__ == "__main__":
    main()
