# Dida Flight MCP Server

`Dida-Flight-MCP` is a flight ticketing service built on the MCP standard, providing airport search and flight query capabilities for AI Agents and MCP clients. (Last updated: 2026-04-24)

## Online Endpoint

- **MCP URL**: `https://mcp.rollinggo.cn/mcp/flight`
- **Transport**: `streamable_http`
- **Current online configuration**: No Bearer Token required on the client side. For private deployments or business channels requiring an API Key, configure according to your actual environment.

## Tools

The Flight MCP exposes 2 available tools:

1. **`searchAirports`**: Search for airport/city information by keywords such as city name, airport name, or airport code
2. **`searchFlights`**: Query flight lists and prices for specified dates, routes, passenger counts, and cabin classes

## Recommended Workflow

1. If the user only provides a natural language city name, first call `searchAirports` to get available `cityCode` or `airportCode`.
2. Call `searchFlights` to query flight lists, segment information, and prices.
3. Prices and inventory are subject to real-time changes from suppliers; it is recommended to re-query before displaying to users or placing orders.

---

## 1) searchAirports

Search for airports, cities, or related transportation hub information by keywords.

### Input Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `keyword` | string | ✅ | Search keyword, such as city name, airport name, or airport code. Examples: `Hangzhou`, `HGH`, `Chengdu`, `CTU` |

### Output Structure

```json
{
  "message": "Airport search successful",
  "airPortInformationList": [
    {
      "airportCode": "TFU",
      "airportName": "Tianfu Airport",
      "cityCode": "CTU",
      "cityName": "Chengdu",
      "countryCode": "CN",
      "countryName": "China",
      "timeZone": "+08:00"
    }
  ]
}

```

### Field Descriptions

- **`airportCode`**: Can be used as `searchFlights.fromAirport` / `searchFlights.toAirport`.
- **`cityCode`**: Can be used as `searchFlights.fromCity` / `searchFlights.toCity`.
- Search results are returned by the supplier and may include city-related transportation hubs; clients should perform secondary filtering using `cityCode`, `airportCode`, and `countryCode`.
- When there are no matching results, `airPortInformationList` may be an empty array.

---

## 2) searchFlights

Query flight options for specified dates, routes, passenger counts, and cabin classes.

### Input Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `adultNumber` | integer | ✅ | Number of adults |
| `childNumber` | integer | ✅ | Number of children. Pass `0` if no children |
| `cabinGrade` | string | ✅ | Cabin class: `ECONOMY`, `PREMIUM_ECONOMY`, `BUSINESS`, `FIRST` |
| `tripType` | string | ✅ | Trip type: `ONE_WAY`, `ROUND_TRIP` |
| `fromDate` | string | ✅ | Departure date (format: `YYYY-MM-DD`) |
| `retDate` | string | ✅ (for round-trip) | Return date, used when `tripType=ROUND_TRIP` |
| `fromCity` | string | ❌ | Departure city code (choose one with `fromAirport`) |
| `fromAirport` | string | ❌ | Departure airport code (choose one with `fromCity`) |
| `toCity` | string | ❌ | Arrival city code (choose one with `toAirport`) |
| `toAirport` | string | ❌ | Arrival airport code (choose one with `toCity`) |

### Output Structure

```json
{
  "message": "Flight search successful",
  "flightInformationList": [
    {
      "routingId": "...",
      "totalAdultPrice": 1813.0,
      "totalChildPrice": 0.0,
      "currency": "CNY",
      "fromSmartValueScore": 95.0,
      "validatingCarrier": "3U",
      "fromSegments": [
        {
          "flightNumber": "3U8916",
          "depTime": "2026-05-01T17:50:00",
          "arrTime": "2026-05-01T21:00:00",
          "depAirport": "HGH",
          "arrAirport": "CTU",
          "duration": "190",
          "stopCities": ""
        }
      ],
      "retSegments": []
    }
  ]
}

```

### Field Descriptions

| Field | Description |
|-------|-------------|
| `routingId` | Unique route ID identifying this flight option |
| `totalAdultPrice` | Total adult price (currency in `currency`) |
| `totalChildPrice` | Total child price (currency in `currency`) |
| `fromSmartValueScore` | Comprehensive recommendation score (higher = better) |
| `validatingCarrier` | Ticketing/carrier airline code |
| `fromSegments` | Outbound flight segments (1 for direct, multiple for connections) |
| `retSegments` | Return flight segments (empty for one-way) |
| `duration` | Flight duration in minutes (string) |
| `stopCities` | Connecting city; empty if direct |

### Notes

- Prices and inventory are **real-time**. Recommend noting "subject to final booking confirmation".
- Same city may have multiple airports. Use `fromAirport` / `toAirport` for precise filtering.
- If user only says "Chengdu" or "Shanghai", use `fromCity` / `toCity` to get results covering all airports.

---

## Usage Examples

### Example 1: Search Airport/City Code

```json
{
  "keyword": "CTU"
}
```

### Example 2: Hangzhou → Chengdu, One-way, Labor Day, 1 Adult, Economy

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

### Example 3: Hangzhou ↔ Chengdu Round-trip, 1 Adult, Economy

```json
{
  "adultNumber": 1,
  "childNumber": 0,
  "cabinGrade": "ECONOMY",
  "fromCity": "HGH",
  "toCity": "CTU",
  "fromDate": "2026-05-01",
  "retDate": "2026-05-05",
  "tripType": "ROUND_TRIP"
}

```

---

## MCP Client Configuration Example

Different MCP clients may have slightly varying field names. The core is configuring the `streamable_http` type and the online MCP URL.

### Basic Configuration

```json
{
  "mcpServers": {
    "dida-Flight-MCP": {
      "url": "https://mcp.rollinggo.cn/mcp/flight",
      "type": "streamable_http"
    }
  }
}


```

### With Explicit Headers

```json
{
  "mcpServers": {
    "dida-Flight-MCP": {
      "url": "https://mcp.rollinggo.cn/mcp/flight",
      "type": "streamable_http",
      "headers": {
        "Authorization": "Bearer YOUR_API_KEY"
      }
    }
  }
}

```

---

## Integration Tips

- **Determine trip type first**: One-way or round-trip? Round-trips require `retDate`.
- **City name → Airport code**: Use `searchAirports` first, or use known IATA codes directly.
- **City code vs Airport code**: City codes are for broad searches; airport codes are for precise filtering.
- **Display recommendation**: Show at minimum: flight number, departure/arrival times, airports, total price, currency, and connection info.

---

## Related Links
- **API Key Application**: https://rollinggo.store/apply
- **MCP Standard**: https://modelcontextprotocol.io/
