from typing import Annotated

from fastmcp import FastMCP
from pydantic import Field

from ..auth import extract_api_key
from ..client import request_api


def register_airport_search_tool(mcp: FastMCP) -> None:
    @mcp.tool(name="searchAirports")
    async def search_airports(
        keyword: Annotated[
            str,
            Field(
                description="搜索关键字。请优先传英文城市名、英文机场名或 IATA 代码；不要优先传中文城市名。示例：Hangzhou、Chengdu、HGH、CTU。",
                min_length=1,
            ),
        ],
    ) -> dict:
        """
        根据英文城市名、英文机场名或 IATA 代码搜索机场/城市信息。

        Returns:
            dict: 上游原始 JSON，包含 message 与 airPortInformationList。
        """
        api_key = extract_api_key()
        return await request_api("POST", "/airportsearch", api_key, payload={"keyword": keyword})
