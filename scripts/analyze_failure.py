#!/usr/bin/env python3
"""
CI Failure Analyzer - reads log from stdin, sends to Gemini, prints analysis.
"""
import sys
import os
import json
import urllib.request
import urllib.error

def analyze_failure(log_text: str) -> str:
    api_key = os.environ.get("GEMINI_API_KEY", "")
    if not api_key:
        return "ERROR: GEMINI_API_KEY not set."

    prompt = f"""You are a senior DevOps engineer reviewing a CI/CD failure log.

Analyze the following GitHub Actions failure log and provide:

1. **Root cause** — What exactly failed and why (be specific: file, line, error type)
2. **Failed step** — Which workflow step broke
3. **Fix** — Concrete code change or command to resolve it
4. **Prevention** — One suggestion to catch this earlier

Keep your analysis under 300 words. Be direct, no fluff.

--- FAILURE LOG START ---
{log_text[:8000]}
--- FAILURE LOG END ---"""

    payload = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}]
    }).encode("utf-8")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"

    req = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"}
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read())
            return data["candidates"][0]["content"]["parts"][0]["text"]
    except urllib.error.HTTPError as e:
        return f"API error {e.code}: {e.read().decode()}"
    except Exception as e:
        return f"Unexpected error: {e}"

if __name__ == "__main__":
    log = sys.stdin.read().strip()
    if not log:
        print("No log input received.")
        sys.exit(1)
    print(analyze_failure(log))
