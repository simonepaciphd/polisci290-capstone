# Stage 2: Take stock of your starting materials

Goal: list what already exists, connect each promised output in `docs/planning/SPEC.md` to the materials it needs, and find the gaps. The result is `docs/planning/RESOURCES.md`, written from `research-planning/templates/RESOURCES.md`.

**Start only after the student has approved `SPEC.md`.** If the spec is still a draft, go back to `research-planning/stages/1-specify.md`.

This stage involves a lot of looking around. If your tool supports it, the agent can do the exploring (step 2A) in a separate chat or a subagent and bring back only the results. That keeps the main chat short. One agent in one chat also works.

## 2A. Explore the project materials (read-only)

The agent looks through the project folder: `input/` (and `input/README.md`), `scripts/`, `output/`, `docs/`, plus any location the student names outside the folder (a course drive, a website, an archive). It starts from the places `SPEC.md` mentions and stops once each deliverable has likely inputs or a clear gap.

Rules for this step:

- **Look, do not touch.** Never move, rename, overwrite, delete or reorganize any file. Keep `input/` unchanged.
- **Open before describing.** Do not guess what a file contains from its name. If a file was seen but not opened, say so.
- **Ask about unclear files.** If the purpose of a file, which version is current, or who may access it is unclear, ask the student. Do not guess. Record unanswered questions as `OPEN-01`, `OPEN-02`, ...
- **No private data into the AI tool.** If a file may hold confidential or identifying material, stop and ask before opening it.

For each resource, record:

| Field | What to write |
|---|---|
| ID | `RES-01`, `RES-02`, ... (never renumber) |
| Location | Path relative to the project folder, or where it lives outside it |
| What it is | A dataset, script, codebook, document set, archive, interview notes, software, etc. |
| Contents | Main variables or topics; what one row, case or document represents |
| Coverage | Years, places, cases, variables or documents covered |
| Source and access limits | Where it came from; licenses, login, restricted or private material |
| Known problems | Missing years, changed definitions, unclear coding, duplicates, etc. |

For a qualitative project, resources are documents, archives, interview or field notes, search procedures and coding schemes. Coverage means which cases, time span and document types are included.

Also note where the agent looked and what it did not look at.

## 2B. Connect each output to its inputs

For every deliverable (`OUT-01`, `OUT-02`, ...) in `SPEC.md`, list the resources it needs: data sources, existing code, software, intermediate results, documents. The goal is that each finished result can be traced back to its starting materials. Example:

| Desired output | Starting materials | Issue to resolve |
|---|---|---|
| Table of descriptive statistics | Survey data; variable dictionary; existing cleaning script | Confirm whether the same sample restrictions apply to every column. |
| Main regression table | Clean analysis dataset; estimation script; model decisions | Clarify clustering and missing-data treatment. |
| Map of study locations | Geographic identifiers; boundary files; plotting code | Check that boundary definitions match the study years. |

## 2C. Look for gaps in both directions

1. **Outputs missing an input.** A planned analysis may need a crosswalk, a year of data, or a set of documents that is not there. For each, the agent lists the options: get or create the resource, change the deliverable, or mark it `UNRESOLVED`.
2. **Resources with no role.** For each, the agent suggests a label with a one-line reason: useful later, redundant, or out of scope.

The agent presents options and what each one changes. **The student decides each important gap.** A file that only looks like the missing input does not close the gap; list it as one of the options. Gaps the student has not decided stay `UNRESOLVED`. They are never treated as solved.

If a gap involves a research choice (for example, which source or which years to use), the agent may add it as a pending question in `docs/decisions.md`. Only the student writes the decision and the reason.

## 2D. Update the spec and get approval

1. The agent fills in `docs/planning/RESOURCES.md` from `research-planning/templates/RESOURCES.md`: the resource list, the output-to-input links, the gaps and the student's decisions.
2. The agent adds the resource IDs to each deliverable in `SPEC.md` and records the change in the spec's change history (what changed and why).
3. The agent shows the student both files and asks for approval. Silence or "go ahead" without reading is not approval. Mark both files approved only after the student says so.
4. Update `agent-workspace/status.md` and add a short entry to `agent-workspace/log.md`.

**Done when:** every deliverable has at least one linked resource or a recorded gap; every listed resource has a role or a label; no project file was moved or changed; the student has approved `RESOURCES.md` and the updated `SPEC.md`.

Next: `research-planning/stages/3-plan.md`.
