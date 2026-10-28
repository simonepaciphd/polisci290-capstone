# Stage 5: Changes and final check

This stage has two parts. Part A applies the whole time you carry out the tasks. Part B is the check at the end.

## Part A: Changes during the work

After the lock, `SPEC.md` is the agreed description of what the project will produce. The agent treats it as fixed unless the student approves a change. Research can still evolve when new evidence appears. Changes must be deliberate, written down, and understood.

### When to propose a change

Propose a change when, during a task, the agent finds that:

- a promised output looks impossible or much harder than planned;
- a new choice comes up that the spec does not settle;
- a check cannot be run the way the spec says;
- the work would add something the spec does not ask for;
- work already done differs from the spec.

First ask: is this really a spec change, or just a mistake in the code or plan? A mistake is fixed without changing the spec.

### How to propose a change

1. Pause only the tasks affected. Unrelated tasks may continue.
2. Add a change entry to `docs/planning/CHANGELOG.md` (format in `research-planning/templates/CHANGELOG.md`), numbered CHG-01, CHG-02, and so on. Never reuse a number. Each entry says:
   - what to change in the spec (IDs and wording);
   - why (the evidence found);
   - which deliverables and tasks are affected;
   - the alternatives, including "keep the spec as it is".
3. Present the entry to the student. For research choices, give the options and their consequences without recommending one.
4. The student approves or rejects. Record the answer and the date in the entry. If the change is a research choice, also add a pending entry to `docs/decisions.md` for the student to complete.
5. If approved, update `SPEC.md` and `PLAN.md` together so they do not contradict each other. Keep the old wording visible (mark it "replaced by CHG-02"). Re-check the affected tasks as in Stage 4, Step 4. If the student uses Git, commit both files together, naming the change.
6. If rejected, keep the entry with the reason. The affected task goes back to following the spec, or stays blocked.

The agent never quietly substitutes a different analysis. Silence or "go ahead" is not approval.

**Example.** A planned subgroup analysis turns out to have too few observations for meaningful estimation. The agent pauses that task, writes CHG-03, and proposes alternatives: change the subgroup definition, present descriptive results only, or drop the analysis. The student chooses. The agent does not pick one and carry on.

## Part B: Final check

The project is not done just because every task says "done". Before the student uses the outputs in the paper, the agent and student check the whole result against the final locked spec.

### 1. Compare each spec item with what exists

For every deliverable, requirement and acceptance check in `SPEC.md`, record one status:

- **Met**: the output exists and its checks passed.
- **Met as changed**: met under an approved change (name the CHG).
- **Not met**: missing or wrong.
- **Not verified**: there is not enough evidence to say.

Also confirm that open questions are resolved and that every student decision is recorded in `docs/decisions.md` in the student's words.

### 2. Trace each table and figure

For each table and figure, name the script that made it, the intermediate results it used, the original files in `input/`, and the approved choices behind it. An output that cannot be traced is "not verified".

### 3. Rerun from start to finish

Follow the documented steps in the project `README.md` from `input/` to `output/`. Write results to a separate, empty folder so earlier results are not overwritten. Compare the new outputs with the existing ones and note any differences.

### 4. Report openly

List every item that is not met or not verified, and every change made without approval. Show them to the student. Do not hide limits inside a chat. Never rewrite the spec afterward to match what happened. If something is unmet, it goes back to a task or to a new change entry the student approves.

### Completion checklist

- [ ] All outputs promised in `SPEC.md` exist.
- [ ] Each output is connected to its script, inputs and approved choices.
- [ ] Required checks have passed.
- [ ] Open questions are resolved or listed as limits.
- [ ] Student approvals and decisions are recorded.
- [ ] Every change has a CHG entry with the student's answer.
- [ ] Scripts and documentation let someone else reproduce the outputs.
- [ ] The final outputs are ready to use in writing the paper.

### Finish

Add a final entry to `agent-workspace/log.md` and update `agent-workspace/status.md`. Then remind the student to write the course AI-use disclosure in their own words, using `agent-workspace/log.md` as the record of what the agent did. The agent does not write the disclosure.
