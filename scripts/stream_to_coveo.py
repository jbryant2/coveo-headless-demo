import json
import requests
import urllib.parse
import time
import re

# -------------------------------
# CONFIGURATION
# -------------------------------
ORG_ID = "ptxefndmz5chilx6kh4kv2xsfha"
SOURCE_ID = "ptxefndmz5chilx6kh4kv2xsfha-q7fxv4st5xz2cyq2pb244uckqi"
API_KEY = "xxfb557a4b-9f67-40a9-870a-fe9dfe622029"

INPUT_JSON = "data/products-1000.json"

BASE_URL = (
    f"https://api.cloud.coveo.com/push/v1/"
    f"organizations/{ORG_ID}/sources/{SOURCE_ID}/documents"
)

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# -------------------------------
# HELPERS
# -------------------------------
def make_safe_id(value: str) -> str:
    """
    Create a URL-safe, Coveo-safe document ID.
    """
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9_-]", "-", value)
    return value[:200]  

# -------------------------------
# LOAD DATA
# -------------------------------
with open(INPUT_JSON, "r", encoding="utf-8") as f:
    items = json.load(f)

print(f"Pushing {len(items)} documents to Coveo...")

# -------------------------------
# PUSH DOCUMENTS
# -------------------------------
success = 0
failures = 0

for index, item in enumerate(items, start=1):
    # Prefer a stable ID if you have one
    raw_id = str(item.get("id") or item.get("title") or f"item-{index}")
    safe_id = make_safe_id(raw_id)

    # Coveo expects URL-encoded documentId
    document_id = f"file://menu/{safe_id}.json"
    encoded_id = urllib.parse.quote(document_id, safe="")

    url = f"{BASE_URL}?documentId={encoded_id}"

    document = {
        "title": item.get("title") or item.get("name"),
        "fileExtension": ".json",
        "data": json.dumps(item)
    }

    response = requests.put(url, headers=HEADERS, json=document)

    if response.status_code in (200, 201, 202):
        success += 1
        print(f"[{index}/{len(items)}] Indexed: {document['title']}")
    else:
        failures += 1
        print(
            f"[{index}/{len(items)}] Failed: {document.get('title')} | "
            f"{response.status_code} {response.text}"
        )

    time.sleep(0.05)

print("\Push complete")
print(f"Success: {success}")
print(f"Failures: {failures}")
