---
name: research-planning
description: Help a student plan a capstone research project before doing the work - define the finished outputs, take stock of starting materials, write a plan of small checkable tasks, then carry it out in small groups. Use when the student says "plan my capstone", "help me plan this project", "write a spec for my paper", or asks to organize a research project with an AI agent.
---

# Research planning (student edition)

This skill helps a student plan a one-quarter capstone project in the order set out in the course Research Guide ("A Practical Guide to Organizing Research with AI Agents"). First decide what the finished project must contain. Then take stock of the materials already available. Then write an ordered plan of small tasks, each with a check. Only after the student approves all three does the real work start, in small groups of tasks. The student makes every research choice. The agent asks questions, drafts planning files, proposes options, and carries out agreed tasks.

**AGENTS.md wins.** The project's `AGENTS.md` sets the ground rules for every agent. Read it first. Where this skill and `AGENTS.md` disagree, follow `AGENTS.md`. The course syllabus and AI-use rules on Canvas are above both.

## Where files live

All planning files go in `docs/planning/` inside the student's project folder. Create the folder if it is missing. Use exactly these names:

- `docs/planning/brief.md` - the student's first description, saved as given (the spec reviewer reads it).
- `docs/planning/SPEC.md` - what the finished project must contain.
- `docs/planning/Spec-Review.md` - findings from the critical review of the spec.
- `docs/planning/RESOURCES.md` - the starting materials and what each one is used for.
- `docs/planning/PLAN.md` - the ordered list of small tasks, with inputs, outputs and checks.
- `docs/planning/Plan-Review.md` - findings from the critical review of the plan.
- `docs/planning/CHANGELOG.md` - every change to the agreed plan after it is locked.

Blank templates are in `research-planning/templates/`. Other records stay where `AGENTS.md` puts them: research decisions in `docs/decisions.md`, current task state in `agent-workspace/status.md`, one log entry per task in `agent-workspace/log.md`.

## Stages

| Stage | File produced | Must be true before moving on |
|---|---|---|
| 1. Specify | `SPEC.md` (draft) | Every deliverable has an ID and an acceptance check; open items are marked `OPEN`; no tools or tasks in it |
| Spec review | `Spec-Review.md` | Reviewed in a fresh chat; the student has answered each finding; the student says "approve" |
| 2. Resources | `RESOURCES.md` | Every deliverable is linked to materials or marked `UNRESOLVED`; the student approves |
| 3. Plan | `PLAN.md` (draft) | Every requirement has a task that produces it and a check that tests it |
| Plan review | `Plan-Review.md` | Reviewed in a fresh chat |
| 4. Decide and lock | `PLAN.md` (final); SPEC, RESOURCES, PLAN marked `LOCKED` | The student has decided every finding and approves the three files together |
| Carry out the work | outputs, `status.md`, `log.md` | Each task's checks were run and reported |
| 5. Changes and final check | `CHANGELOG.md` | Every promised output exists, traces back to its inputs, and can be repeated |

## Rules for every stage

1. **What before how.** Stage 1 describes the finished result only. No software, scripts or task order until Stage 3.
2. **No silent gap filling.** Read the project files first. If something is not stated by the student or a project file, mark it `OPEN-01`, `OPEN-02`, ... and ask. Never fill a gap with a plausible guess.
3. **Stable IDs.** Deliverables `OUT-01`, requirements `R-01`, acceptance checks `A-01`, constraints `C-01`, non-goals `N-01`, open items `OPEN-01`, tasks `T-01`, decisions `D-001` (numbered the way `docs/decisions.md` already numbers them), changes `CHG-01`. Never renumber an ID once used; retire it instead.
4. **Stage gates.** Do not start a stage until the student has approved the one before it. Do not start the real work until Stage 4 is locked.
5. **Independent reviews.** The two critical reviews happen in a fresh chat (or a subagent, if your tool has them) that sees only the raw files, not this conversation. If that is not possible, say so plainly.
6. **The student decides.** Offer options and what each one changes. Never pick a research choice yourself. Silence or "go ahead" is not a decision. Ask the student to record decisions and reasons in `docs/decisions.md` in their own words; you may add pending questions there.
7. **No prose for submission.** You may draft planning files, code, technical notes and tracking notes. Never write, paraphrase or restyle text the student will submit.
8. **No silent spec changes.** After the lock, the spec changes only through `CHANGELOG.md` with the student's approval.
9. **Keep it small.** This is a one-quarter paper. A typical spec has about 5-15 deliverables. Prefer fewer, plainer steps.

## Status of each planning file

Each planning file starts with a status line, so any session can tell where the work stands:

- `DRAFT` - being written; may change freely with the student.
- `APPROVED` - the student said "approve" at the end of its stage.
- `LOCKED` - approved together with the other two files at Stage 4; changes now go through `CHANGELOG.md`.
- `SUPERSEDED` - replaced because the goal changed; kept, not deleted.

Only the student's explicit words move a file to `APPROVED` or `LOCKED`. Record the date next to the status.

## Start

1. Read `AGENTS.md`, `README.md`, `docs/decisions.md` and `agent-workspace/status.md`. Briefly explain the ground rules back to the student.
2. Look in `docs/planning/`.
   - Empty or missing: start at Stage 1.
   - Files already there: do not restart. Find the last stage that was approved or locked (each file records its status) and resume at the next one.
3. Tell the student in one or two sentences which stage they are in and what that stage will produce.
4. Note in `agent-workspace/status.md` that planning is under way and which stage is current.

## Stage 1 - Specify

Follow `research-planning/stages/1-specify.md`. Interview the student about what the finished project must contain, draft `SPEC.md`, and run its completeness checks.

## Spec review

Follow `research-planning/stages/review.md` in **SPEC mode**. The review runs in a fresh chat given only the raw files. Write its findings to `Spec-Review.md`. The student answers each finding and approves the spec.

## Stage 2 - Resources

Follow `research-planning/stages/2-resources.md`. List the data, documents, code and software already available, link each deliverable to the materials it needs, and check for gaps in both directions.

## Stage 3 - Plan

Follow `research-planning/stages/3-plan.md`. Break the work into small tasks, each with inputs, outputs and checks, and write the draft `PLAN.md`.

## Plan review

Follow `research-planning/stages/review.md` in **PLAN mode**, again in a fresh chat. Write its findings to `Plan-Review.md`.

## Stage 4 - Decide and lock

Follow `research-planning/stages/4-decide-and-lock.md`. Go through the review findings with the student, finalize `PLAN.md`, and lock `SPEC.md`, `RESOURCES.md` and `PLAN.md` together. If the student uses Git, suggest committing the planning files at the lock.

## Carry out the work in small groups

The work is done one task at a time, or in a small group of related tasks done together.

1. Pick the next task (or small group) whose inputs are ready, in `PLAN.md` order.
2. Before each task, agree the plan in `agent-workspace/status.md` as `AGENTS.md` requires: goal, inputs, exact files to change, steps, expected output, checks. Wait for the student's approval.
3. Do only the agreed steps. Then end with a task report:
   - what changed;
   - input -> steps -> output;
   - checks run and their results;
   - uncertainties;
   - decisions needed.
4. Append a log entry to `agent-workspace/log.md` and update `status.md`.
5. Never mark a task done without its checks. If checks were not run, label the output "not yet checked".
6. If a question or problem comes up, pause only the tasks it affects and ask the student. If it changes the spec or plan, handle it through Stage 5.
7. Optional: if your tool supports several agents at once, tasks that do not touch the same files may run in parallel. One agent is always fine.

## Stage 5 - Changes and final check

Follow `research-planning/stages/5-changes-and-final-check.md`. Record every change to the locked plan in `CHANGELOG.md`, with the student's approval. At the end, check that every promised output exists, traces back to its inputs, and can be repeated.

## Common mistakes

- **Tools in the spec.** Stage 1 names software or methods the student did not require. Move them out.
- **Guessing to save time.** A missing fact becomes a plausible default instead of an `OPEN` item and a question.
- **Reviewing your own work.** The review runs in the same chat that wrote the draft. Use a fresh chat.
- **"Go ahead" as a decision.** A general approval is treated as a research choice. Ask the specific question.
- **"Done" without checks.** A task is marked complete because the code ran.
- **Quiet drift.** The work changes direction without a `CHANGELOG.md` entry.
