import re
from typing import Annotated, Literal, Optional

from fastmcp import FastMCP
from pydantic import Field

from ..auth import extract_api_key
from ..client import request_api

CabinGrade = Literal["ECONOMY", "PREMIUM_ECONOMY", "BUSINESS", "FIRST"]
TripType = Literal["ONE_WAY", "ROUND_TRIP"]

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def _validate_date(value: str, field_name: str) -> None:
    if not DATE_RE.fullmatch(value):
        raise ValueError(f"{field_name} 必须使用 YYYY-MM-DD 格式")


def register_flight_search_tool(mcp: FastMCP) -> None:
    @mcp.tool(name="searchFlights")
    async def search_flights(
        adultNumber: Annotated[int, Field(description="成人数量，必须大于等于 1。", ge=1)],
        childNumber: Annotated[int, Field(description="儿童数量，没有儿童时传 0。", ge=0)],
        cabinGrade: Annotated[
            CabinGrade,
            Field(description="舱等偏好。可选值：ECONOMY、PREMIUM_ECONOMY、BUSINESS、FIRST。"),
        ],
        fromDate: Annotated[str, Field(description="出发日期，格式 YYYY-MM-DD。")],
        tripType: Annotated[TripType, Field(description="行程类型。可选值：ONE_WAY、ROUND_TRIP。")],
        retDate: Annotated[Optional[str], Field(description="返程日期，格式 YYYY-MM-DD。tripType=ROUND_TRIP 时必填。")] = None,
        fromCity: Annotated[Optional[str], Field(description="出发城市代码，与 fromAirport 二选一。示例：HGH。")] = None,
        fromAirport: Annotated[Optional[str], Field(description="出发机场代码，与 fromCity 二选一。示例：HGH。")] = None,
        toCity: Annotated[Optional[str], Field(description="到达城市代码，与 toAirport 二选一。示例：CTU。")] = None,
        toAirport: Annotated[Optional[str], Field(description="到达机场代码，与 toCity 二选一。示例：TFU。")] = None,
    ) -> dict:
        """
        查询指定日期、航线、乘客人数和舱等的航班方案。

        Returns:
            dict: 上游原始 JSON，包含 message 与 flightInformationList。
        """
        _validate_date(fromDate, "fromDate")
        if retDate:
            _validate_date(retDate, "retDate")
        if tripType == "ROUND_TRIP" and not retDate:
            raise ValueError("tripType=ROUND_TRIP 时必须传 retDate")
        if not (fromCity or fromAirport):
            raise ValueError("fromCity 与 fromAirport 必须至少传一个")
        if not (toCity or toAirport):
            raise ValueError("toCity 与 toAirport 必须至少传一个")

        payload = {
            "adultNumber": adultNumber,
            "childNumber": childNumber,
            "cabinGrade": cabinGrade,
            "fromDate": fromDate,
            "tripType": tripType,
        }

        if retDate:
            payload["retDate"] = retDate
        if fromCity:
            payload["fromCity"] = fromCity
        if fromAirport:
            payload["fromAirport"] = fromAirport
        if toCity:
            payload["toCity"] = toCity
        if toAirport:
            payload["toAirport"] = toAirport

        api_key = extract_api_key()
        return await request_api("POST", "/flightsearch", api_key, payload=payload)
