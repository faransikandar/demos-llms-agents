from pydantic import BaseModel
from typing import List, Optional, Dict

class Message(BaseModel):
    ref_conversation_id: int
    ref_user_id: int
    transaction_datetime_utc: str
    screen_name: str
    message: str
class EvaluateRequest(BaseModel):
    messages_list: List[Message]
    ref_conversation_id: int
    ref_user_id: int

class BeliefStatement(BaseModel):
    topic: str
    statement: str
    certainty: float

class EvaluationSummary(BaseModel):
    conversation_value: Dict[str, float]
    storybot_metrics: Optional[Dict[str, float]] = {}
    user_belief_snapshot: Optional[Dict[str, List[BeliefStatement]]] = {}
    # user_belief_vector: Optional[List[float]] = []
    anomaly_signals: Optional[Dict[str, bool]] = {}

class Recommendation(BaseModel):
    post_id: int
    match_score: float
    title: str

class EvaluateResponse(BaseModel):
    ref_conversation_id: int
    ref_user_id: int
    evaluation_summary: EvaluationSummary
    recommended_posts: Optional[List[Recommendation]] = []
