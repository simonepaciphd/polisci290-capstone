# Stage 4: Decide and lock

Goal: turn the plan review into decisions, finish `PLAN.md`, and lock the three planning files together. After the lock, work can start.

## Inputs

Read these in full before starting. Do not work from summaries.

- `docs/planning/SPEC.md` (approved specification)
- `docs/planning/RESOURCES.md` (inventory of starting materials)
- `docs/planning/PLAN.md` (draft plan from Stage 3)
- `docs/planning/Plan-Review.md` (critical review of the plan)

Leave `Plan-Review.md` unchanged. It is the record of what the reviewer found.

## Step 1: Sort each finding

Go through the review one finding at a time. Put each finding in one of three groups.

1. **Fix directly.** The fix is mechanical and follows from the approved spec in only one way. Examples: a task uses a file that no earlier task produces; a deliverable has no task that checks it; two tasks write the same file at the same time; a broken ID reference. Make the fix and record it.
2. **Student decision.** Two or more reasonable choices remain, or the choice touches the research (sources, cases, measures, samples, models, interpretation, scope, timeline). Do not fix it. Ask the student (Step 2).
3. **Spec question.** The reviewer marked it `SPEC-QUESTION`: the problem is in `SPEC.md`, not the plan. Explain it to the student. Change `SPEC.md` only with the student's approval, never silently, and note the change in the spec's history section.

The agent may also reject a finding when the evidence shows no real problem. Give the reason. Every finding gets a decision; none simply disappears.

## Step 2: Ask the student, a few at a time

Ask one to three questions at a time. For each:

```markdown
### Question about <finding>: <plain question>
Why it came up: <finding and spec IDs>
What it affects: <deliverables and tasks>

1. <Option A>: what you get, extra time or work, risk.
2. <Option B>: what you get, extra time or work, risk.
3. <Option C, only if really different>: consequence.
```

Give 2 to 4 options with honest consequences in both directions. On research choices, do not recommend an option. On purely technical matters the agent may say which option it would pick and why. Silence or "go ahead" is not a decision. Until the student answers, the affected tasks stay blocked.

For each student research decision, also add a pending entry to `docs/decisions.md` in that file's format, as `AGENTS.md` requires. The agent writes the question and the options. The student writes the decision and the reason.

## Step 3: Record the outcome in PLAN.md

Add a short findings table to `PLAN.md`:

| Finding | Decision | By whom |
|---|---|---|
| PR-03: T-05 uses a file nobody makes | Fixed: T-05 now depends on T-02 | Agent (mechanical) |
| PR-04: how to treat missing years | Student chose option 2 (D-002) | Student |
| PR-06: extra robustness table | Rejected: not in the spec | Agent, student agreed |

Update the tasks to match. Keep existing task IDs; give new work a new ID; mark a dropped task "removed" instead of deleting it.

## Step 4: Re-check the plan

A fix can break something else. After all edits, check again:

- Every deliverable and acceptance check has a task that makes it and a task that checks it.
- Every task input already exists in `RESOURCES.md` or comes from an earlier task.
- No task depends on itself through a chain of other tasks.
- No two tasks in the same group write the same file.
- Tasks waiting on an unanswered student decision are marked blocked.

## Step 5: Lock

Show the student `SPEC.md`, `RESOURCES.md` and `PLAN.md` together, with a short synopsis:

- what will exist at the end (the deliverables, in plain words);
- gaps that are still unresolved (missing data, open items);
- the points where the student must decide during the work;
- the first group of tasks to do.

Ask for an explicit "LOCK". Anything less is not a lock. On "LOCK", mark all three files `LOCKED` with the date. If the student uses Git, commit the three files together. Add a log entry in `agent-workspace/log.md` and update `agent-workspace/status.md`.

From now on, any change to the spec goes through `research-planning/stages/5-changes-and-final-check.md`.

**Optional.** Propose a short "Current plan" note for the project `README.md`: where the planning files are, which stage the project is in, and the next group of tasks. Write it only if the student approves the text.
