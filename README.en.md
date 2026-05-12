# Dida Flight MCP Server

> 🌐 **English** | [中文](README.md)

Dida Flight Search MCP Server. Provides airport search and flight query capabilities for AI Agents and MCP clients via FastMCP.

Currently exposes 2 tools:

- `searchAirports` — Search airport/city info by English city name, English airport name, or IATA code.
- `searchFlights` — Query flight options by date, route, passenger count, and cabin class.

`checkFlightSeats` and `checkBaggageAllowance` are not yet implemented.

## Installation

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Configuration

Default upstream API address:

```text
https://mcp.Dida.cn
```

Override via environment variable:

```bash
set ROLLINGGO_API_BASE_URL=https://mcp.rollinggo.cn
```

The HTTP server reads the API Key from request headers. Pass one of the following:

```http
Authorization: Bearer <your_api_key>
```

or:

```http
X-Secret-Key: <your_api_key>
```

## Start

```bash
python server.py
```

Default endpoint:

```text
http://127.0.0.1:8000/mcp
```

## MCP Client Configuration

```json
{
  "mcpServers": {
    "Dida-Flight-MCP": {
      "url": "http://127.0.0.1:8000/mcp",
      "type": "streamable_http",
      "headers": {
        "Authorization": "Bearer YOUR_API_KEY"
      }
    }
  }
}
```

## searchAirports

For the `keyword` parameter, prefer English city names, English airport names, or IATA codes (e.g. `Hangzhou`, `Chengdu`, `HGH`, `CTU`). Chinese city names are not recommended as primary input.

Input:

```json
{
  "keyword": "Hangzhou"
}
```

Upstream endpoint:

```text
POST /api/mcp/airportsearch
```

## searchFlights

Input:

```json
{
  "adultNumber": 1,
  "childNumber": 0,
  "cabinGrade": "ECONOMY",
  "fromCity": "HGH",
  "toCity": "CTU",
  "fromDate": "2026-05-01",
  "tripType": "ONE_WAY"
}
```

Upstream endpoint:

```text
POST /api/mcp/flightsearch
```
