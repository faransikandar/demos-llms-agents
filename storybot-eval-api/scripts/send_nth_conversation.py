import json
import requests
import sys

CONVO_FILE = "data/conversations.json"
API_URL = "http://127.0.0.1:8000/evaluate"

# Use Nth item from CLI (default to 0)
n = int(sys.argv[1]) if len(sys.argv) > 1 else 0

# Load file and extract Nth conversation
with open(CONVO_FILE) as f:
    conversations = json.load(f)

try:
    payload = conversations[n]
except IndexError:
    print(f"❌ Conversation #{n} not found. File has {len(conversations)} items.")
    sys.exit(1)

# Send the POST request
response = requests.post(API_URL, json=payload)

# Show result
print(f"✅ Status: {response.status_code}")
try:
    print(json.dumps(response.json(), indent=2))
except Exception:
    print(response.text)