from fastapi import APIRouter
from api.schemas import EvaluateRequest, EvaluateResponse
from evaluation.metrics_basic import compute_basic_metrics
from evaluation.metrics_sentiment import compute_sentiment_metrics
from evaluation.metrics_belief_shift import extract_beliefs_and_vector
from evaluation.metrics_anomalies import detect_anomalies
from recommendation.recommender import recommend_content
from utils.profiling import benchmark

router = APIRouter()

@router.get("/healthz")
def health_check():
    return {"status": "ok"}

@router.post("/evaluate", response_model=EvaluateResponse)
@benchmark
def evaluate_conversation(payload: EvaluateRequest):
    convo = payload.messages_list
    ref_id = payload.ref_conversation_id
    ref_user_id = payload.ref_user_id  # assumes first user msg is user

    # Metrics
    basic_metrics = compute_basic_metrics(convo)
    sentiment_metrics = compute_sentiment_metrics(convo)
    beliefs, belief_vector = extract_beliefs_and_vector(convo)
    anomalies = detect_anomalies(convo)

    # Recommend posts based on beliefs
    recs = recommend_content(belief_vector)

    return {
        "ref_conversation_id": ref_id,
        "ref_user_id": ref_user_id,
        "evaluation_summary": {
            "conversation_value": basic_metrics | sentiment_metrics,
            "storybot_metrics": {},  # placeholder for storybot metrics re: performance, relevance, engagement, etc.
            "user_belief_snapshot": {"beliefs": beliefs["beliefs"]},
            # "user_belief_vector": belief_vector,
            "anomaly_signals": anomalies
        },
        "recommended_posts": recs
    }
