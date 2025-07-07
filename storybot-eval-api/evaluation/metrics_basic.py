from collections import Counter
from typing import List, Dict
import re
import numpy as np
from utils.nlp_tools import get_emoji_count, tokenize_text

def compute_basic_metrics(conversation: List["Message"]) -> Dict[str, float]:
    """
    Compute lightweight, interpretable metrics from a single conversation.
    """
    messages = [msg.message for msg in conversation]
    user_messages = [msg.message for msg in conversation if "storybot" not in msg.screen_name.lower()]

    round_count = int(len(conversation) / 2)
    user_message_lengths = [len(m) for m in user_messages]
    user_avg_msg_len = np.mean(user_message_lengths)

    user_emoji_total = sum(get_emoji_count(m) for m in messages)

    user_all_words = []
    for msg in user_messages:
        user_all_words.extend(tokenize_text(msg))
    user_unique_words = set(user_all_words)
    type_token_ratio = len(user_unique_words) / max(1, len(user_all_words))

    return {
        "round_count": round_count,
        "user_avg_message_length": round(user_avg_msg_len, 2),
        "user_emoji_count": user_emoji_total,
        "user_unique_word_ratio": round(type_token_ratio, 2)
    }
