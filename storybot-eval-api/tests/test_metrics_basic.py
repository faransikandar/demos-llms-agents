from evaluation.metrics_basic import compute_basic_metrics
from api.schemas import Message

def test_basic_metrics_outputs_expected_keys():
    sample_convo = [
        Message(
            message="I feel stuck 😞",
            screen_name="user_123",
            ref_conversation_id=1,
            ref_user_id=999,
            transaction_datetime_utc="2023-10-01T10:15:00Z"
        ),
        Message(
            message="That sounds hard. Can you tell me more?",
            screen_name="StoryBot",
            ref_conversation_id=1,
            ref_user_id=999,
            transaction_datetime_utc="2023-10-01T10:16:00Z"
        ),
    ]

    result = compute_basic_metrics(sample_convo)
    assert isinstance(result, dict)
    assert "round_count" in result
    assert "avg_message_length" in result
    assert "emoji_count" in result
    assert "unique_word_ratio" in result
