# StoryBot Health - Conversational Evaluation + Recommendations API

## Overview

This project leverages conversational data from a fictional mental health wellness product to understand how individuals perceive themselves and how these perceptions evolve over time. These conversations come from one-on-one conversations between a user and a generative agent (StoryBot) - also included is data on a person-to-person community discussion board about health topics and a user activity log. The evolving identity signal drives personalization and recommendation systems - i.e. using user-bot conversation data to recommend person-to-perrson cocmmunity discussion topics.

This project implements a modular, extensible REST API system for:
- Evaluating conversations between users and StoryBot
- Extracting and tracking user beliefs over time
- Monitoring anomalies in conversational behavior
- Recommending community content aligned with user aspirations

Future extensions of the API include:
- Improved metrics and modeling choices
- Integrating a Streamlit app for visualization of embedding space and recommendations
- Simulating message processing in "real time" for anomaly detection, as well as sentiment analysis and recommendations

The API addresses four key product areas:
1. **Conversation Value**: Quantifies engagement, sentiment change, and introspective depth.
2. **StoryBot Development**: Analyzes bot response quality, timing, and user behavioral responses.
3. **Community Recommendations**: Suggests posts using belief vectors and aspirational alignment.
4. **Anomaly Detection**: Flags emotional spikes, topic shifts, or prompt injection attempts.

---

## Features

- **Phase 1: Basic Metrics**
  - Round count, emoji use, message lengths, sentiment polarity
- **Phase 2: Emotional and Thematic Depth**
  - Mood volatility, sentiment trajectory, StoryBot impact on tone
- **Phase 3: Belief Evolution**
  - Identity vector extraction, belief shifts via embeddings
  - FAISS-based trajectory modeling and belief similarity lookup
- **Phase 4: Anomaly Monitoring**
  - Spike detection (emoji, sentiment)
  - Topic drift and prompt injection heuristics

-----

## Repo Structure

```
storybot_eval_api/
├── data/
│   ├── conversations.json
│   ├── discussions.json
│   ├── activity.json
│
├── api/
│   ├── __init__.py
│   ├── main.py                         # FastAPI setup
│   ├── schemas.py                      # Pydantic I/O schemas
│   ├── router.py                       # Route: POST /evaluate, /recommend
│
├── evaluation/
│   ├── metrics_basic.py                # Phase 1: rounds, emojis, message len
│   ├── metrics_sentiment.py            # Phase 2: mood/tone trajectory
│   ├── metrics_belief_shift.py         # Phase 3: identity/belief vector Δ
│   ├── metrics_anomalies.py            # Phase 4: emoji spike, injection, topic spike
│
├── recommendation/
│   ├── belief_indexer.py               # FAISS: user/belief vector index
│   ├── content_indexer.py              # FAISS: post embedding index
│   ├── recommender.py                  # Recommend content from beliefs
│
├── utils/
│   ├── nlp_tools.py                    # Embedding, sentiment, keyword, emoji utils
│   ├── loader.py                       # JSON loaders for each file
│   ├── preprocessing.py                # Normalize casing, emoji, etc.
│
├── notebooks/
│   ├── eda_metrics_demo.ipynb          # Visualize user-level metrics
│   ├── belief_to_content_recs.ipynb    # Manually inspect FAISS recommendations
│
├── tests/
│   ├── test_metrics.py
│   ├── test_recommender.py
│
├── README.md
├── requirements.txt
└── .env.example

------
```

## Getting Started - Installation + Running the API + Tests

### Installation

The dependencies require some nesting environments - we're assuming an entirely local build that can be run on Macs with Intel silicon (this was written on a Macbook Pro 2017).

1. Install `Python@3.11` - e.g. `pyenv install 3.11`
2. Install `conda` - e.g. `brew install miniconda`
3. Using the `makefile`, simply run the following steps:
    a) `make conda-create` - Creates a `conda` environment using  - this will be called `conda-faiss-cpu` by default
    b) `make pipenv-install` - Installs pipenv within conda environment
    c) `make pipenv-deps` - Install pipenv dependencies from Pipfile
    d) `make shell` (Optional) - Launches an interactive shell of a pipenv environment, within a conda environment
    e) `make check-python` (Optional) - Checks that the appropriate Python version is being used

### Running the API

`make run-api` - Runs the API, including outputing all analytics and recommendations to a new JSON object - and, eventually, a Streamlit app

### Running Tests

`make test` - Runs tests on the entire codebase

### Other Features

`make streamlit` (In Progress) - Runs the Streamlit app for interactivity

------

## API

### `POST /evaluate`
Evaluate a conversation and return metrics + recommendations.

`make run-api`                  # in one terminal tab
`make send-sample-request`      # in another — only proceeds if server is healthy

**NOTE** - Launching this, using nested Conda + Pipenv environments, can be _very_ slow. It may be faster to launch into a properly setup shell using `make shell` (after the previous necessary steps), and then running the steps within `make run-api` and `make send-sample-request` manually. 

Within an interactive terminal, this process would be as follows. In your CLI, launch the FastAPI server by typing:

`uvicorn api.main:app --reload`

Then, after launching the API, send the request in a separate shell (with all dependencies) by typing:

`python scripts/send_sample_request.py`

OR you can type:

```
curl -X POST http://127.0.0.1:8000/evaluate \
  -H "Content-Type: application/json" \
  -d "@sample_conversation.json"
```

OR you can:

Stream it manually in `Swagger UI`
1. Open `http://127.0.0.1:8000/docs` or `http://localhost:8000/docs`
2. Click `POST /evaluate`
3. Paste one conversation (from conversations.json) into the request body
4. Click `"Try it out"`

### Input/Output Schemas

**Input**:

The general input format looks like this:

```json
{
  "ref_conversation_id": 42615,
  "conversation": [
    {
      "message": "I feel stuck lately.",
      "screen_name": "User822",
      "ref_conversation_id": 42615,
      "ref_user_id": 822,
      "transaction_datetime_utc": "2023-10-01T08:00:00Z"
    },
    ...
  ]
}
```

**Output**:

This schema defines what the `/evaluate` endpoint will return. It's structured to serve multiple teams:
A. Conversation valuation
B. StoryBot analysis
C. Content recommendation
D. Anomaly monitoring

```json
{
  "ref_conversation_id": 42615,
  "ref_user_id": 822,
  "evaluation_summary": {
    "conversation_value": {
      "round_count": 5,
      "avg_message_length": 94.2,
      "emoji_count": 3,
      "unique_word_ratio": 0.73,
      "sentiment_trajectory": {
        "start": 0.2,
        "end": 0.6,
        "delta": 0.4
      },
      "belief_shift_score": 0.35,
      "mood_volatility": 0.12,
      "engagement_score": 0.82
    },
    "storybot_metrics": {
      "avg_response_latency_secs": 2.3,
      "avg_sentiment_of_responses": 0.5,
      "avg_relevance_score": 0.78,
      "behavior_change_likelihood": 0.4,
      "user_reply_rate_after_bot_msg": 0.9
    },
    "user_identity_snapshot": {
      "beliefs": [
        {
          "topic": "confidence",
          "statement": "I lack confidence in group settings",
          "certainty": 0.84
        },
        {
          "topic": "purpose",
          "statement": "I want to make a meaningful impact",
          "certainty": 0.76
        }
      ],
      "identity_vector": {
        "confidence": -0.5,
        "purpose": 0.7,
        "social_belonging": 0.1
      }
    },
    "anomaly_signals": {
      "emoji_spike": false,
      "language_style_shift": true,
      "topic_drift": false,
      "prompt_injection_flagged": false,
      "mood_spike": true
    }
  },
  "recommended_posts": [
    {
      "post_id": 3830,
      "match_score": 0.87,
      "title": "How I regained confidence after social anxiety"
    },
    {
      "post_id": 4212,
      "match_score": 0.82,
      "title": "Finding purpose through small actions"
    }
  ]
}
```