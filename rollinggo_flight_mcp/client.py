from typing import Any, Dict, Optional

import httpx

from .config import get_api_base_url, get_api_prefix


async def request_api(method: str, endpoint: str, api_key: str, payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    url = f"{get_api_base_url()}{get_api_prefix()}{endpoint}"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json",
    }
    if method.upper() == "POST":
        headers["Content-Type"] = "application/json"

    try:
        async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
            response = await client.request(method.upper(), url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        body = ""
        try:
            body = e.response.text
        except Exception:
            pass
        raise Exception(f"HTTP请求失败 (状态码: {e.response.status_code})：{body or str(e)}")
    except httpx.HTTPError as e:
        raise Exception(f"HTTP请求失败：{str(e)}")
