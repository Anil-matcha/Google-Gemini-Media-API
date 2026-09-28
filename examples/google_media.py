"""Submit and poll Google media generation requests via Muapi.

Usage: MUAPI_API_KEY=... python examples/google_media.py [nano|imagen|veo|omni|tts]
This example uses only the Python standard library.
"""

import json
import os
import sys
import time
from urllib.error import HTTPError
from urllib.request import Request, urlopen

BASE_URL = "https://api.muapi.ai/api/v1"
REQUESTS = {
    "nano": ("nano-banana", {"prompt": "A glass greenhouse on a mossy hillside at sunrise", "aspect_ratio": "1:1"}),
    "imagen": ("google-imagen4", {"prompt": "A glass greenhouse at sunrise, editorial photography", "aspect_ratio": "16:9", "num_images": 1}),
    "veo": ("veo3.1-text-to-video", {"prompt": "A cinematic sunrise over a misty mountain valley", "duration": 8}),
    "omni": ("gemini-omni-text-to-video", {"prompt": "A chef explains a recipe in a warm studio kitchen", "resolution": "1080p", "duration": 8, "aspect_ratio": "16:9"}),
    "tts": ("gemini-3-8-flash-tts", {
        "speakers": [{"speaker_id": "Speaker 1", "voice_name": "Kore", "accent": "Neutral", "style": "Empathetic", "pace": "Natural"}],
        "dialogue_turns": [{"speaker_id": "Speaker 1", "text": "Welcome to the show."}],
    }),
}


def call(url, key, payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    headers = {"x-api-key": key}
    if payload is not None:
        headers["Content-Type"] = "application/json"
    req = Request(url, data=data, headers=headers, method="POST" if payload is not None else "GET")
    try:
        with urlopen(req, timeout=60) as response:
            return json.load(response)
    except HTTPError as error:
        detail = error.read().decode(errors="replace")
        raise RuntimeError(f"Muapi returned HTTP {error.code}: {detail}") from error


def main():
    key = os.environ.get("MUAPI_API_KEY")
    if not key:
        raise SystemExit("Set MUAPI_API_KEY in your environment.")
    name = sys.argv[1] if len(sys.argv) > 1 else "nano"
    if name not in REQUESTS:
        raise SystemExit(f"Choose one of: {', '.join(REQUESTS)}")
    endpoint, payload = REQUESTS[name]
    submitted = call(f"{BASE_URL}/{endpoint}", key, payload)
    request_id = submitted.get("request_id")
    if not request_id:
        print(json.dumps(submitted, indent=2))
        return
    print(f"Submitted {endpoint}; request_id={request_id}")
    result_url = f"{BASE_URL}/predictions/{request_id}/result"
    while True:
        result = call(result_url, key)
        print(json.dumps(result, indent=2))
        status = str(result.get("status", "")).lower()
        if status in {"completed", "failed", "error", "cancelled"}:
            break
        time.sleep(3)


if __name__ == "__main__":
    main()
