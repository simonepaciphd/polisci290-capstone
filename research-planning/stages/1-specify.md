# Stage 1: Specify what the finished project must contain

**Goal.** Write down, in `docs/planning/SPEC.md`, exactly what the finished capstone must contain: every table, figure, dataset, appendix item and supporting file, what each one shows, and how anyone can tell it is finished. This stage is about the destination, not the route. Do not choose software, code or task order yet.

**Output.** `docs/planning/SPEC.md`, built from `research-planning/templates/SPEC.md`. Use IDs from the first draft on: deliverables `OUT-01`, requirements `R-01`, acceptance checks `A-01`, constraints `C-01`, non-goals `N-01`, open items `OPEN-01`. Never renumber an ID once used.

**Rules for the agent in this stage.**
- First read what already exists: `README.md`, `AGENTS.md`, `docs/decisions.md`, any proposal or notes the student points to. Do not ask the student for facts you can read.
- The student decides every research choice (question, cases, measures, samples, models, interpretation). You may offer options and tradeoffs; you never pick one. Silence or "go ahead" is not a decision.
- Mark each line of the spec as `STUDENT` (the student said it), `SOURCE: <file>` (read from a file), or `OPEN` (not yet answered). Never fill a gap with a plausible guess.
- Do not write or rephrase prose the student will submit. The spec describes the paper's contents; it is not the paper.

## 1A. Get the student's first description

Ask the student to describe the project in their own words. It can be rough and incomplete. Ask for:
1. What they hope to learn (the research question) and their main argument, if they have one.
2. What evidence they expect to use (data, documents, cases, interviews).
3. What the final paper should show.
4. Planned descriptive statistics, models or tests, comparisons, robustness or sensitivity checks, figures, tables, and appendix materials, even if uncertain.

Save the description as given in `docs/planning/brief.md` so the reviewer can read it later.

## 1B. Interview in small batches

Read the description, then ask about what is unclear. Ask **3-5 questions at a time**, wait for answers, then continue. Cover, as relevant:
- **Unit of observation:** what one row or one case is (a country-year, a voter, a bill, a speech).
- **Years and cases:** which are included and which are excluded, and why.
- **Key concepts:** how each is defined and measured (for example, how "treatment" or "democratic backsliding" is coded).
- **Main comparison:** what is compared with what.
- **Primary outcome:** which result the paper mainly rests on.
- **Paper vs. appendix:** which results go in the main text and which in the appendix.
- **Revision trigger:** what evidence would make the student change the design or the argument.

Keep a running list of unanswered items as `OPEN-01`, `OPEN-02`, ... in the spec. If the student says "I don't know yet", record it as OPEN, note what it blocks, and move on. Any research choice the student makes also goes as a pending question in `docs/decisions.md`; only the student writes the decision and the reason there.

## 1C. Completeness checks before the review

Before the spec goes to review, check that every deliverable has:
1. an ID (`OUT-01`, ...) and, if useful, a short name such as TABLE-01 or FIGURE-03;
2. a one-line statement of what it shows;
3. the data and method it needs, at the level of the result (sample, years, comparison, model), not at the level of code;
4. the files it must produce (for example the figure, the numbers behind it, the script that makes it);
5. an acceptance check (`A-xx`) saying how to tell it is finished, in terms anyone can inspect.

Also check: no tools, packages or code choices appear (unless the course or the student fixed them; then they are constraints, `C-xx`); vague words like "robust" or "clear" are turned into something checkable or marked OPEN; plausible extras that are out of scope are listed as non-goals (`N-xx`). A typical capstone spec has about 5-15 deliverables.

Then hand the draft to the critical review: follow `research-planning/stages/review.md` in **SPEC mode**. The review saves `docs/planning/Spec-Review.md`.

## 1D. First complete spec

1. Go through each review finding with the student. For every finding that needs a research choice, present the options and tradeoffs; the student decides. Record what was decided in the spec and, for research choices, as pending entries in `docs/decisions.md`.
2. Fold the decisions into `docs/planning/SPEC.md`. Do not renumber IDs; add new ones.
3. Show the student a short, readable summary: what the finished project contains (five lines or fewer), the main fixed choices, the remaining OPEN items and what each blocks.
4. Ask for an explicit **APPROVE**, or for precise edits. Anything else (silence, "looks fine, keep going") is not approval. Do not start Stage 2 until the student approves. Open items may remain only if the student agrees they do not block planning.

The spec is not locked yet. It is locked together with RESOURCES.md and PLAN.md in Stage 4.

## Worked deliverable (adapted from the course guide)

```markdown
### OUT-03 (FIGURE-03): Event-study plot
- Shows: how the outcome changes in the years before and after the policy, relative to the comparison group. [STUDENT]
- Data and method: county-year panel, 2005-2020; event time -5 to +5 years; comparison group = counties never treated;
  omitted reference period = year -1; 95% confidence intervals; model as in OUT-02. [STUDENT]
- Sample: same sample as the main model (OUT-02). [STUDENT]
- Files: publication-ready figure in output/; the numerical estimates used to draw it (a table file in output/);
  the script in scripts/ that produces both. [STUDENT]
- A-03: plotted points match the stored estimates; rerunning the script recreates the figure from input/. 
- OPEN-04: whether to bin event times beyond +/-5. Blocks: final version of OUT-03.
```
