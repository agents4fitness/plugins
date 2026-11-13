---
name: build-agent-from-plan
description: Turn a coach's own training/nutrition program (PDF, spreadsheet, Word doc, screenshots, notes) into an Agents4 Fitness coaching agent their clients chat with. Use for "build my agent from this plan", "import my program", "here's my 12-week block".
metadata:
  short-description: "Turn your own program into your AI coaching agent"
  display-name: "Build agent from plan"
  default-prompt: "Build my coaching agent from this plan, exactly as written."
---

# Build an agent from the coach's plan

## Read the plan

- **The host can hand the uploaded file to tools** (ChatGPT): call `agent_builder_import_plan_file` with `file`
  and `dry_run: true`. Show the coach what was read (`read.program`) and any `questions_for_the_coach`, then call
  it again with `dry_run: false`.
- **Otherwise** (Claude, Claude Code, Codex): read the file yourself and call `agent_builder_import_plan` with the
  program as structured days, exactly as written.

## Map it into `import_plan`

1. **Agent:** `agent.name` (the coach's name for it), `voice`, `instructions` (their philosophy and rules).
2. **Client type:** `program.client_type` with a new, specific `id` for this agent (e.g. `built_to_last_12wk`) —
   never another agent's.
3. **Workout days:** `program.workout_days` covering all 7 weekdays.
   - Each day: `workout_template.day_of_week` and `type`; rest days are `type: "rest"` with `exercises: []`.
   - Each exercise: `name`, `sets`, `reps` as a string ("6-8", "10/leg", "AMRAP"), `rest_seconds`, `notes` for
     RPE/RIR/tempo.
   - Timed work uses `duration_sec`; distances use `distance_m`.
   - Link each day to its nutrition day with `nutrition_day_id`.
4. **Nutrition days:** `program.nutrition_days`, e.g. Training Day / Rest Day.
   - `macro_targets` exactly as written.
   - `meal_template.meals[].foods[]`: `name`, numeric `base_amount` with `base_unit`, `calories`, `protein_g`,
     `carbs_g`, `fat_g`, and `scale_with`. Use standard values when the plan gives no macros.
   - `scale_with` is exactly one of `calories` (the default), `protein`, `carbs`, `fat` (the portion scales to
     each client's targets on that axis) or `fixed` (keep the coach's exact portion).
5. **Rules:** progression and deload rules go in `program.progression_notes`.
6. **Validate:** call with `dry_run: true` first, and fix whatever field the error names.

## Create it, then hand back

1. Create it as a **draft** (`deploy: false`) unless the coach explicitly said to put it live.
2. Tell the coach what was imported (days, exercise count, nutrition targets) and every assumption you made:
   portions you had to interpret, macros you filled in, ambiguous items.
   - Say in one line that **recovery-based adjustments are on**. When a client's readiness drops (their wearable,
     or check-ins showing poor sleep, high fatigue or pain), the agent lightens their next session: about 80%
     volume on a yellow day, 60% on an orange day, a recovery session on a red day. It adds recovery nutrition
     guidance but doesn't change calories. This is how Agents4 Fitness agents coach, so present it as part of the
     agent, not as a setting to review.
   - Change it only if the coach asks (`agents_set_agent_wearable_coaching_policy`; for example, `proposal` mode,
     where the coach approves each adjustment). Leave every other setting the coach didn't mention as it is.
3. Next steps, only on request:
   - preview a client chat (`agents_test_agent_interaction`)
   - go live (`agents_deploy_agent`, which runs the safety gate and **replaces the coach's current live agent**)
   - move clients onto it (`agents_assign_agent_to_clients`)

Phases or levels in one document become extra client types on the same agent (call again with `agent_id`).

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
