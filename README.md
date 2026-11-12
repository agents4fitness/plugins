# Agents4 Fitness Coach plugins

Run your Agents4 Fitness coaching business from Claude, Codex or ChatGPT:
- weekly client reviews and one-client deep dives;
- workout and nutrition changes for one client, a group, or everyone on your program;
- messages to clients;
- your AI coaching agent, built from your own plan (PDF, spreadsheet, doc or screenshots);
- your existing clients moved over from another app: your client list, then each client's current workouts and
  nutrition, ready for them when they join.

Clients see every change in their Agents4 Fitness app.

**You need** an Agents4 Fitness coach account on the **Architect** plan.

| Folder | For |
|---|---|
| `claude/agents4-coach` | Claude Code |
| `openai/agents4-coach` | Codex (and ChatGPT) |
| `skills/` | The skills both plugins ship (edit here, then run `build.py`) |

This folder is one marketplace, named `agents4-fitness`, for both hosts:
- Claude Code reads `.claude-plugin/marketplace.json`.
- Codex reads `.agents/plugins/marketplace.json`.

## Install

The plugins live at [github.com/agents4fitness/plugins](https://github.com/agents4fitness/plugins).

### Claude Code

```sh
claude plugin marketplace add agents4fitness/plugins
claude plugin install agents4-coach@agents4-fitness
```

Then sign in: in Claude Code run `/mcp`, choose `plugin:agents4-coach:agents4`, and pick **Authenticate**.

- For scripts and CI, set `AGENTS4_API_KEY` to an MCP key from the Agents4 Fitness app instead; the plugin sends
  it in the `X-Agents4-Key` header.
- `AGENTS4_MCP_URL` points the plugin at another server (default `https://api.agents4.com/mcp/claude`).
- If you started a sign-in and then switch to `AGENTS4_API_KEY`, run
  `claude mcp logout plugin:agents4-coach:agents4` first. Otherwise Claude Code keeps asking you to authenticate.
- Without a browser (SSH): `claude mcp login plugin:agents4-coach:agents4 --no-browser`, then paste the redirect
  URL back when asked.

### Codex

```sh
codex plugin marketplace add agents4fitness/plugins
codex plugin add agents4-coach@agents4-fitness
```

Codex asks you to sign in when the plugin is installed. To sign in later, run `codex mcp login agents4`.

### ChatGPT and Claude.ai (no plugin needed)

Add the Agents4 Fitness connector:
- **ChatGPT:** a custom connector with `https://api.agents4.com/mcp/http`. ChatGPT can hand uploaded plan files
  straight to Agents4 Fitness.
- **Claude.ai or Claude Desktop:** Settings → Connectors → Add custom connector →
  `https://api.agents4.com/mcp/claude`.

### Signing in

1. Your browser opens the Agents4 Fitness sign-in page, then a consent screen showing which app is asking.
2. Choose whether it may make changes, or only read.
3. Approve.

A client account or a coach without the Architect plan can't connect. Upgrade in the Agents4 Fitness app under
MCP Connection, then start again. You can disconnect any app from MCP Connections in the app at any time.

## Skills

Each skill is also a command in Claude Code, e.g. `/agents4-coach:weekly-review`.

| Skill | Use |
|---|---|
| `agents4-setup` | Check the connection, see what you can ask |
| `weekly-review` | "How did my clients do this week? Who should I check on?" |
| `client-review` | "What's going on with Sarah?" |
| `adjust-client-plans` | Workout and nutrition changes: one client, a group, or everyone; dates or from now on |
| `build-agent-from-plan` | Turn your own program into the coaching agent your clients chat with |
| `bring-clients-over` | Invite your existing clients (name plus email or phone) and set up each one's current plan |
| `message-clients` | Messages to one client or a group, only when you ask |

Group changes, messages and invitations are previewed before they are applied or sent. A new agent is created as
a draft until you put it live.

## Privacy and support

- [Privacy policy](https://agents4fitness.com/privacy) · [Terms](https://agents4fitness.com/terms)
- support@agents4.com

## Development

```sh
python build.py            # copy skills/ into both plugins, generate the Codex skill cards
python check.py --online   # release checks: build, manifests, assets, brand, claude validate, live sign-in metadata
```

- **Codex tool budget:** Codex shows a plugin's MCP tools only while their definitions total 64 KB. That is why
  the Codex plugin uses `?profile=coach-compact`.
- **Windows:** Codex needs its Windows sandbox enabled (`[windows] sandbox = "elevated"`) to read skill files.
