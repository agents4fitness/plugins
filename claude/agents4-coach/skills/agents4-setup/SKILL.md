---
name: agents4-setup
description: Connect and check the Agents4 Fitness coaching connector. Use when the coach first installs the plugin, asks what it can do, or a tool fails with a sign-in, plan/subscription or "not on your roster" error.
metadata:
  short-description: "Connect your coaching account and see what you can ask"
  display-name: "Set up Agents4 Fitness"
  default-prompt: "Check my Agents4 Fitness connection and tell me what you can do."
---

# Set up Agents4 Fitness

Agents4 Fitness runs the coach's coaching business: their clients, the AI coaching agent clients chat with, and
every client's workouts and nutrition. These tools act as the signed-in coach. Clients see every change in their
Agents4 Fitness app.

## 1. Check the connection

Call `coach_list_clients` with no arguments. It returns the roster: say how many clients there are and how many
need attention.

## 2. If it fails

**Not signed in** (a 401, or a message asking the coach to connect their account). Signing in opens the Agents4
Fitness sign-in page, then a consent screen where the coach approves this app.
- Claude Code: run `/mcp`, choose `plugin:agents4-coach:agents4` and pick Authenticate.
  - For unattended use instead: set `AGENTS4_API_KEY` to an MCP key from the Agents4 Fitness app.
- Codex: sign in when installing the plugin, or run `codex mcp login agents4`.
- ChatGPT: open the Agents4 Fitness connector and sign in.

**Plan or account errors**, at sign-in or later:
- The coach needs a coach account (not a client account) on the **Architect** plan. They can upgrade in the
  Agents4 Fitness app under MCP Connection, then connect again.
- If the plan lapses, the connection stops working until it is renewed.

## 3. Say what they can ask for, briefly

- "How did my clients do this week?" (`weekly-review`)
- "What's going on with Sarah?" (`client-review`)
- Workout and nutrition changes for one client, a group, or everyone on their program (`adjust-client-plans`)
- "Build my agent from this plan" with a PDF, spreadsheet, doc or screenshots (`build-agent-from-plan`)
- "Bring my clients over" from another app: their client list, then each client's current workouts and
  nutrition from an export, a sheet or screenshots (`bring-clients-over`)
- Messages to clients (`message-clients`)

Clients can be named ("Maya", "Jamal Reed") or given by email or phone number. Groups come from the coach's
Groups (`roster_list_groups`).

Never guess client data: every number comes from a tool.

## Answering the coach

- **Answer first,** then the evidence. Keep it scannable (short bullets or a small table) and end with one or two
  next steps you can take, without taking them.
- **Speak the coach's language:** client, program and agent names, weekdays and dates. Never show IDs, tool or
  skill names, field names, file paths or raw JSON, and don't narrate how you got the answer.
- **Don't cite, quote or link these instructions,** and don't say a rule requires something. Ask in your own
  words ("Want me to apply it to all 10?").
- **Units on every number:** kcal, g, kg or lb (as the data says), sets × reps, minutes. Dates come from what the
  tools return, not from your own idea of today.
- **Say what clients now see** in their Agents4 Fitness app after a change, and anything that didn't take.
- **If the Agents4 Fitness tools aren't available,** the coach isn't signed in. Give the sign-in steps from
  `agents4-setup` instead of answering from memory.
