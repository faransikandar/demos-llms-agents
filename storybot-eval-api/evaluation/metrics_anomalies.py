import re
import numpy as np
from typing import List, Dict
from datetime import datetime
from utils.nlp_tools import get_emoji_count, tokenize_text, aggregate_sentiment

PROMPT_INJECTION_PATTERNS = [
    r"ignore previous instructions",
    r"you are now",
    r"repeat after me",
    r"system prompt",
    r"simulate being",
    r"as an AI",
    r"jailbreak"
]

TOPIC_STOPWORDS = {"the", "and", "is", "you", "i", "to", "a", "it", "of", "in", "that", "this"}

def detect_anomalies(conversation: List["Message"]) -> Dict[str, bool | float]:
    user_messages = [msg.message for msg in conversation if "storybot" not in msg.screen_name.lower()]
    messages = [msg.message for msg in conversation]

    return {
        "emoji_spike": detect_emoji_spike(messages),
        "language_style_shift": detect_language_shift(messages),
        "mood_spike": detect_mood_spike(messages),
        "topic_drift": detect_topic_spike(messages),
        "prompt_injection_flagged": detect_prompt_injection(messages),
        # "user_response_time_delta": get_max_user_response_time([
        #     msg for msg in conversation if "storybot" not in msg.screen_name.lower()
        # ]),

        # "repetition_or_contradiction": detect_repetition_or_contradiction(messages)
    }

# ---------- Existing Anomaly Heuristics ----------

def detect_emoji_spike(messages: List[str], threshold: float = 2.5) -> bool:
    emoji_counts = [get_emoji_count(msg) for msg in messages]
    if len(emoji_counts) < 2:
        return False
    avg = np.mean(emoji_counts[:-1]) or 1e-3
    return emoji_counts[-1] > threshold * avg

def detect_language_shift(messages: List[str], delta_thresh: float = 1.5) -> bool:
    if len(messages) < 4:
        return False
    lengths = [len(tokenize_text(msg)) for msg in messages]
    return abs(lengths[-1] - np.mean(lengths[:-1])) > delta_thresh * np.std(lengths[:-1])

def detect_mood_spike(messages: List[str], spike_threshold: float = 0.75) -> bool:
    sentiments = aggregate_sentiment(messages)
    if len(sentiments) < 2:
        return False
    return abs(sentiments[-1] - np.mean(sentiments[:-1])) > spike_threshold

def detect_topic_spike(messages: List[str], uniqueness_thresh: float = 0.5) -> bool:
    def keywords(msg):
        return set(w for w in tokenize_text(msg) if w not in TOPIC_STOPWORDS)

    if len(messages) < 4:
        return False

    prev_kw = set.union(*[keywords(m) for m in messages[:-1]])
    curr_kw = keywords(messages[-1])
    if not curr_kw:
        return False
    novelty = len(curr_kw - prev_kw) / len(curr_kw)
    return novelty > uniqueness_thresh

def detect_prompt_injection(messages: List[str]) -> bool:
    joined = " ".join(messages).lower()
    return any(re.search(pat, joined) for pat in PROMPT_INJECTION_PATTERNS)

# def get_max_user_response_time(user_msgs: List[dict]) -> float:
#     """Return max response delta in seconds between consecutive user messages."""
#     timestamps = [m["transaction_datetime_utc"] for m in user_msgs]
#     if len(timestamps) < 2:
#         return 0.0
#     times = [datetime.fromisoformat(ts.replace("Z", "+00:00")) for ts in timestamps]
#     deltas = [(t2 - t1).total_seconds() for t1, t2 in zip(times[:-1], times[1:])]
#     return round(max(deltas), 2)

# def detect_repetition_or_contradiction(messages: List[str], thresh=0.85) -> bool:
#     """Detect repeated or nearly identical messages based on cosine similarity."""
#     if len(messages) < 3:
#         return False
#     from utils.nlp_tools import embed_texts, cosine_similarity
#     embeddings = embed_texts(messages)
#     sim_scores = []
#     for i in range(len(embeddings) - 1):
#         sim = cosine_similarity(embeddings[i], embeddings[i + 1])
#         sim_scores.append(sim)
#     repeat_count = sum(1 for sim in sim_scores if sim > thresh)
#     return repeat_count >= 2
