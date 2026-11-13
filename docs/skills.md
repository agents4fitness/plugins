# Skills

A skill is a set of written instructions your AI app follows for one kind of request: which Agents4 Fitness
tools to use, in what order, when to show you a preview, and how to report back. The Claude Code and Codex
plugins ship the seven skills below. You do not have to name a skill: ask in your own words and the right one is
used.

In Claude Code each skill is also a command, for example `/agents4-coach:weekly-review`.

| Skill | For |
|---|---|
| [`agents4-setup`](#agents4-setup) | Checking the connection and seeing what you can ask |
| [`weekly-review`](#weekly-review) | The week across your roster, or any question about a group |
| [`client-review`](#client-review) | Everything about one client |
| [`adjust-client-plans`](#adjust-client-plans) | Workout and nutrition changes for one client, a group or everyone |
| [`build-agent-from-plan`](#build-agent-from-plan) | Turning your own program into your coaching agent |
| [`bring-clients-over`](#bring-clients-over) | Moving your existing clients and their plans over from another app |
| [`message-clients`](#message-clients) | A message to one client or a group |

Then: [what every skill has in common](#what-every-skill-has-in-common) and
[write a routine of your own](#write-a-routine-of-your-own).

## agents4-setup

**Say:** "Check my Agents4 Fitness connection and tell me what you can do."

Reads your roster to confirm the connection works, and says how many clients you have and how many need
attention. If the connection fails, it gives the sign-in steps for your app, or explains a plan or account
problem (a client account, or a coach account that is not on the Architect plan).

Uses `coach_list_clients`.

## weekly-review

**Say:** "How did my clients do this week? Who should I check on?" · "How is my Saturday group doing?"

Reads one report and fits the answer on one screen: the headline numbers (workouts completed of planned,
protein against target, meal logging, check-ins, sleep, weight trend, personal records), up to five clients to
check on with the evidence, and the week's wins. Your whole roster and the last 7 days unless you name a group
or a window.

- A client with no plan is listed separately, not as someone missing sessions.
- Very low logged calories with a steady weight are reported as likely under-logging.
- It changes nothing, and offers a closer look, a message or a plan change as next steps.

Uses `coach_cohort_report`.

## client-review

**Say:** "What's going on with Sarah?" · "Is Mike hitting his protein?" · "What did Jamal lift last week?"

Answers your question first, then gives the rest briefly: workouts completed against planned with missed dates
and personal records, nutrition logged against the targets in their plan, check-ins and weight, which program
they follow and whether you customised it, their next sessions and your recent messages. The last 14 days unless
you name a window.

For "what will Maya see on Tuesday?", it reads her plan day by day exactly as her app shows it.

Uses `coach_client_summary` and `coach_get_client_plan`.

## adjust-client-plans

**Say:** "Swap back squats for leg press for Jamal for the next two weeks." · "Drop carbs by 20 g on rest days
for my Saturday group." · "Swap Tuesday's lunges for split squats for everyone on my program."

Picks the scope from how you ask:

| You want | What changes |
|---|---|
| Certain dates ("this week", "for the next two weeks") | Those dates only, for the clients you named |
| From now on, for one client or a group | Those clients get their own copy of the program with the change |
| Everyone on your program | The program itself, so every client on it follows the change |

- One client and a clear request: applied at once.
- More than one client: you get a preview (who it reaches, before and after) and it is applied after you
  confirm.
- The reply says what each client now sees, and names any date or client that did not take the change.
- A client with their own copy stops following later changes to your program. You are told when that happens,
  and you can put them back on the program at any time.
- It does not message clients about the change unless you ask.

Uses `coach_edit_workouts`, `coach_edit_nutrition`, `coach_edit_program`, `coach_revert_client_program` and
`coach_get_client_plan`.

## build-agent-from-plan

**Say:** "Build my coaching agent from this plan, exactly as written." (attach a PDF, spreadsheet, document,
screenshots or notes)

Reads your program and creates your agent from it: the training week with every exercise's sets, reps, rest and
notes, your nutrition days with their targets and meals, and your progression and deload rules.

- The agent is a **draft** until you say to put it live.
- You are told what was imported and every assumption that was made.
- Recovery-based adjustments are on, and you can change how they work.
- On request: a preview conversation with the agent, putting it live (safety checks run first, and it replaces
  your current live agent), and moving clients onto it.

Uses `agent_builder_import_plan` (or `agent_builder_import_plan_file` where the app hands your uploaded file to
the server), then `agents_test_agent_interaction`, `agents_deploy_agent` and `agents_assign_agent_to_clients`.

## bring-clients-over

**Say:** "Bring my clients over from this spreadsheet and set up each one's current plan."

Two steps. First your client list: it previews who would be invited and how, and sends the invitations after
you confirm. Then each client's plan, read from what you have (an export, a spreadsheet, screenshots, notes)
and saved exactly as written.

- A client already on your roster or already invited is not invited twice.
- A client with no email address gets a personal link that you pass on.
- A plan set for an invited client is waiting for them the moment they join.
- You are told every assumption: weekdays that were chosen, macros that were filled in, anything unreadable.
- It first checks that your connection has the tools it needs. If they are missing (for example on a read-only
  connection), it says so and stops.

Uses `coach_add_clients`, `coach_set_client_plan` and `coach_list_clients`.

## message-clients

**Say:** "Remind everyone on my program that check-ins are due Sunday night."

Writes the message as you, in your tone. One client: sent. More than one: you see the message and the
recipients and it is sent after you confirm. It lands in each client's Agents4 Fitness inbox with a push
notification.

It runs only when you ask to message, remind, tell or announce something.

Uses `coach_message_clients`.

## What every skill has in common

- **The answer comes first,** then the evidence, short enough to scan.
- **Your terms:** client, program and agent names, weekdays and dates. No ids or tool names.
- **Units on every number:** kcal, g, kg or lb as your data has it, sets × reps, minutes.
- **Every number comes from your account.** Nothing is estimated.
- **After a change, you are told what clients now see** in their app, and anything that did not take.
- **Next steps are offered, not taken.**

## Write a routine of your own

The seven skills cover single requests. A routine strings them into the way you work: your Monday check, your
Friday wrap-up, your onboarding steps for a new client. A routine is one text file.

### Start from the sample

[examples/skills/friday-wrap-up/SKILL.md](../examples/skills/friday-wrap-up/SKILL.md) reads the week, picks up
to three clients to check on, drafts a note to each, and sends only the ones you approve.

To install it in Claude Code, copy the folder `examples/skills/friday-wrap-up` from this repository to
`.claude/skills/friday-wrap-up` in your project. To have it in every project, copy it to
`~/.claude/skills/friday-wrap-up` instead. On macOS, Linux or Git Bash, from a copy of this repository:

```sh
# this project only
mkdir -p .claude/skills && cp -r examples/skills/friday-wrap-up .claude/skills/

# every project
mkdir -p ~/.claude/skills && cp -r examples/skills/friday-wrap-up ~/.claude/skills/
```

Start a new Claude Code session and say "Do my Friday wrap-up." [Use case 8](use-cases.md#8-run-a-routine-of-your-own)
shows a reply.

Other apps have their own place for skills or custom instructions. The steps you write are the same.

### The parts of the file

The sample, shortened:

```markdown
---
name: friday-wrap-up
description: The coach's end-of-week routine in Agents4 Fitness — this week's numbers, up to three clients to check on, and a drafted note for each that the coach approves before anything is sent. Use for "do my Friday wrap-up", "wrap up the week", "end of week routine".
---

# Friday wrap-up

1. Call `coach_cohort_report` for the whole roster, last 7 days.
2. Give the week in three lines: workouts completed of planned, average protein against target, check-ins.
3. Pick at most three clients to check on, worst first: two or more missed workouts, no check-in in five days,
   or no meals logged.
4. For each of those clients, draft a short note from the coach. Do not send anything yet.
5. Show the drafts and ask which ones to send, then stop. After the coach answers, send only the notes they
   approved (`coach_message_clients`, one client per call) and say who was messaged.
```

- **`name`** is the folder name.
- **`description`** decides when the skill is used. Keep it on one line, say what the routine does, and quote
  the phrases you would actually type.
- **The steps** are plain instructions. Name the tool for each step so the right one is used.

### What makes a routine dependable

- **Say when to stop and ask.** "Show the drafts and ask which ones to send, then stop" is what keeps a routine
  from sending messages on its own. Do the same before any change that reaches more than one client.
- **Say where the numbers come from.** "Every number comes from the report: never estimate."
- **Write your thresholds down.** Two missed workouts, five days without a check-in, 80% of protein: whatever
  you actually use to decide who needs you.
- **Write in your voice.** "First person, plain, no emoji" produces notes that sound like you.
- **Say what to do when the tools are missing,** so a routine never answers from memory.
- **Try it on one client first.** The plan, message and invitation tools accept `dry_run: true`, which previews
  without applying.

### Tools to build on

| Step in your routine | Tool |
|---|---|
| Who is on my roster, who is invited, who needs attention | `coach_list_clients` |
| The numbers for a group over a window | `coach_cohort_report` |
| Everything about one client | `coach_client_summary` |
| What a client sees on given dates | `coach_get_client_plan` |
| Change workouts or nutrition | `coach_edit_workouts`, `coach_edit_nutrition` |
| Message one client or a group | `coach_message_clients` |
| My groups | `roster_list_groups` |

[connect.md](connect.md#what-the-server-offers) has the full list.
