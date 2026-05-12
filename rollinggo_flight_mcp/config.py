import os


def get_api_base_url() -> str:
    return os.getenv("ROLLINGGO_API_BASE_URL", "https://mcp.rollinggo.cn").rstrip("/")


def get_api_prefix() -> str:
    return os.getenv("ROLLINGGO_API_PREFIX", "/mcp").rstrip("/")
