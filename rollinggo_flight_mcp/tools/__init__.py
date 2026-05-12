from fastmcp import FastMCP

from .airport_search import register_airport_search_tool
from .flight_search import register_flight_search_tool


def register_tools(mcp: FastMCP) -> None:
    register_airport_search_tool(mcp)
    register_flight_search_tool(mcp)
