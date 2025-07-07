from typing import List, Dict, Tuple
import json
import numpy as np
from utils.nlp_tools import embed_texts, cosine_similarity

POSTS_PATH = "data/discussions.json"

with open(POSTS_PATH, "r") as f:
    POST_DATA = json.load(f)

# Precompute post vectors once (can cache for prod)
POSTS = []
POST_VECTORS = []

for entry in POST_DATA:
    main_msg = entry["messages_list"][0]["text"]
    POSTS.append({"post_id": entry["post_id"], "title": main_msg})
    POST_VECTORS.append(embed_texts([main_msg])[0])

POST_VECTORS = np.array(POST_VECTORS)

def recommend_content(belief_vector: List[float], top_k=3):
    sims = [cosine_similarity(np.array(belief_vector), vec) for vec in POST_VECTORS]
    top_indices = np.argsort(sims)[-top_k:][::-1]

    return [
        {
            "post_id": POSTS[i]["post_id"],
            "match_score": round(sims[i], 3),
            "title": POSTS[i]["title"][:100]
        }
        for i in top_indices
    ]
