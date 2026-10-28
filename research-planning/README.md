# Research planning: a planning helper for your capstone

This folder is a set of instructions you give to an AI agent so it can help you plan your capstone the way the course Research Guide ("A Practical Guide to Organizing Research with AI Agents") describes. You first decide what your finished project must contain. Then you list the materials you already have. Then you write a step-by-step plan of small tasks, each with a check. The agent asks questions, drafts the planning files and points out gaps. You make every research choice.

## What you get at the end

Four plain-text planning files in `docs/planning/` inside your project folder:

- `SPEC.md` - what your finished project must contain, and how you will know each part is done.
- `RESOURCES.md` - the data, documents and code you start from, and what each one is for.
- `PLAN.md` - an ordered list of small tasks, each with its inputs, outputs and checks.
- `CHANGELOG.md` - a record of any change to the plan after you agree it.

The agent also writes two short review files (`Spec-Review.md`, `Plan-Review.md`) along the way.

## Install

Put the whole `research-planning` folder inside your project folder, next to `AGENTS.md`:

```text
my-capstone/
  AGENTS.md
  README.md
  research-planning/
  input/  output/  scripts/  docs/  agent-workspace/
```

## Start

Open your project folder in your AI tool and paste this as your first message:

```text
Read AGENTS.md, then read research-planning/SKILL.md and follow it to help me plan my capstone. Start with stage 1.
```

If you already started planning in an earlier session, use the same prompt. The agent should find your files in `docs/planning/` and pick up where you left off.

## Notes for different tools

- **Claude Code:** the prompt above works as is. Optionally, also copy the folder to `.claude/skills/research-planning/` so it loads as a skill.
- **Tools that cannot read files:** paste `SKILL.md` and the file for your current stage (in `research-planning/stages/`), plus your current planning files. Save the agent's drafts into `docs/planning/` yourself.
- **Reviews:** at two points the agent will ask you to open a fresh chat for an independent review. Do it; a reviewer who did not write the draft catches more.

## How long it takes

Expect a few sessions, not one sitting. Stage 1 (deciding what the project must contain) usually takes the longest, because it is where you make your own choices.

## What stays yours

All research choices: your question, argument, sources, cases, measures, samples, models and interpretation. All writing you submit. The agent proposes options; you decide and record your reasons in `docs/decisions.md` in your own words.

This helper is optional. The course AI-use rules apply, including disclosing meaningful AI use.
