import re
import emoji
import numpy as np
from typing import List, Tuple
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from sentence_transformers import SentenceTransformer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from utils.profiling import benchmark

# ------------------------
# 1. Preloaded Models
# ------------------------

# Embedding model (lightweight, CPU-friendly)
EMBEDDING_MODEL = SentenceTransformer("all-MiniLM-L6-v2")

# VADER (rule-based, fast)
VADER = SentimentIntensityAnalyzer()

# Optional: Transformer sentiment (fallback, larger)
TRANSFORMER_SENTIMENT = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

# ------------------------
# 2. Basic NLP Utilities
# ------------------------

def get_emoji_count(text: str) -> int:
    return len([c for c in text if c in emoji.EMOJI_DATA])

def tokenize_text(text: str) -> List[str]:
    text = re.sub(r'[^\w\s]', '', text.lower())
    return text.split()

# ------------------------
# 3. Sentiment Utilities
# ------------------------

def vader_sentiment(text: str) -> float:
    return VADER.polarity_scores(text)["compound"]

def transformer_sentiment(text: str) -> float:
    # Positive = +1, Negative = -1
    result = TRANSFORMER_SENTIMENT(text)[0]
    return result['score'] if result['label'] == 'POSITIVE' else -result['score']

def aggregate_sentiment(messages: List[str], method="vader") -> List[float]:
    scores = []
    for msg in messages:
        if method == "vader":
            scores.append(vader_sentiment(msg))
        elif method == "transformer":
            scores.append(transformer_sentiment(msg))
    return scores

# ------------------------
# 4. Embedding Utilities
# ------------------------

@benchmark
def embed_text(text: str) -> np.ndarray:
    return EMBEDDING_MODEL.encode(text)

@benchmark
def embed_texts(texts: List[str]) -> np.ndarray:
    return EMBEDDING_MODEL.encode(texts)

def belief_vector_from_statements(statements: List[str]) -> np.ndarray:
    vectors = embed_texts(statements)
    return np.mean(vectors, axis=0)

def cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
    if np.linalg.norm(vec1) == 0 or np.linalg.norm(vec2) == 0:
        return 0.0
    return float(np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2)))
