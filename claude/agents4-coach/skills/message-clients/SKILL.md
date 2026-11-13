---
name: message-clients
description: Send a message from the coach to one Agents4 Fitness client or a group (an agent's clients, a group, everyone). Use only when the coach asks to message, remind, tell or announce something to clients.
metadata:
  short-description: "Send a message to one client or a group"
  display-name: "Message clients"
  default-prompt: "Remind everyone on my program that check-ins are due Sunday night."
---

# Message clients

1. Work out the recipients: `client` (one name) or `cohort` (`{"agent": ...}`, `{"group": ...}`, `{"names": [...]}`,
   `{"all": true}`).
2. Draft the message as the coach, in the first person and in their tone: no emoji or hype unless the coach
   writes that way. Use `{{first_name}}` to address each client by name. Keep it short.
3. **One client:** send it, unless you had to word it for them.
4. **More than one client:** call `coach_message_clients` with `dry_run: true`. Show the message and the
   recipients, ask the coach to confirm, and stop there. Send after they say yes in a later message, unless they
   already said "send it". Then report how many it reached.

It lands in each client's Agents4 Fitness inbox with a push notification. Never message clients the coach didn't ask you
to — plan changes already show in their app.

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
