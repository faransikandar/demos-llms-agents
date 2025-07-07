from typing import List, Dict, Tuple
from api.schemas import BeliefStatement
from utils.nlp_tools import embed_texts, cosine_similarity

def extract_beliefs_and_vector(conversation: List["Message"]) -> Tuple[Dict[str, List[BeliefStatement]], List[float]]:
    user_messages = [msg.message for msg in conversation if "storybot" not in msg.screen_name.lower()]
    if len(user_messages) < 2:
        return {"beliefs": []}, []

    # Take first and last messages as indicative beliefs
    belief_statements = [user_messages[0], user_messages[-1]]
    belief_vector = embed_texts(belief_statements).mean(axis=0)

    beliefs = [
        BeliefStatement(topic="general", statement=belief_statements[0], certainty=0.5),
        BeliefStatement(topic="general", statement=belief_statements[1], certainty=0.7)
    ]

    return {"beliefs": beliefs}, belief_vector.tolist()
