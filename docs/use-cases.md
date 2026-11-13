# Sample use cases

What a coach asks once their AI app is [connected](connect.md), what happens, and what their clients see. You
ask in your own words. The phrasing below is only a starting point.

The example replies come from test runs on a test account. The clients in them are made up.

1. [Review the week](#1-review-the-week)
2. [Look into one client](#2-look-into-one-client)
3. [Change one client's plan](#3-change-one-clients-plan)
4. [Change a group, or everyone on your program](#4-change-a-group-or-everyone-on-your-program)
5. [Build your agent from your own program](#5-build-your-agent-from-your-own-program)
6. [Bring your clients over from another app](#6-bring-your-clients-over-from-another-app)
7. [Message clients](#7-message-clients)
8. [Run a routine of your own](#8-run-a-routine-of-your-own)

## 1. Review the week

**Ask**

- "How did my clients do this week? Who should I check on?"
- "How is my Saturday group doing over the last 14 days?"
- "Which of my clients are under their protein target?"

**What happens**

Your AI app reads one report for the clients you named (your whole roster and the last 7 days unless you say
otherwise) and answers on one screen:

- the headline numbers: workouts completed of planned, protein against target, days with meals logged,
  check-ins, sleep and weight trend, and personal records;
- up to five clients to check on, worst first, each with the evidence ("0 of 5 workouts, no meals logged");
- the week's wins.

A group can be one of your groups, the clients on one agent, a list of names, or clients with one goal. Clients
with no plan yet are listed separately. They are not counted as missing sessions.

Nothing is changed. The reply ends with next steps you can ask for: a closer look at one client, a message, or
a plan change.

## 2. Look into one client

**Ask**

- "What's going on with Sarah? Is she hitting her protein?"
- "What did Jamal lift last week?"
- "Does Maya's Tuesday session have the face pulls?"

**What happens**

Your question is answered first, from that client's own app data (the last 14 days unless you name a window):

- **Workouts:** completed of planned, missed dates with the session name, the lifts in each session, personal
  records.
- **Nutrition:** days logged, average intake against the targets their plan shows, days at 90% or more of
  protein.
- **Check-ins:** how many, the last one, sleep, energy and stress, weight from first to last, recent notes.
- **Program:** which program they follow and whether you have customised it for them.
- Their next sessions and your recent messages.

You can name a client by name, email address or phone number. If a name matches more than one client, you are
asked which one.

## 3. Change one client's plan

**Ask**

- "Sam tweaked his knee: no squats or lunges for the next two weeks."
- "From now on, swap the leg extension for sissy squats on Maria's Friday session."
- "Take 150 kcal off Dana's rest days."

**What happens**

A clear request for one client is applied at once. You choose how long it lasts by how you ask:

- **Set dates** ("this week", "for the next two weeks"): only those dates change. The program stays as it is.
- **From now on:** the client gets their own copy of the program with the change. Later changes to your agent's
  program will not reach them until you put them back on it.

Workout changes can swap, add or remove an exercise, change sets, reps, load, rest or notes, replace a whole
session, or make a day a rest day. Nutrition changes set new daily targets or shift them (calories stay
consistent with the macros, and protein holds unless you change it), on training days, rest days or a day you
name.

**What the client sees**

Their app shows the updated plan the next time they open it. The reply tells you what they now see.

**Example reply**

> I swapped the leg extension for sissy squats in Maria Lopez's Friday Quads session, and the change applies to
> every Friday from now on.
>
> - **Change:** Leg Extension → Sissy Squat, still 3 × 15.
> - **What Maria sees for tomorrow (Fri 13 Nov):** Leg Press, Bulgarian Split Squat, Sissy Squat.
>
> Maria now has her own copy of the program. Changes you make to your main agent program won't reach her unless
> you switch her back to it, which would also drop this swap.

## 4. Change a group, or everyone on your program

**Ask**

- "Swap Tuesday's lunges for Bulgarian split squats for everyone on my hypertrophy program."
- "The leg press is out of order this week. Give my 6 am group hack squats instead until Sunday."
- "Drop carbs by 20 g on rest days for my Saturday group."

**What happens**

1. You get a preview first: who the change reaches, and what changes for them, before and after.
2. You confirm, and it is applied. Your first request does not count as the confirmation unless it says to go
   ahead without checking.
3. The reply says what each client now sees, and names anyone it could not reach and why (for example a client
   with no plan yet).

"Everyone on my program" changes the program itself, so every client on it gets the change the next time they
open the app. The exception is a client you gave their own copy of the program
([use case 3](#3-change-one-clients-plan)). A group or a list of names changes those clients only.

To make a group, ask: "Make a group called 6 am with Maya, Jamal and Priya."

## 5. Build your agent from your own program

Your agent is your method, automated: it writes each client's training and nutrition plan by your rules and
adapts it to that client.

**Ask**

Attach your program and say:

- "Here's my 12-week program (PDF). Build my coaching agent from it exactly as written."
- "Build my agent from these screenshots of my training split and meal plan."

**What happens**

1. Your program is read exactly as written: the training week with every exercise's sets, reps, rest and notes,
   your nutrition days with their targets and meals, and your progression and deload rules.
2. The agent is created as a **draft**. Nothing changes for your clients.
3. You are told what was imported and every assumption that was made, such as a portion that had to be
   interpreted or macros that were filled in from standard values.
4. Recovery-based adjustments are on: when a client's readiness drops (their wearable, or check-ins showing poor
   sleep, high fatigue or pain), the agent lightens their next session. You can change that, for example so
   that each adjustment waits for your approval.

Then, when you ask:

- "Show me how it would answer a client who missed two sessions." (a preview conversation)
- "Put it live." It runs a set of safety checks first, and it replaces your current live agent.
- "Move Maya and Jamal onto it."

A program with phases or levels in one document becomes separate programs on the same agent.

## 6. Bring your clients over from another app

Two steps: who your clients are, then each client's current plan. A client does not have to have joined yet. A
plan you set for an invited client is waiting for them the moment they join.

**Ask**

- "I'm moving my coaching over from my old app. This spreadsheet is my client list."
- "These two screenshots are Maria's current training plan and meal plan. Set her up with exactly that."
- "Who hasn't joined yet, and is everyone's plan ready?"

**Step 1: your client list**

You get a preview before anything is sent.

> Your export lists 3 clients. All 3 would be new invitations, because none of them is on your Agents4 Fitness
> roster or already invited. Nothing has been sent yet.
>
> | Client | Contact on file | How they'd be invited |
> |---|---|---|
> | Maria Lopez | maria.lopez@example.com | Invitation email |
> | Jon Bauer | +1 312 555 0188 (phone only) | You get a personal sign-up link to text him |
> | Aisha Khan | No contact details | You get a personal sign-up link to pass on |
>
> **Should I send the 3 invitations?**

After you say yes:

- a client with an email address is emailed an invitation;
- a client with only a phone number, or only a name, gets a personal link that you pass on yourself;
- a client who is already on your roster, or already invited, is recognised and not invited twice;
- your plan's client limit applies. If the list would go over it, nobody is invited and you are told the limit.

**Step 2: each client's plan**

Send what you have for each client: the old app's export, a spreadsheet, screenshots, or typed notes.

> Maria's plan is saved exactly as written in her screenshots. She hasn't joined yet, so she'll get the plan the
> moment she accepts her invitation.
>
> | Day | Session | Exercises |
> |---|---|---|
> | Mon | Glutes & Hamstrings | Hip Thrust 4×8 (rest 120 s) · Romanian Deadlift 3×10 (90 s) · Cable Kickback 3×15/side (45 s) |
> | Wed | Upper Body | Lat Pulldown 4×10 (75 s) · Dumbbell Shoulder Press 3×10 (75 s) · Seated Cable Row 3×12 (60 s) |
> | Fri | Quads | Leg Press 4×12 (120 s) · Bulgarian Split Squat 3×8/leg (90 s) · Leg Extension 3×15 (60 s) |
> | Tue, Thu, Sat, Sun | Rest | |
>
> **Nutrition (every day):** 1,725 kcal · 139 g protein · 176 g carbs · 53 g fat. That's 4 meals with all 12
> foods at the written portions.
>
> **Assumptions:** none. Everything came straight from the screenshots.

You are told about anything that needs your call. For example:

- A plan written as "Day 1, Day 2" has no weekdays, so you are asked which days that client trains.
- If the written meals do not add up to the stated targets, the portions are scaled to reach the targets. You
  are told the gap and can keep the written portions instead.
- Calories and macros that the plan does not list are filled in from standard values, and the reply says so.
- An exercise note that states a loading rule (for example "add 2.5 kg when all sets hit 5") is kept for you and
  is not shown to the client. The reply names it and offers to reword it as a cue the client will see.

**What the client sees**

A client already on your roster has the plan in their app straight away. An invited client has it the moment
they join, before they do anything else in the app.

**Good to know**

- An invitation lasts 7 days. If it expires, add the client again: their saved plan moves to the new
  invitation.
- The plan comes over. A client's history in the other app (logged sessions, weigh-ins, progress photos) does
  not.
- For many clients on one shared program, build an agent instead ([use case 5](#5-build-your-agent-from-your-own-program)).

## 7. Message clients

**Ask**

- "Tell Maya great work on the deadlift PR."
- "Remind everyone on my program that check-ins are due Sunday night."

**What happens**

- **One client:** the message is sent. If the wording was written for you, you see it first.
- **More than one client:** you see the message and the list of recipients, and it is sent after you confirm.
  The reply says how many clients it reached.

Messages are written as you, in your tone, and can address each client by first name.

**What the client sees**

The message arrives in their Agents4 Fitness inbox with a push notification.

Your AI app messages clients only when you ask it to. A plan change does not need a message: the client's app
already shows it.

## 8. Run a routine of your own

A skill is a short set of written steps. [examples/skills/friday-wrap-up](../examples/skills/friday-wrap-up/SKILL.md)
is a sample end-of-week routine: the week's numbers, up to three clients to check on, and a drafted note for
each that you approve before anything is sent. [skills.md](skills.md#write-a-routine-of-your-own) shows how to
install it and change it.

**Ask**

- "Do my Friday wrap-up."

**Example reply**

> Here's your wrap-up for Saturday 7 – Friday 13 November.
>
> **The week**
> - **Workouts:** 0 of 6 planned sessions were completed.
> - **Protein:** there's no average, because no client logged any meals this week.
> - **Check-ins:** none from any of your 3 clients.
>
> **Clients to check on (worst first)**
> 1. **Dana Whitlock:** missed all 4 planned sessions (Sat 7, Mon 9, Tue 10 and Thu 12 Nov). No meals logged
>    against her 1,969 kcal / 154 g protein targets, and no check-in on record.
> 2. **Sam Okafor:** missed both planned sessions (Mon 9 and Wed 11 Nov). No meals logged against his 1,881 kcal /
>    153 g protein targets, and no check-in on record.
>
> **Lee Park has no plan yet,** so he isn't missing sessions.
>
> **Draft notes (none sent yet)**
>
> **To Dana:** Hi Dana, I noticed none of your four sessions this week got logged: Saturday, Monday, Tuesday or
> Thursday. That's fine, weeks like this happen, but I'd like to know what got in the way. Is it the schedule,
> the workouts themselves, or something else going on?
>
> **To Sam:** Hi Sam, your Monday and Wednesday sessions didn't get logged this week, and I haven't seen any meals
> come through either. Did you train and not log it, or was it a tough week to fit things in?
>
> Which of these should I send: Dana, Sam, both or neither? You can also change the wording first.

## From your own code

The same tools answer a script. [examples/python/weekly_numbers.py](../examples/python/weekly_numbers.py) reads
your roster and this week's numbers with an API key. See [Your own code](connect.md#your-own-code).
