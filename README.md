# Dida Flight MCP Server

> 🌐 [English](README.en.md) | **中文**

Dida 机票搜索 MCP Server。通过 FastMCP 为 AI Agent 和 MCP 客户端提供机场检索和航班查询能力。

当前版本只暴露 2 个工具：

- `searchAirports`：根据英文城市名、英文机场名或 IATA 代码搜索机场/城市信息。
- `searchFlights`：查询指定日期、航线、乘客人数和舱等的航班方案。

暂不实现 `checkFlightSeats` 和 `checkBaggageAllowance`。

## 安装依赖

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## 配置

默认上游 API 地址：

```text
https://mcp.rollinggo.cn
```

可通过环境变量覆盖：

```bash
set ROLLINGGO_API_BASE_URL=https://mcp.rollinggo.cn
```

HTTP 版本运行时从请求头读取 API Key。调用方需要传入以下任一请求头：

```http
Authorization: Bearer <your_api_key>
```

或：

```http
X-Secret-Key: <your_api_key>
```

## 启动

```bash
python server.py
```

默认监听：

```text
http://127.0.0.1:8000/mcp
```

## MCP 客户端配置示例

```json
{
  "mcpServers": {
    "dida-Flight-MCP": {
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

`keyword` 请优先传英文城市名、英文机场名或 IATA 代码，例如 `Hangzhou`、`Chengdu`、`HGH`、`CTU`。不建议优先传中文城市名。

输入：

```json
{
  "keyword": "Hangzhou"
}
```

上游端点：

```text
POST /api/mcp/airportsearch
```

## searchFlights

输入：

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

上游端点：

```text
POST /api/mcp/flightsearch
```

