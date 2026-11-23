import requests


OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
TIMEOUT_SECONDS = 30


def ask_llm(messages: list[dict], model: str, api_key: str) -> str:
    payload = {
        "model": model,
        "messages": messages,
        "max_tokens": 1000,
    }
    try:
        response = requests.post(
            url=OPENROUTER_URL,
            json=payload,
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        data = response.json()
        content = data["choices"][0]["message"].get("content")
    except requests.exceptions.Timeout as e:
        raise RuntimeError(
            f"OpenRouter did not respond within {TIMEOUT_SECONDS} seconds (model: {model})"
        ) from e
    except requests.exceptions.HTTPError as e:
        raise RuntimeError(
            f"OpenRouter returned HTTP {e.response.status_code} for model {model}: {e.response.text[:200]}"
        ) from e
    except requests.exceptions.JSONDecodeError as e:
        raise RuntimeError(f"OpenRouter returned invalid JSON (model: {model})") from e
    except requests.exceptions.RequestException as e:
        raise RuntimeError(
            f"Could not connect to OpenRouter ({type(e).__name__})"
        ) from e
    except (KeyError, IndexError, TypeError) as e:
        raise RuntimeError(
            f"Unexpected response format from OpenRouter (model: {model}, {type(e).__name__})"
        ) from e
    if not content:
        raise RuntimeError(f"Model {model} returned an empty answer")
    return content
