"""Connect to Agents4 Fitness from your own code: read your roster and this week's numbers.

Read-only: it calls two tools that only read. It needs nothing but Python's standard library.

    export AGENTS4_API_KEY=mcp_sk_...     # Agents4 Fitness app: More -> Connect ChatGPT & Claude -> Generate API Key
    python weekly_numbers.py

The key acts as you, the coach. Keep it out of source control and out of URLs.
"""
import json
import os
import urllib.error
import urllib.request

URL = os.environ.get("AGENTS4_MCP_URL", "https://api.agents4.com/mcp/http")
KEY = os.environ["AGENTS4_API_KEY"]


def rpc(method, params=None):
    """Send one request to the MCP server and return its result."""
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params or {}}).encode()
    request = urllib.request.Request(URL, data=body, headers={
        "Authorization": f"Bearer {KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
    })
    try:
        with urllib.request.urlopen(request, timeout=300) as response:
            raw = response.read().decode()
    except urllib.error.HTTPError as error:
        raise SystemExit(f"{error.code}: {error.read().decode()}")
    if raw.startswith(("event:", "data:")):  # the same message, delivered as a server-sent event
        raw = "\n".join(line[5:].strip() for line in raw.splitlines() if line.startswith("data:"))
    message = json.loads(raw)
    if "error" in message:
        raise SystemExit(f"The server refused {method}: {message['error']}")
    return message["result"]


def call(tool, arguments=None):
    """Run one tool and return its answer. Every Agents4 Fitness tool answers with JSON in a text block."""
    result = rpc("tools/call", {"name": tool, "arguments": arguments or {}})
    text = "".join(block["text"] for block in result["content"] if block["type"] == "text")
    if result.get("isError"):
        raise SystemExit(f"{tool} failed: {text}")
    return json.loads(text)


def main():
    tools = rpc("tools/list")["tools"]
    print(f"Connected: {len(tools)} tools.")

    roster = call("coach_list_clients")
    print(f"{roster['count']} clients, {roster['needs_attention_count']} need attention.")

    week = call("coach_cohort_report", {"days": 7})
    print(json.dumps(week.get("summary", week), indent=2))


if __name__ == "__main__":
    main()
