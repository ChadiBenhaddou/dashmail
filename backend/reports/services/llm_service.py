import json
import os
import re
import time

import openai


def call_llm(system_prompt, user_prompt, max_retries=3):
    client = openai.OpenAI(
        api_key=os.getenv("LLM_API_KEY", "missing"),
        base_url=os.getenv("LLM_API_BASE_URL", "https://api.openai.com/v1"),
    )
    model = os.getenv("LLM_MODEL", "gpt-4o")

    last_exc = None
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.3,
                response_format={"type": "json_object"},
            )
            raw = response.choices[0].message.content
            return _parse_json(raw)
        except openai.APITimeoutError as exc:
            last_exc = exc
            time.sleep(2 ** attempt)
        except openai.APIStatusError as exc:
            last_exc = exc
            if exc.status_code >= 500:
                time.sleep(2 ** attempt)
            else:
                raise
        except (json.JSONDecodeError, ValueError) as exc:
            last_exc = exc
            time.sleep(2 ** attempt)

    raise last_exc


def _parse_json(raw_text):
    raw_text = raw_text.strip()
    try:
        return json.loads(raw_text)
    except json.JSONDecodeError:
        pass

    match = re.search(r"\{.*\}", raw_text, re.DOTALL)
    if match:
        return json.loads(match.group())

    raise ValueError(f"Could not parse JSON from LLM response: {raw_text[:200]}")
