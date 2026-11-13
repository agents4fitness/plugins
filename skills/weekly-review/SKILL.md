---
name: weekly-review
description: Weekly update on the coach's clients from Agents4 Fitness — headline numbers, wins, and who to check on. Use for "how did my clients do this week", "who should I worry about", "weekly report", or any question about a group (a cohort, an agent's clients, a goal).
metadata:
  short-description: "Headline numbers, wins and who to check on"
  display-name: "Weekly client review"
  default-prompt: "How did my clients do this week? Who should I check on?"
---

# Weekly review

1. Call `coach_cohort_report`.
   - Whole roster, last 7 days by default. For a group, pass `cohort` (`{"group": "HYROX squad"}`,
     `{"agent": "<agent name>"}`, `{"names": ["Maya", "Jamal"]}`, `{"goal": "fat loss"}`) and `days` if the coach
     named a window.
2. Lead with the headline numbers from `summary`:
   - workouts completed of planned (adherence %), PRs
   - protein vs target, meal-logging days
   - check-ins, sleep, weight trend
3. Who to check on: build the list from `highlights` and the rows, worst first, one line each with the evidence
   ("0 of 5 workouts, no meals logged, checks in daily").
   - `missed_2_or_more_workouts`, `no_workout_logged`, `under_80pct_protein`, `no_check_in_5_plus_days`,
     `not_logging_meals`.
   - The app's `needs_attention` flag is based on check-ins only, so a client can be missing workouts without it.
   - Very low logged calories with flat weight usually means under-logging, not under-eating — say so.
   - Clients with no planned workouts (no plan yet, or another program) aren't "missing" sessions; mention them
     separately if relevant.
4. Wins: clients who hit their sessions and protein, and PRs.
5. Fit it on one screen: the headline numbers, up to five clients to check on (offer the rest), and wins in a
   line or two. Mention clients without a plan in one line.
6. Offer next steps; don't take them unasked: a deeper look at one client (`client-review`), a message
   (`message-clients`), or a plan change (`adjust-client-plans`).

Answer from the rows: never estimate numbers the report didn't give.
