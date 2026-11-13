# Connect your AI app to Agents4 Fitness

Agents4 Fitness runs an MCP server for coaches. MCP (Model Context Protocol) is the standard way an AI app
calls outside tools: once your app is connected, it can read your roster and make the changes you ask for, as
you.

- [Before you start](#before-you-start)
- [The server](#the-server)
- [Claude](#claude) · [ChatGPT](#chatgpt) · [Claude Code](#claude-code) · [Codex](#codex) ·
  [Cursor and VS Code](#cursor-and-vs-code) · [Your own code](#your-own-code)
- [Signing in and permissions](#signing-in-and-permissions)
- [API keys](#api-keys)
- [What the server offers](#what-the-server-offers)
- [Trouble connecting](#trouble-connecting)

## Before you start

- You need an Agents4 Fitness coach account on the **Architect** plan. To upgrade, open the Agents4 Fitness app
  and go to More → Connect ChatGPT & Claude → Upgrade to Architect.
- You sign in with the same username and password you use in the Agents4 Fitness app.
- Your AI app has to accept custom connectors or MCP servers. In Claude and ChatGPT that depends on your plan
  and, in a workspace, on what your admin allows.

## The server

| | |
|---|---|
| Server URL | `https://api.agents4.com/mcp/http` |
| Transport | Streamable HTTP |
| Sign-in | OAuth (the sign-in page opens in your browser), or an API key from the Agents4 Fitness app |
| Acts as | You, the signed-in coach. It reaches your own clients and agents and nobody else's |

The Agents4 Fitness app shows the same URL with a Copy button under More → Connect ChatGPT & Claude.

`https://api.agents4.com/mcp/claude` is the same server on a second address. The Claude Code plugin uses it.

## Claude

For claude.ai and the Claude desktop app.

1. Open Settings → Connectors → Add custom connector.
2. Name it Agents4 Fitness and paste the server URL. Leave the advanced OAuth fields empty.
3. Select Connect. The Agents4 Fitness sign-in page opens: sign in and approve.
4. In a chat, turn on Agents4 Fitness from the tools menu. Attach your program or ask a question.

## ChatGPT

1. Open Settings → Apps & Connectors → Advanced settings and turn on Developer mode.
2. Back in Apps & Connectors, select Create, name it Agents4 Fitness and paste the server URL.
3. Choose OAuth as the authentication, confirm you trust the app and select Create.
4. Sign in to Agents4 Fitness and approve. In a chat, add Agents4 Fitness from the + menu.

ChatGPT can hand a file you upload (PDF, spreadsheet, document, screenshots) straight to Agents4 Fitness, which
reads it there.

Claude and ChatGPT rename their settings menus from time to time. If a name differs, look for custom
connectors.

## Claude Code

### With the plugin (recommended)

The plugin adds the server and the seven [skills](skills.md).

```sh
claude plugin marketplace add agents4fitness/plugins
claude plugin install agents4-coach@agents4-fitness
```

Then sign in: in Claude Code run `/mcp`, choose `plugin:agents4-coach:agents4`, and pick **Authenticate**.

- **Check it:** ask "Check my Agents4 Fitness connection", or run `/agents4-coach:agents4-setup`.
- **Update later:** `claude plugin marketplace update agents4-fitness`, then
  `claude plugin update agents4-coach@agents4-fitness`.
- **Without a browser (SSH):** `claude mcp login plugin:agents4-coach:agents4 --no-browser`, then paste the
  redirect URL back when asked.
- **Scripts and CI:** set `AGENTS4_API_KEY` to an [API key](#api-keys) instead of signing in. The plugin sends it
  in the `X-Agents4-Key` header.
- If you started a sign-in and then switch to `AGENTS4_API_KEY`, run
  `claude mcp logout plugin:agents4-coach:agents4` first. Otherwise Claude Code keeps asking you to authenticate.
- `AGENTS4_MCP_URL` points the plugin at another server address (default `https://api.agents4.com/mcp/claude`).

### Without the plugin

You get the tools, without the skills.

```sh
# Sign in with your browser: afterwards run /mcp, choose agents4, pick Authenticate
claude mcp add --transport http agents4 https://api.agents4.com/mcp/http

# Or use an API key
claude mcp add --transport http agents4 https://api.agents4.com/mcp/http \
  --header "Authorization: Bearer $AGENTS4_API_KEY"
```

`claude mcp list` shows the server as connected, or as needing sign-in.

The same server in a project's `.mcp.json`, with the key read from your environment:

```json
{
  "mcpServers": {
    "agents4": {
      "type": "http",
      "url": "https://api.agents4.com/mcp/http",
      "headers": { "Authorization": "Bearer ${AGENTS4_API_KEY}" }
    }
  }
}
```

## Codex

```sh
codex plugin marketplace add agents4fitness/plugins
codex plugin add agents4-coach@agents4-fitness
```

Codex asks you to sign in when the plugin is installed. To sign in later, run `codex mcp login agents4`.

- The Codex plugin connects to `https://api.agents4.com/mcp/http?profile=coach-compact`. Codex shows a plugin's
  tools only while their definitions fit a size budget, and this profile lists the tools the skills use. The rest
  stay reachable (see [tool profiles](#tool-profiles)).
- On Windows, Codex needs its Windows sandbox enabled (`[windows] sandbox = "elevated"`) to read skill files.

## Cursor and VS Code

Code editors connect with an API key. In the Agents4 Fitness app, open More → Connect ChatGPT & Claude →
Generate API Key: the app shows a ready-made block for each editor with your key filled in.

Cursor, in `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "agents4": {
      "url": "https://api.agents4.com/mcp/http",
      "headers": { "Authorization": "Bearer mcp_sk_your_key" }
    }
  }
}
```

VS Code, in `.vscode/mcp.json`:

```json
{
  "servers": {
    "agents4": {
      "type": "http",
      "url": "https://api.agents4.com/mcp/http",
      "headers": { "Authorization": "Bearer mcp_sk_your_key" }
    }
  }
}
```

A file with a key in it stays out of version control.

## Your own code

Any MCP client that speaks Streamable HTTP can connect. Send your API key as a bearer token.

### Python

[examples/python/weekly_numbers.py](../examples/python/weekly_numbers.py) lists the tools and reads your roster
and this week's numbers. It is read-only and needs only Python's standard library.

With the MCP Python SDK (`pip install mcp`, version 2):

```python
import asyncio
import json
import os

import httpx2
from mcp import Client
from mcp.client.streamable_http import streamable_http_client

URL = "https://api.agents4.com/mcp/http"
HEADERS = {"Authorization": f"Bearer {os.environ['AGENTS4_API_KEY']}"}


async def main():
    async with httpx2.AsyncClient(headers=HEADERS, timeout=httpx2.Timeout(30, read=300)) as http:
        async with Client(streamable_http_client(URL, http_client=http)) as client:
            tools = await client.list_tools()
            print(len(tools.tools), "tools")
            result = await client.call_tool("coach_list_clients", {})
            roster = json.loads(result.content[0].text)
            print(roster["count"], "clients,", roster["needs_attention_count"], "need attention")


asyncio.run(main())
```

Version 1 of the SDK names these differently: `streamablehttp_client(URL, headers=HEADERS)` with
`ClientSession`.

### Plain HTTP

The server is stateless: one POST per request, and a tool call needs no session.

```sh
curl -s https://api.agents4.com/mcp/http \
  -H "Authorization: Bearer $AGENTS4_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"coach_list_clients","arguments":{}}}'
```

Every tool answers with one text block that holds JSON:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [
      { "type": "text", "text": "{\"success\": true, \"cohort\": \"whole roster\", \"count\": 0, \"needs_attention_count\": 0, \"clients\": [], \"truncated\": false}" }
    ],
    "isError": false
  }
}
```

`tools/list` returns every tool with its input schema, and `initialize` returns the server's own guidance for
the model in `instructions`. Pass that guidance to your model: it says which tool to use for which request and
when to preview a change first.

### OAuth, for an app that signs coaches in

The server follows the MCP authorization flow, so a client that implements it needs no setup on our side.

1. A request without credentials gets `401` and a `WWW-Authenticate` header that points at the server's metadata:
   `https://api.agents4.com/.well-known/oauth-protected-resource`.
2. That document names the authorization server, `https://api.agents4.com/mcp/oauth`. Its metadata lists the
   endpoints: `/authorize`, `/token`, `/register` and `/revoke`.
3. Register your client at the registration endpoint (dynamic client registration), then run the authorization
   code flow with PKCE (`S256`). The coach signs in and approves on app.agents4fitness.com.
4. Send the access token as `Authorization: Bearer …`.

| | |
|---|---|
| Scopes | `mcp:read` for tools that only read; `mcp:write` for tools that change something |
| Access token | Lasts one hour |
| Refresh token | Replaced each time it is used. Reusing an old one ends the connection |
| Connection | Lasts 30 days, then the coach signs in again. It ends sooner if the coach disconnects the app (at once), changes their password, or their Architect plan ends |

### Tool profiles

Add `?profile=<name>` to the server URL to choose which tools one connection lists. A narrower profile also
narrows what that connection can run. A profile never adds rights: the coach's sign-in decides those.

| Profile | Lists |
|---|---|
| `coach` (default) | The everyday coaching tools, sized for chat apps, plus three tools that find and run the rest |
| `coach-compact` | A shorter list for apps with a tool budget (the Codex plugin uses it), plus the same three |
| `agent-builder`, `clients`, `planning`, `marketplace-creator`, `auto-review` | Every tool in that one area |
| `full` | Every tool. Too many for a chat app; meant for your own tooling |

An unknown profile is refused with `400` and the list of valid names.

## Signing in and permissions

- The sign-in page is on [app.agents4fitness.com](https://app.agents4fitness.com). Check the address before you
  type your password.
- Sign in with your coach account. If you are signed in as a client, the page asks you to switch.
- The approval screen names the app that is asking and where it will return you. Only connect an app you
  recognize.
- You choose what the app may do: read your agents, client records, check-ins and plans, and (if you leave it
  on) create and update agents, change plans and take other coaching actions. If you turn changes off, the
  tools that change anything are not offered to that app at all.
- A sign-in page is valid for 10 minutes. A connection lasts 30 days.
- To disconnect an app, open More → Connect ChatGPT & Claude in the Agents4 Fitness app and select Disconnect
  next to it. It loses access straight away.

## API keys

For code editors, scripts and your own code.

- **Create one:** Agents4 Fitness app → More → Connect ChatGPT & Claude → Generate API Key. Keys start with
  `mcp_sk_`.
- **Send it** as `Authorization: Bearer mcp_sk_…`.
- **It acts as you.** Anyone who holds it can read your clients' data and change their plans. Keep it in an
  environment variable or a secret store, never in a URL, a chat, or a file you commit.
- **Revoke it** in the app, on the API Keys screen (Manage API keys, on the same screen where you created it).

## What the server offers

The default tool list, by job. `tools/list` is the authority: it has every tool's description and input schema.

| Job | Tools |
|---|---|
| See your clients | `coach_list_clients`, `coach_client_summary`, `coach_cohort_report`, `coach_get_client_plan` |
| Change plans | `coach_edit_workouts`, `coach_edit_nutrition`, `coach_edit_program`, `coach_revert_client_program`, `planning_set_client_program` |
| Bring clients over | `coach_add_clients`, `coach_set_client_plan` |
| Message clients | `coach_message_clients` |
| Groups | `roster_list_groups`, `roster_create_group`, `roster_add_to_group`, `roster_remove_from_group` |
| Build your agent | `agent_builder_import_plan`, `agent_builder_import_plan_file` |
| Shape, test and deploy your agent | `agents_list_agents`, `agents_get_agent_config`, `agents_manage_agent_config`, `agents_set_agent_workout_days`, `agents_set_agent_nutrition_days`, `agents_set_agent_guardrails`, `agents_test_agent_interaction`, `agents_deploy_agent`, `agents_assign_agent_to_clients`, and more |
| Exercise, food and knowledge library | `library_search_exercises`, `library_add_exercise`, `library_search_foods`, `library_add_food`, `library_search_knowledge`, `library_ingest_content` |
| Everything else | `platform_find_tools` (search), `platform_read_tool` (run a read-only tool), `platform_call_tool` (run a tool that changes something) |

How the tools behave:

- **A client is named the way you would name them:** a name, an email address or a phone number. If a name
  matches several clients, the answer lists them so you can say which.
- **Many clients at once** are a cohort: a group, an agent's clients, a list of names, or everyone.
- **`dry_run: true` previews** a change, a message or a set of invitations without making it.
- **Every change reports what the client now sees** in their app, and names anything that did not take.
- **Tools are labelled** for your AI app: read-only tools, tools that change or delete something, and tools that
  reach outside your account (an invitation email). Apps use those labels to decide when to ask you first.

## Trouble connecting

| You see | What to do |
|---|---|
| "An active Architect plan or MCP subscription is required" | Your account is not on Architect. Upgrade in the app, then start the connection again from your AI app |
| "This is a client account" | Select Switch account and sign in with your coach username and password |
| "This connection request expired" | The sign-in page is valid for 10 minutes. Start again from your AI app |
| Asked to sign in again | A connection lasts 30 days, and ends sooner if your Architect plan ends or you change your password. Sign in again the same way |
| Forgot your password | Use Forgot password on the sign-in page. Changing your password disconnects your AI apps, so connect them again afterwards |
| `401` with "Sign in to your Agents4 Fitness coach account…" from your own code | The key or token is missing, mistyped, revoked or expired |
| Claude Code keeps asking you to authenticate after you set `AGENTS4_API_KEY` | Run `claude mcp logout plugin:agents4-coach:agents4` |
| Your AI app says it cannot make a change, or that a feature is not available on your connection | The connection is probably read-only, so the tools that change anything are hidden. Disconnect the app in the Agents4 Fitness app, connect again and allow changes |

Still stuck: support@agents4.com.
