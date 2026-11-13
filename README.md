# Agents4 Fitness for coaches: plugins and MCP server

Agents4 Fitness turns your coaching method into an AI agent. The agent writes each client's training and
nutrition plan by your rules and adapts it to that client. This repository connects your Agents4 Fitness coach
account to the AI app you already use (Claude, ChatGPT, Claude Code, Codex, or your own code), so you can run
your roster by asking for what you want.

Once connected, you can:

- review the week across your roster and see who to check on;
- look into one client: workouts completed against planned, nutrition against targets, check-ins, weight;
- change workouts and nutrition for one client, a group, or everyone on your program, for set dates or from now
  on;
- build your coaching agent from your own program (PDF, spreadsheet, document or screenshots), exactly as written;
- bring your existing clients over from another app: your client list, then each client's current workouts and
  nutrition, ready for them when they join;
- message one client or a group.

Clients see every change in their Agents4 Fitness app.

| In this repository | What it is |
|---|---|
| [docs/connect.md](docs/connect.md) | How to connect each app, or your own code, to the Agents4 Fitness MCP server |
| [docs/use-cases.md](docs/use-cases.md) | Sample use cases: what to ask, what happens, what your clients see |
| [docs/skills.md](docs/skills.md) | The seven skills the plugins ship, and how to write a routine of your own |
| [examples/](examples/) | A sample skill to copy and a short Python client |
| `claude/agents4-coach` | The plugin for Claude Code |
| `openai/agents4-coach` | The plugin for Codex |
| `skills/` | The skills both plugins ship (edit here, then run `build.py`) |

## What you need

- An Agents4 Fitness coach account on the **Architect** plan. A client account, or a coach account on another
  plan, cannot connect.
- An AI app that accepts custom connectors or MCP servers.

## Connect

The server URL is the same for every app:

```text
https://api.agents4.com/mcp/http
```

| Your app | How you connect | Steps |
|---|---|---|
| Claude (claude.ai or the desktop app) | Add a custom connector with the server URL, then sign in | [Claude](docs/connect.md#claude) |
| ChatGPT | Add a custom connector with the server URL, then sign in | [ChatGPT](docs/connect.md#chatgpt) |
| Claude Code | Install the plugin (two commands), then sign in | [Claude Code](docs/connect.md#claude-code) |
| Codex | Install the plugin (two commands), then sign in | [Codex](docs/connect.md#codex) |
| Cursor, VS Code | Add the server with an API key from the app | [Cursor and VS Code](docs/connect.md#cursor-and-vs-code) |
| Your own code | Any MCP client: the server URL and an API key or OAuth | [Your own code](docs/connect.md#your-own-code) |

### Claude Code

```sh
claude plugin marketplace add agents4fitness/plugins
claude plugin install agents4-coach@agents4-fitness
```

Then sign in: in Claude Code run `/mcp`, choose `plugin:agents4-coach:agents4`, and pick **Authenticate**.

### Codex

```sh
codex plugin marketplace add agents4fitness/plugins
codex plugin add agents4-coach@agents4-fitness
```

Codex asks you to sign in when the plugin is installed. To sign in later, run `codex mcp login agents4`.

### Signing in

1. Your browser opens the Agents4 Fitness sign-in page, then an approval screen that names the app asking.
2. Choose whether the app may make changes, or only read.
3. Approve.

You can disconnect any app in the Agents4 Fitness app under More → Connect ChatGPT & Claude.
[docs/connect.md](docs/connect.md) has the full steps, API keys and troubleshooting.

## First things to ask

- "How did my clients do this week? Who should I check on?"
- "What's going on with Sarah? Is she hitting her protein?"
- "Sam tweaked his knee: no squats or lunges for the next two weeks."
- "Swap Tuesday's lunges for Bulgarian split squats for everyone on my hypertrophy program."
- "Here's my 12-week program (PDF). Build my coaching agent from it exactly as written."
- "Bring my clients over from this spreadsheet and set up each one's current plan."

[docs/use-cases.md](docs/use-cases.md) walks through each of these.

## Skills

A skill is a set of instructions your AI app follows for one kind of request. The plugins ship seven. In Claude
Code each one is also a command, for example `/agents4-coach:weekly-review`.

| Skill | Use |
|---|---|
| `agents4-setup` | Check the connection, see what you can ask |
| `weekly-review` | "How did my clients do this week? Who should I check on?" |
| `client-review` | "What's going on with Sarah?" |
| `adjust-client-plans` | Workout and nutrition changes: one client, a group, or everyone; dates or from now on |
| `build-agent-from-plan` | Turn your own program into the coaching agent your clients chat with |
| `bring-clients-over` | Invite your existing clients (name plus email or phone) and set up each one's current plan |
| `message-clients` | Messages to one client or a group, only when you ask |

[docs/skills.md](docs/skills.md) describes each one and shows how to write a routine of your own, starting from
[examples/skills/friday-wrap-up](examples/skills/friday-wrap-up/SKILL.md).

Without a plugin (Claude and ChatGPT connectors), the server gives your AI app the same guidance in short form,
so the requests above work there too.

## How changes are applied

- **One client, a clear request:** applied at once. The reply says what that client now sees in their app.
- **A group, everyone on a program, a message to several clients, or invitations:** previewed first (who it
  reaches, and what changes), then applied when you confirm.
- **A new agent** is created as a draft. It goes live when you say so.
- **Read only:** at sign-in you can let an app read without making changes.

## Privacy and support

- [Privacy policy](https://agents4fitness.com/privacy) · [Terms](https://agents4fitness.com/terms)
- [Connection help](https://agents4fitness.com/help/connect-ai)
- support@agents4.com

Agents4 Fitness is not affiliated with Anthropic or OpenAI.

## Development

```sh
python build.py            # copy skills/ into both plugins, generate the Codex skill cards
python check.py --online   # release checks: build, manifests, docs, brand, claude validate, live sign-in metadata
```

- **Codex tool budget:** Codex shows a plugin's MCP tools only while their definitions total 64 KB. That is why
  the Codex plugin uses `?profile=coach-compact`.
- **Windows:** Codex needs its Windows sandbox enabled (`[windows] sandbox = "elevated"`) to read skill files.
