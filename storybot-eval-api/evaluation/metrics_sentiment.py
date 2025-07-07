from typing import List, Dict
import numpy as np
from utils.nlp_tools import aggregate_sentiment

def compute_sentiment_metrics(conversation: List["Message"]) -> Dict[str, float]:
    user_messages = [msg.message for msg in conversation if "storybot" not in msg.screen_name.lower()]

    sentiment_scores = aggregate_sentiment(user_messages, method="vader")
    if not sentiment_scores:
        return {
            "sentiment_start": 0.0,
            "sentiment_end": 0.0,
            "sentiment_delta": 0.0,
            "mood_volatility": 0.0
        }

    return {
        "sentiment_start": round(sentiment_scores[0], 3),
        "sentiment_end": round(sentiment_scores[-1], 3),
        "sentiment_delta": round(sentiment_scores[-1] - sentiment_scores[0], 3),
        "mood_volatility": round(np.std(sentiment_scores), 3)
    }
