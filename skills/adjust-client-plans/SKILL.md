---
name: adjust-client-plans
description: Change Agents4 Fitness clients' workouts or nutrition — one client, a group, or everyone on the coach's program; for specific dates or from now on. Use for exercise swaps/adds/removals, sets/reps changes, rest days, calorie or macro changes, food swaps.
metadata:
  short-description: "Change workouts or nutrition for one client, a group or everyone"
  display-name: "Adjust client plans"
  default-prompt: "Swap back squats for leg press for Jamal for the next two weeks."
---

# Adjust client plans

## 1. Pick the tool and scope

| The coach wants | Tool | Arguments |
|---|---|---|
| A change for **everyone on their program** ("for everyone on Northline") | `coach_edit_program` | `agent`, `day` + `workout_changes`, or `nutrition_day` + `targets`/`change`/`food_swaps` |
| One client, or a group/list of clients | `coach_edit_workouts` / `coach_edit_nutrition` | `client`, or `cohort` (`{"group": ...}`, `{"names": [...]}`, `{"agent": ...}`) |
| Only certain dates ("this week", "for the next two weeks") | same | `scope: "dates"` + `dates` or `start_date`/`end_date` |
| From now on, for those clients only | same | `scope: "program"` |

- `scope: "program"` gives those clients their **own copy** of the program: later changes to the agent's program
  won't reach them until `coach_revert_client_program`. Tell the coach when this happens.
- A new group: `roster_create_group` with `group_name` and `client_ids` (ids from `coach_list_clients`).

## 2. Workout changes

`changes` is a list of ops:
- `swap` — `exercise`, `with`; keeps sets/reps unless given
- `add` — `exercise`, `sets`, `reps`, `rest_seconds`, optional `after`; with `scope: "program"` it needs `day`
  (a weekday or session name, e.g. "Upper A")
- `remove`
- `update` — sets, reps, weight, rest_seconds, notes
- `replace_session`
- `make_rest_day`

Read the current plan first when unsure what's there (`coach_get_client_plan`).

## 3. Nutrition changes

- `targets` (absolute) or `change` (e.g. `{"calories": -150}`, `{"carbs": -20}`); calories stay consistent with
  the macros, and protein holds unless changed.
- `day`: "training", "rest", or a named day.
- Food swaps (`scope: "program"`) need the replacement's portion and macros (standard values are fine): pick a
  portion with similar calories to the food it replaces.

## 4. Apply safely

1. **One client, clear request:** apply it straight away.
2. **More than one client** (a group, a list, everyone on a program), or anything the coach might not expect:
   - Run it with `dry_run: true` and show the preview: who it reaches, and what changes (before → after).
   - Ask the coach to confirm in that same reply, and stop there. Apply only after they say yes in a later
     message. Their original request is not the confirmation, unless it says to go ahead without checking ("go
     ahead and apply it", "no need to confirm").
3. Report from the result:
   - `client_now_sees`: what each client's app shows now.
   - `verified: false` / `warning`: say exactly which dates or clients didn't take the change and why.
   - Clients skipped (marketplace programs, no plan yet).

Don't message clients about the change unless the coach asks: the app already shows their updated plan.
