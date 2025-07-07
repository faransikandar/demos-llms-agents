import json
import requests
import sys

API_URL = "http://127.0.0.1:8000"
HEALTH_URL = f"{API_URL}/healthz"
EVAL_URL = f"{API_URL}/evaluate"

# Health check
try:
    r = requests.get(HEALTH_URL)
    if r.status_code != 200:
        print("❌ API is not healthy:", r.status_code)
        sys.exit(1)
except requests.exceptions.ConnectionError:
    print("❌ Cannot connect to FastAPI server. Did you run `make run-api`?")
    sys.exit(1)

# Load a sample
with open("data/conversations.json") as f:
    conversations = json.load(f)
sample = conversations[0]

# Save locally (optional)
with open("data/sample_conversation.json", "w") as f:
    json.dump(sample, f, indent=2)

# POST request
res = requests.post(EVAL_URL, json=sample)

print(f"✅ Response [{res.status_code}]:")
try:
    print(json.dumps(res.json(), indent=2))
except Exception:
    print("⚠️ Could not parse JSON:")
    print(res.text)