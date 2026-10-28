# Critical review (two modes)

A second, independent reader checks the planning files before the student approves them. The reviewer acts as a **skeptical co-author**: its job is to find problems, not to agree. It **never rewrites** the files and **never chooses** a research option. It reports findings; the student decides what to do about each one.

- **SPEC mode** is used at the end of Stage 1, on the draft `docs/planning/SPEC.md`.
- **PLAN mode** is used at the end of Stage 3, on the draft `docs/planning/PLAN.md`.

## How to run the review independently (both modes)

An independent reviewer has not seen the conversation that produced the draft, so it cannot share the same blind spots.
1. Open a **fresh chat or session** with your AI tool (or, if your tool has them, start a **subagent**).
2. Give it only the raw files listed for the mode below, plus this file (`research-planning/stages/review.md`).
3. Tell it to work **read-only**: it must not edit any file.
4. Do **not** tell it what you expect it to find or which parts you are worried about. Use the copyable prompt below as is.
5. Bring its findings back to the main chat. The main agent saves them, unchanged, to `docs/planning/Spec-Review.md` or `docs/planning/Plan-Review.md`.

If a fresh session or subagent is not possible, the agent must **say so**, then do the review anyway as a clearly separate pass: re-read only the listed files, set aside its earlier reasoning, and note at the top of the review file "Not independent: same session as the draft."

## SPEC mode

**Inputs (only these):** the student's first description (`docs/planning/brief.md`), the draft `docs/planning/SPEC.md`, and any files the spec cites.

**Look for:**
- **Contradictions.** Example: the main model uses one sample (2005-2020, all counties) but a figure appears to use another (only treated counties, or different years). Requirements, constraints, non-goals or checks that conflict.
- **Missing pieces.** A deliverable without a statement of what it shows, without its data and method, without its files, or without a check. A result the description promises that no deliverable produces.
- **Infeasible data.** A planned analysis needs data that may not exist, may not be accessible this quarter, or is private. Propose alternatives.
- **Vague completion criteria.** Checks like "looks good" or "robust" that no one could verify.
- **Question fit.** Do the deliverables together actually answer the research question?

## PLAN mode

**Inputs (only these):** `docs/planning/SPEC.md` (approved), `docs/planning/RESOURCES.md`, and the draft `docs/planning/PLAN.md` with its task cards.

**Check that:**
- every deliverable (`OUT-xx`) and requirement (`R-xx`) has a task that produces it and a check that confirms it;
- every task's inputs either already exist (in RESOURCES.md) or are produced by an earlier task;
- there are no circular dependencies (task A waits for B while B waits for A);
- tasks are small enough to finish and check in one sitting ("prepare the data" is too broad);
- research choices are flagged as **student decisions** on the task card, not buried inside a task's steps;
- two tasks done at the same time (in the same group) never edit the same file.

If a problem lies in `SPEC.md` itself rather than in the plan, label the finding `SPEC-QUESTION`. Do not suggest rewriting the spec to fit the plan.

## Finding format (both modes)

Number findings `SR-01`, `SR-02`, ... in SPEC mode and `PR-01`, `PR-02`, ... in PLAN mode. Never renumber.

```markdown
### SR-01: <short title>
- Severity: critical | high | medium | low
- Where: <IDs and file, e.g. OUT-02, OUT-03 in SPEC.md>
- Problem: <what is wrong, quoting the exact line>
- Why it matters: <what would fail or be wrong if ignored>
- Possible fixes: <two or more options when a research choice is involved>
- Needs a student decision: yes | no
```

Severity: **critical** = a promised output cannot be produced or would be wrong; **high** = a major gap likely to cause failure; **medium** = a real weakness or wasted effort; **low** = small clarity issue. Do not inflate. No generic advice ("add more checks") without pointing at a specific item.

Start the review file with: inputs reviewed, whether the review was independent, a one-line verdict (ready / ready after fixes / needs student decisions), and the count of findings by severity. End with what the review did not check.

## Copyable reviewer prompt: SPEC mode

```text
You are reviewing a draft research specification as a skeptical co-author. Read research-planning/stages/review.md
and follow its SPEC mode. Your only inputs are: docs/planning/brief.md, docs/planning/SPEC.md, and any files SPEC.md
cites. Work read-only: do not edit, create or delete any file. Do not rewrite the spec and do not choose among
research options; offer options and say whether the student must decide. Report every finding in the format in
review.md, numbered SR-01, SR-02, ..., with the header and closing section described there.
```

## Copyable reviewer prompt: PLAN mode

```text
You are reviewing a draft research work plan as a skeptical co-author. Read research-planning/stages/review.md
and follow its PLAN mode. Your only inputs are: docs/planning/SPEC.md, docs/planning/RESOURCES.md and
docs/planning/PLAN.md. Work read-only: do not edit, create or delete any file. Do not rewrite the plan and do not
make research choices; offer options and say whether the student must decide. Report every finding in the format
in review.md, numbered PR-01, PR-02, ..., with the header and closing section described there.
```

After the review, the main agent saves the reviewer's text unchanged to the review file. The findings are then resolved with the student: SPEC findings in Stage 1D (`research-planning/stages/1-specify.md`), PLAN findings in Stage 4 (`research-planning/stages/4-decide-and-lock.md`).
