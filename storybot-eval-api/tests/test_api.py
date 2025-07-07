
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_healthz():
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_evaluate_endpoint_valid_input():
    payload = {
        "ref_conversation_id": 1,
        "ref_user_id": 999,
        "messages_list": [
            {
                "message": "Hi, I'm feeling anxious 😟",
                "screen_name": "user_999",
                "ref_conversation_id": 1,
                "ref_user_id": 999,
                "transaction_datetime_utc": "2024-01-01T12:00:00Z"
            },
            {
                "message": "That's understandable. Want to tell me more?",
                "screen_name": "StoryBot",
                "ref_conversation_id": 1,
                "ref_user_id": 999,
                "transaction_datetime_utc": "2024-01-01T12:01:00Z"
            }
        ]
    }

    response = client.post("/evaluate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "ref_conversation_id" in data
    assert "evaluation_summary" in data
    assert "conversation_value" in data["evaluation_summary"]
