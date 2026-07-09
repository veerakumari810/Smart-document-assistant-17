import os
import pickle
import faiss
import numpy as np

class FAISSVectorStore:
    def __init__(self, index_dir="database/faiss_index"):
        self.index_dir = index_dir
        self.index_path = os.path.join(index_dir, "index.faiss")
        self.metadata_path = os.path.join(index_dir, "metadata.pkl")
        os.makedirs(index_dir, exist_ok=True)
        self.index = None
        self.chunks = []

    def add_documents(self, chunks: list, embeddings: np.ndarray):
        dimension = embeddings.shape[1]
        
        if self.index is None:
            self.index = faiss.IndexFlatL2(dimension)
            
        self.index.add(np.array(embeddings).astype('float32'))
        self.chunks.extend(chunks)
        self.save_index()

    def save_index(self):
        faiss.write_index(self.index, self.index_path)
        with open(self.metadata_path, "wb") as f:
            pickle.dump(self.chunks, f)

    def load_index(self):
        # Windows లో క్లీన్‌గా లోడ్ అవ్వడానికి rb మోడ్ పక్కాగా ఇక్కడ ఫిక్స్ చేసాము
        if os.path.exists(self.index_path) and os.path.exists(self.metadata_path):
            try:
                self.index = faiss.read_index(self.index_path)
                with open(self.metadata_path, "rb") as f:
                    self.chunks = pickle.load(f)
                return True
            except Exception as e:
                print(f"Error loading FAISS index: {e}")
                return False
        return False