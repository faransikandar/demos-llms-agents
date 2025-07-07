import faiss
import numpy as np

class BeliefIndexer:
    def __init__(self, dim: int = 384):
        self.index = faiss.IndexFlatL2(dim)
        self.vectors = []
        self.user_ids = []

    def add(self, user_id: int, vector: List[float]):
        vec_np = np.array(vector).astype('float32')
        self.index.add(np.expand_dims(vec_np, axis=0))
        self.vectors.append(vec_np)
        self.user_ids.append(user_id)

    def query(self, vector: List[float], k: int = 5) -> List[int]:
        vec_np = np.array(vector).astype('float32').reshape(1, -1)
        distances, indices = self.index.search(vec_np, k)
        return [self.user_ids[i] for i in indices[0] if i < len(self.user_ids)]
