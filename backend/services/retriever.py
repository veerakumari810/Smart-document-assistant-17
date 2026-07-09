import numpy as np

class RetrieverService:
    @staticmethod
    def retrieve_relevant_chunks(query_embedding, vector_store, top_k: int = 3):
        if vector_store.index is None:
            vector_store.load_index()
            
        if vector_store.index is None:
            return []

        query_vector = np.array([query_embedding]).astype('float32')
        distances, indices = vector_store.index.search(query_vector, top_k)
        
        results = []
        for idx in indices[0]:
            if idx != -1 and idx < len(vector_store.chunks):
                results.append(vector_store.chunks[idx])
        return results