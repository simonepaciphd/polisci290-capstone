# Working with an AI agent: a small, visible research folder

An **AI agent** is an AI tool that can take several steps for you, such as reading files, editing code, and running an analysis. That makes it useful, but also makes it easy to lose track of what happened. The aim here is simple: **you direct the research; the agent helps carry out tasks you understand and approve.**

This is an optional setup, not an extra assignment or a requirement to use AI. The [course AI-use rules](polisci290-ai-use-and-disclosure.md) still apply: submitted prose must be your own, sources and results need checking, and meaningful AI use needs disclosure. The syllabus and Canvas remain authoritative.

## 1. Start with one folder

Download the [starter folder](../replication-starter.zip), unzip it, and rename `replication-starter` to something like `my-capstone`. You can also copy the [`replication-starter/`](../replication-starter/) directory from the repository. Keep the whole project together:

```text
my-capstone/
  README.md                 Your project map and instructions for repeating the work
  AGENTS.md                 Rules you give every AI agent
  input/                    Original data, documents, and source notes
  output/                   Generated tables, figures, and prepared data
  scripts/                  Code that turns inputs into outputs
  docs/                     Your writing and your research decisions
  agent-workspace/           Agent status, work log, and temporary work
```

The `.md` files are plain text with headings. You can read and edit them in a text editor; you do not need a special app, terminal commands, or Git to use this folder. GitHub is just where you get the starter. You do not need to upload your project to GitHub.

**Replication** means someone can follow your instructions and repeat the steps that produced a result. A folder helps only if you also record where the evidence came from, which steps used it, and how you checked the result. For a qualitative project, inputs can be public documents, scripts can be documented search or coding procedures, and outputs can be evidence tables. Do not add code just to fill a folder.

### Set it up yourself first (about ten minutes)

1. **You:** In `README.md`, write your question, your current expectation, and the next small task in your own words. It is fine to mark things undecided.
2. **You:** Put permitted source files in `input/`. In `input/README.md`, record where each came from, when you got it, and what it covers. Keep originals unchanged. Do not put confidential, private, or identifying material into an AI tool or a public repository.
3. **You:** Read `AGENTS.md`. These are the agent's ground rules. Do not ask the agent to weaken them so it can finish faster.
4. **You:** Start `docs/decisions.md` with the research choices you have already made and why. Leave open choices pending.
5. **With AI (optional):** Open the project folder in your tool. Explicitly ask it to read `AGENTS.md` and the project map. If it cannot access files, attach or paste those files and maintain the tracking pages yourself. Do not assume a particular tool automatically reads an instruction file.

Instructions are not a technical lock. Limit the tool's file access and permissions where available, read its proposed actions, and check the files it actually changed. Start with one agent and one small task at a time.

## 2. Keep research choices with you

The agent may explain alternatives and their consequences. **It must not select an answer on your behalf, treat silence as approval, or turn a suggestion into an approved research choice.**

| The agent can carry out an agreed task | You must decide first |
|---|---|
| List columns and count missing values | What a concept means and how to measure it |
| Implement your written inclusion rule | Which cases, years, or sources belong in the study |
| Report duplicates or merge failures | Whether to remove, combine, fill in, or recode observations |
| Run the comparison or model you chose | Which comparison, coding categories, model, or test answers your question |
| Draw the figure you specified | Which evidence to emphasize and what to claim from it |
| Flag a possible mistake or rival explanation | How to interpret the evidence and revise your argument |

“Clean the data” is too broad. A choice can look technical and still change the research: treating a blank as zero, deleting an outlier, changing a date range, or selecting a merge rule can change your findings. If the task is unclear, the agent should stop and explain the choice in everyday language.

For a pending choice, ask for: **the question, the available options, what each changes, and what evidence would help you choose.** Discuss it with the instructor if needed. Then write your choice and reason in `docs/decisions.md`, in your own words, and tell the agent which recorded decision to implement. A general “go ahead” does not authorize new research choices discovered later.

The agent may draft code, technical documentation, and tracking notes. It may give feedback on your writing. It must not write, paraphrase, or restyle the assignment prose you submit as your own.

## 3. Give one bounded task

Use this prompt after you have made your own first attempt:

```text
Read AGENTS.md, README.md, docs/decisions.md, and agent-workspace/status.md.
My goal for this session is: [one small task].
The research decisions I have already made are: [decision IDs, or none yet].
You may work with these files: [names].
The expected result is: [one checkable output].

Before editing or running anything, explain your plan in plain language:
what you will read, what you will change, what the result will tell me,
and how we will check it. Put that plan in the status page and wait for
my approval. Flag any research choice I still need to make.
Do not write my assignment prose. Do not make research choices for me.
```

A good first task: “Using `input/county-data.csv`, list the columns, count rows and missing values, and save a report to `agent-workspace/data-check.md`. Do not drop, fill in, or recode anything.”

After reading the plan, approve its exact scope or revise it. The agent can then complete the agreed mechanical steps without asking about every line of code. It must pause again for a new research choice, an unexpected problem, or work beyond that scope.

## 4. Monitor three small records

| Record | What it tells you | Who maintains it |
|---|---|---|
| `agent-workspace/status.md` | What is happening now, what is waiting for you, and what comes next | Agent updates; you read it before approving more work |
| `agent-workspace/log.md` | What happened in each work session: request, files changed, checks, unresolved issues | Agent appends; you check against the actual files |
| `docs/decisions.md` | Which research choices you made, why, and which are still pending | You own and write the decisions; agent may add clearly marked pending questions |

The status page should say **planned**, **working**, **waiting for you**, or **ready for your check**, with the last update time. It should name the actual task and files. “Done” without a check is not enough. The agent updates it before starting, when it pauses or changes course, and when it finishes an agreed task. These are written records, not a live activity monitor: an old status does not prove an agent is still working.

Keep the log short: one entry per bounded task, plus an entry when the plan changes or an attempted run fails. Save useful prompts or chat exports in `agent-workspace/` when permitted; record the tool/model and enough detail to explain its contribution. You do not need a transcript of every keystroke.

**Example:** The agent finds 12 counties with missing outcomes. It records the count and pauses, leaving the data unchanged. You decide to exclude those counties for a particular comparison, explain the limitation, and record D-002. The agent implements D-002 in a script, reports the row counts before and after, and points you to the affected table. You check several counties yourself before using the table. It does not try other exclusions to obtain a preferred result.

## 5. Be able to explain the whole chain

Before accepting an output, close the chat briefly and answer these in your own words:

1. What question is this step helping me answer?
2. Where did the evidence come from, and what does one row, case, or document represent?
3. What did we do to it, which observations changed, and which choices were mine?
4. Which script or written procedure produced this table or figure, and what checks did we run?
5. What does the result support, what does it leave uncertain, and what can it not establish?

You do not need to explain every line of code. You do need to understand the main steps, the assumptions, and why a check would catch a plausible mistake. Ask for a small worked example if you cannot explain a transformation. If you cannot explain an output or its limits, keep it marked **not yet checked** and do not use it as evidence in your submission yet.

Have the agent end each task with: **what changed; the input → steps → output path; checks actually run and their results; uncertainties; decisions needed; the next small step.** “The code ran” does not establish that the analysis is right. Spot-check source records, totals, joins, coding, and figure labels yourself, as appropriate. Verify sources by opening and reading them.

## 6. Make the result repeatable

Before a milestone, update the project `README.md` so another person can:

- Find the inputs, their sources, and any access restrictions.
- See the script or procedure order and the exact commands or manual steps, starting from the project folder.
- Identify the software, versions, and extra packages needed. Record a fixed random seed if the procedure uses random draws.
- Connect each important result to its input files, script/procedure, and approved decisions.
- Repeat the work into a separate, empty output folder and compare the expected results, without changing the originals. Record what was actually rerun and any differences.

For a manual evidence table, document the document list, search terms, inclusion and coding rules, and source page references instead. A restricted source may require access instructions rather than a shared copy; do not claim that someone without that access can fully reproduce it.

Write your milestone in your own words and use the work log to prepare your [AI-use note](polisci290-ai-use-and-disclosure.md#ai-use-note-template-suggested-format). The folder and logs support your explanation; they do not replace your judgment or your responsibility for the work.

## Going further: plan your project with an agent

Once your folder is set up, you can also use an agent to plan the whole project before you start the analysis.

- **Read the approach.** The [Research Guide (PDF)](../research-guide/Agentic_Research_Workflow_Research_Guide.pdf) explains it in three moves: decide what the finished project must contain, list what you already have, then plan small tasks that each come with a check.
- **Give your agent the steps.** The research-planning skill turns that approach into steps your agent follows. Download [`research-planning.zip`](../research-planning.zip) and unzip it into your capstone folder, next to `AGENTS.md`. It comes from a larger public system, [ai-os-public](https://github.com/simonepaciphd/ai-os-public), if you are curious.
- **Start with one prompt.** Paste this into your tool: `Read AGENTS.md, then read research-planning/SKILL.md and follow it to help me plan my capstone. Start with stage 1.`
- **Keep the choices yours.** You make every research choice and write every word you submit. The course AI-use rules still apply. This step is optional.
