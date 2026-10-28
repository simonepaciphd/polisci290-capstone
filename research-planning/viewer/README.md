# Plan viewer

Turns your planning files into one page you can open in a browser: your tasks in their groups, what each task uses and checks, and the deliverables they lead to. It is optional. It reads your planning files and never changes them.

## Make the page

From your project folder:

```text
python research-planning/viewer/plan_viewer.py docs/planning
```

This writes `docs/planning/Plan-Visual.html`. Open it in any browser; it needs no internet. Build it again after any change to the plan. Do not edit the page by hand.

You need Python 3.8 or newer and nothing else. On Windows, if `python` is not found, try `py`.

To list problems without writing the page, add `--check`.

## What it reads

- `SPEC.md`: the title, the research question and the Deliverables table.
- `RESOURCES.md`: the Resources table.
- `PLAN.md`: the task groups table and the task cards (Objective, Serves, Inputs, Outputs, Depends on, Steps, Checks, Student decisions, Status).

Files written from the templates in `research-planning/templates/` work as they are. A task card can use `- Field: value` lines, as in the template, or plain `Field: value` lines, as in the example in `stages/3-plan.md`.

## Messages

`ERROR` means the page was not built:

- `E-NO-VERIFY`: a task has no checks.
- `E-UNKNOWN-REF`: a task names a task, deliverable (`OUT-..`) or resource (`RES-..`) that does not exist.
- `E-CYCLE`: tasks wait on each other in a loop.
- `E-SCHEDULE`: a task sits in an earlier group than a task it waits on.
- `E-STRUCTURE`: a file, section, table or ID is missing or malformed.

`WARN` means the page was built, but something may be off: a deliverable no task serves (`W-NO-PRODUCER`), a task in no group (`W-NO-GROUP`), or a task that uses another task's output without listing it under "Depends on" (`W-INPUT-DEP`). Warnings also appear at the bottom of the page.
