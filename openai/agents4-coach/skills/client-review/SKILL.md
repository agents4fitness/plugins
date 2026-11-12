---
name: client-review
description: Everything about one Agents4 Fitness client — workouts done vs planned, missed sessions, PRs, nutrition vs targets, check-ins, weight, upcoming sessions, recent messages — or what their plan shows on a given day. Use for "what's going on with Sarah?", "is Mike hitting his protein?", "what did Jamal lift last week?", "does Maya's Tuesday session have the face pulls?".
metadata:
  short-description: "Everything about one client: workouts, nutrition, check-ins"
  display-name: "Client review"
  default-prompt: "What's going on with Sarah? Is she hitting her protein?"
---

# Client review

1. Call `coach_client_summary` with `client` (their name) and `days` (14 by default; use the coach's window).
   - If the name matches several clients, the result lists candidates: ask which one.
2. Answer the coach's actual question first, then the rest briefly:
   - **Workouts:** completed of planned (adherence %), missed dates with the session name, today's session if
     still open, PRs. Lifts per session are in `workouts.sessions[].lifts`.
   - **Nutrition:** days logged, average logged vs the targets their plan shows, days at ≥90% of protein. If they
     log one meal a day or calories are implausibly low with stable weight, say it looks like under-logging.
   - **Check-ins:** count, last date, sleep/energy/stress averages, weight first → last, recent notes.
   - **Program:** which program they follow and whether the coach customised it.
   - **Next sessions** and recent messages.
3. Suggest one or two concrete next steps (a message, a plan change); do them only if asked.

For what they'll see on specific dates, use `coach_get_client_plan`.

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
