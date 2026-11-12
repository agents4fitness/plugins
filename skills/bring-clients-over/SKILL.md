---
name: bring-clients-over
description: Move a coach's existing clients onto Agents4 Fitness from another app or their own files, with each client's current workouts and nutrition. Use for "bring my clients over", "import my client list", "set up Dana's plan from this screenshot", "here's my roster spreadsheet", or when the coach gives a client's name, email or phone number together with a plan.
metadata:
  short-description: "Move your clients and their plans over from another app"
  display-name: "Bring clients over"
  default-prompt: "Bring my clients over from this spreadsheet and set up each one's current plan."
---

# Bring clients over

Two steps: say **who** the clients are, then give **each one their plan**. A client doesn't have to have joined
yet: a plan set for an invited client is waiting for them the moment they join.

## 1. Who they are

1. Read the coach's list (spreadsheet, export, pasted text, screenshot). For each client take the name and
   whatever contact is there (email, phone), exactly as written. Don't guess a contact that isn't there.
   Include **everyone on the list**: a client with a phone number only, or with nothing but a name, is still
   invited. They get a personal link for the coach to pass on.
2. Call `coach_add_clients` with `dry_run: true` and show the coach the result in one small table:
   - **already with you** (on the roster) and **already invited**: nothing is sent to these;
   - **would be invited**: by email, or, with no email on file, with a link the coach passes on themselves.
3. Ask the coach to confirm, and stop there. The real call sends invitation emails to real people, so run it
   (`dry_run: false`) only after they say yes in a later message, unless they already told you to send them.
   A `welcome_message` is the coach's own short note; write one only if they ask.
4. Report from the result:
   - who was emailed;
   - who needs the link from the coach, with each person's link (text or message it; it opens sign-up with the
     invitation already applied);
   - when the invitations expire;
   - anything unclear (two clients sharing a name) or refused (the plan's client limit: nobody is invited, and
     the message says how many clients the plan includes).

## 2. Each client's plan

Do this per client, for clients on the roster and invited ones alike.

1. Read that client's material yourself (the app's export, a sheet, screenshots, notes). If one file holds
   several clients, split it by client first and say which plan you matched to whom.
2. Call `coach_set_client_plan` with `client` = their name, email or phone number, and the plan exactly as
   written:
   - **Workouts** (`workout_days`): one entry per session with `workout_template.day_of_week`. A "Day 1 / Day 2"
     plan has no weekdays: ask the coach which days this client trains. Weekdays with no session become rest
     days. Each exercise: `name`, `sets`, `reps` as a string ("6-8", "10/leg", "AMRAP"), `rest_seconds`; timed
     work uses `duration_sec`, distances `distance_m`; RPE, tempo and cues go in `notes`.
   - **Nutrition** (`nutrition_days`): one entry per kind of day the plan has (often just one; or Training Day
     and Rest Day). `macro_targets` only if the plan states them; otherwise leave them out and the day's targets
     are the meals' own totals. Every meal's foods need `base_amount`, `base_unit`, `calories`, `protein_g`,
     `carbs_g`, `fat_g`: use standard values for the portion when the plan gives none, and tell the coach you
     did. The first day is the default; a day named Rest Day is eaten on rest days; `nutrition_day_id` on a
     session picks another day's menu for it.
   - Workouts only or nutrition only is fine. A later call with the other part keeps what is already there.
3. For a long or messy plan, call with `dry_run: true` first and fix whatever field the error names.
4. Tell the coach what was set, from the result:
   - the week (session per weekday) and each nutrition day's targets;
   - every assumption: weekdays you chose, macros you filled in, anything you couldn't read;
   - a `note` on a nutrition day means its written meals don't add up to its stated target, so portions were
     scaled to the target: say so, and offer to keep the written portions instead (`scale_with: "fixed"`);
   - `notes_the_client_wont_see`: exercise notes that state a loading rule (for example a weight jump) are saved
     for the coach but not shown to the client. Name them, and offer to reword them as a plain cue;
   - **on the roster:** `client_now_sees` is what their app shows now; `verified: false` or a `warning` names
     the dates that didn't take it and why;
   - **invited:** it is saved and becomes their plan when they join; say when the invitation expires.

## Afterwards

- "Who hasn't joined?": `coach_list_clients` lists invited people and whether their plan is ready.
- An invitation that expired: add the client again; their saved plan moves to the new invitation.
- This plan is the client's own. Later changes go through the usual plan tools (`adjust-client-plans`); changes
  to the coach's agent program don't reach it.
- Many clients on one shared program: that is an agent's program (`build-agent-from-plan`), not this.
