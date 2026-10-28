# Stage 3: Write the plan of small tasks

Goal: turn the approved spec into an ordered set of small tasks, each with its inputs, outputs and checks. The result is a draft `docs/planning/PLAN.md`, written from `research-planning/templates/PLAN.md`, with status `DRAFT`.

**Start only from an approved `SPEC.md` that already has resource links**, and an approved `docs/planning/RESOURCES.md`. If either is missing, go back to `research-planning/stages/1-specify.md` or `research-planning/stages/2-resources.md`.

This stage plans the work; it does not do it. The agent may read files but must not edit data, write analysis code or run anything yet.

If planning reveals a missing research choice, do not hide it inside a task. Add it as a pending question in `docs/decisions.md` and list it in the plan as an open item. If it reveals a missing input, send it back to `RESOURCES.md` as a gap.

## 3A. Identify the main parts of the work

Start with broad activities. For a quantitative project, typically:

1. Get and inspect the data.
2. Clean and combine sources.
3. Construct measures.
4. Produce descriptive results.
5. Run the models.
6. Run extra checks (sensitivity, alternative samples).
7. Make tables and figures.
8. Assemble materials for the paper (the student writes the paper itself).

For a qualitative project, the equivalents are: collect documents; code or categorize them; compare cases; build evidence tables.

Note which activities can happen at the same time (for example, cleaning two unrelated sources) and which must wait (models wait for the cleaned data).

## 3B. Break activities into small tasks

Each task should be small enough to finish and check in one sitting with clear instructions. "Prepare the data" is too broad. "Merge county-year unemployment rates into the county-year analysis file and report unmatched records" is a workable task.

Give each task an ID (`T-01`, `T-02`, ...; never renumber) and fill in:

- **Objective:** one sentence on what the task achieves.
- **Inputs:** exact files, as resource IDs (`RES-..`) or outputs of earlier tasks.
- **Outputs:** exact files it creates, in `output/`, `scripts/` or `agent-workspace/`. Never in `input/`.
- **Depends on:** tasks that must finish first because their output is an input here. Do not add a dependency just to impose an order.
- **Steps:** a few plain-language steps.
- **Checks:** how we will know it worked (see 3C).
- **Student decisions needed:** research choices the student must make before or during the task.
- **Serves:** the spec items it helps produce or check (`OUT-..`, `R-..`, `A-..`).

## 3C. Decide the checks before doing the task

Write concrete checks now, before anyone carries out the task. Not "check it is correct", but things like: no duplicate IDs; row counts before and after; a list of unmatched records; values within plausible ranges; the sample matches the spec; the figure's points match the saved estimates; rerunning the script gives the same output.

Mark each check as:

- **Automatic:** a script or count can confirm it.
- **Student judgment:** only the student can decide (for example, whether a coding rule fits the concept). These become decisions on the task card.

Example task card (from the course guide):

```text
### T-07 — Merge two panel datasets
Objective: Add annual unemployment to the county-year analysis file.
Inputs: Clean county-year panel (output of T-05); annual unemployment data
  (cleaned by T-06 from RES-04).
Action: Merge by county and year, without altering the source files.
Outputs: A new analysis dataset in output/ and a merge summary.
Depends on: T-05, T-06.
Checks (automatic): no duplicate county-year keys; unmatched records listed;
  observation counts before and after explained; unemployment values within
  plausible bounds.
Student decision: How to handle counties with missing years, if the answer
  changes the study sample.
Serves: OUT-02, R-03, A-04.
```

## Group the tasks

Put tasks into small ordered groups. A group is a set of tasks done together, then checked by the student before the next group starts. Give each group a one-line reason. For example:

| Group | Tasks | Reason |
|---|---|---|
| 1 | T-01 to T-04 | Get and inspect each source; they do not depend on each other. |
| 2 | T-05 to T-07 | Clean and merge; needs the inspection results and a student decision on missing years. |
| 3 | T-08 to T-10 | Measures and descriptives; need the merged file. |
| 4 | T-11 to T-13 | Models, tables and figures; need the measures. |

Place tasks that need a student decision early in a group, so the rest is not waiting at the end. Keep groups small enough for the student to check in one sitting.

## Check the plan before review

1. **Coverage check.** Every deliverable (`OUT-..`), requirement (`R-..`) and acceptance check (`A-..`) in `SPEC.md` has at least one task that produces it and one task or check that verifies it. List anything uncovered.
2. **Dependency check.** No task uses an output that a later task creates. No loops (T-03 waits for T-05, which waits for T-03).
3. **Inputs check.** Every task input is a listed resource, an earlier task's output, or something the student will supply. Inputs marked `UNRESOLVED` in `RESOURCES.md` block their tasks; mark those tasks blocked.
4. **Final task.** Include a last task that reruns the whole chain from `input/` into a separate, empty output folder and compares the results. This supports the final check in `research-planning/stages/5-changes-and-final-check.md`.

Fix what the agent can fix mechanically. Anything that needs a choice goes to the student.

## Save and hand off

1. Write `docs/planning/PLAN.md` from `research-planning/templates/PLAN.md` with status `DRAFT`.
2. Update `agent-workspace/status.md` ("waiting for you") and add a short entry to `agent-workspace/log.md`.
3. Show the student the plan in plain language: the groups, the decisions they will need to make, and anything uncovered or blocked.

**Done when:** every task has inputs, outputs, dependencies, checks and spec links; coverage and dependency checks pass or their problems are listed; nothing has been carried out.

Next: critical review of the plan, `research-planning/stages/review.md` in PLAN mode. Do it in a fresh chat or subagent if your tool allows it. The plan stays `DRAFT` until `research-planning/stages/4-decide-and-lock.md`.
