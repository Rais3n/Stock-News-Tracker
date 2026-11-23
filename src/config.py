import os 


def load_api_key(name: str) -> str:
    api_key = os.getenv(name)
    if not api_key:
        raise RuntimeError(f"Environment variable {name} is missing or empty")
    return api_key