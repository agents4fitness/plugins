---
name: friday-wrap-up
description: The coach's end-of-week routine in Agents4 Fitness — this week's numbers, up to three clients to check on, and a drafted note for each that the coach approves before anything is sent. Use for "do my Friday wrap-up", "wrap up the week", "end of week routine".
---

# Friday wrap-up

A sample routine. Change the steps, the thresholds and the wording to the way you coach.

1. Call `coach_cohort_report` for the whole roster, last 7 days.
2. Give the week in three lines: workouts completed of planned, average protein against target, check-ins.
3. Pick at most three clients to check on, worst first: two or more missed workouts, no check-in in five days,
   or no meals logged. One line each with the evidence. Clients with no plan yet go on a separate line; they
   are not missing sessions.
4. For each of those clients, draft a short note from the coach: first person, plain, no emoji, one specific
   observation from their week and one question. Do not send anything yet.
5. Show the drafts and ask which ones to send, then stop. After the coach answers, send only the notes they
   approved (`coach_message_clients`, one client per call) and say who was messaged.
6. Close with one win from the week if the report has one.

Every number comes from the report: never estimate. Use client names, weekdays and dates, never ids or tool
names. If the Agents4 Fitness tools are missing, the coach is not connected: say so and stop.
