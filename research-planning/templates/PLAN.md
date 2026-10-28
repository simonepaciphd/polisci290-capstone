# PLAN: [project title]

Status: DRAFT | APPROVED | LOCKED | SUPERSEDED
Date: [YYYY-MM-DD]
Based on: docs/planning/SPEC.md ([status/date]) and docs/planning/RESOURCES.md ([status/date])

This file breaks the work into small tasks, each with a check. The agent updates task status here and in `agent-workspace/status.md`.

## Task groups, in order
A task group is a few tasks done together before you review them.

| Group | Tasks | Why this order |
|---|---|---|
| 1 | [T-01, T-02] | [e.g. inspect the data before any choices about it] |
| 2 | [T-03] | [fill in] |

## Task cards
Copy this card once per task.

### T-01: [short name]
- Objective: [one result you can see or check]
- Serves: [OUT-xx, R-xx, A-xx]
- Inputs: [e.g. input/county-data.csv (RES-01)]
- Outputs: [e.g. output/table-01.csv, scripts/01-clean.R]
- Depends on: [T-xx or none]
- Steps: [short plain list; no research choices hidden inside]
- Checks: [e.g. row counts before and after; open five source records and compare]
- Student decisions: [D-xxx in docs/decisions.md, or "none"; the agent stops until you decide]
- Status: planned | working | waiting for you | ready for your check | done

"Done" means the checks ran and you looked at the result.

## Coverage
Every deliverable and acceptance check in `SPEC.md` needs a task that makes it and a task that checks it.

| SPEC item | Producing task | Checking task |
|---|---|---|
| OUT-01 | [T-xx] | [T-xx] |
| A-01 | [T-xx] | [T-xx] |

## Review findings
From the plan review in `docs/planning/Plan-Review.md`. You decide each one.

| Finding | Disposition | Decided by |
|---|---|---|
| [short summary] | [accepted: plan changed / rejected: reason / deferred] | [student] |
