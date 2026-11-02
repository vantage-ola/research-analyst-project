# Exposure rubric (v1)

Every task in `tasks.csv` gets one score. The score answers one question:

> Can a current LLM-based tool do this task, to a standard a paying client would accept, with a person only reviewing it?

This is a claim about what the technology can do. It is not a forecast of job losses, and it ignores whether a given Nigerian worker can afford or reach the tool. Access barriers are recorded separately (see "Barriers").

## Scale

| Score | Label | Definition |
|---|---|---|
| 0 | Not exposed | An LLM tool cannot do a meaningful part of this task today, so a person still does the core work. |
| 1 | Partly exposed | An LLM tool can do part of the task or noticeably cut the time, but a person must do or closely check a large share. |
| 2 | Largely exposed | An LLM tool can produce output a client would accept after light review, with a person doing little beyond checking it. |

## What counts as "an LLM tool"

- A frontier chat model available in the paid or free tiers as of the scoring date (record it in the scores file), with text, image, file, and audio input where the vendor supports them.
- Basic built-in tools: web search, code execution, file reading.
- Not counted: custom software built around the model, fine-tuning, or agents that need engineering work to set up. Anything that needs a physical presence, a live phone line, or being a particular person also counts as outside the tool.

## Decision rules

Apply in this order and stop at the first rule that fits.

1. **Needs physical presence or a body** (visiting a home, handling cash): score 0.
2. **Live and real-time with a person** (a phone call, a live tutoring session, interpreting a live conversation): score 0 or 1. Use 1 only if a large preparatory or follow-up part of the task is exposed by itself.
3. **Output is text, code, a table, an image, or a translation a person reviews afterwards**: go to rule 4.
4. **Could a client accept the first draft after a short check?** Yes: 2. Needs real editing or checking of facts: 1. Needs the person to do the core work: 0.
5. **The task needs knowledge the models handle badly** (for example, Yoruba, Igbo, Hausa, Pidgin, Nigerian accents, Nigerian tax rules): score what the models can do now, judged from a test run where one exists. Do not assume. If you have not tested it, score from your best judgment and mark `confidence = low`.

## Barriers (recorded, not scored)

Each task gets a second tag set, so readers can see where exposure and real-world use might differ:

- `payment`: tool or client requires a foreign card or account
- `connectivity`: needs stable high-bandwidth connection or power
- `language`: depends on languages or accents where models are weaker
- `informal`: work depends on trust, referral, or informal client relationships
- `regulatory`: depends on local rules a model may not know
- `none`

A task can carry more than one tag.

## Edge cases

- **Mixed tasks.** If a task has several steps, score the step that takes most of the time. Say which in the reason column.
- **Quality bar differs by client.** Score for an ordinary paying client, not the most demanding one.
- **Task is done in a different way now.** Score what the task is, not the current method (for example, "transcribe audio" is scored on the outcome, not on typing).
- **You have never done the task.** Say so in the reason column and set `confidence = low`.

## Worked examples

| Task | Score | Reason |
|---|---|---|
| CS03 Log and categorise tickets in a helpdesk tool | 2 | Classification and summary from text; a person only spot-checks. |
| CS05 Take live voice calls with customers | 0 | Real-time voice with an unpredictable person; a human still has to be on the call. |
| BK05 Prepare VAT and withholding tax returns | 1 | A model can draft the calculation, but a person must check Nigerian rules and file the return. |
| WD07 Integrate Paystack or Flutterwave payments | 1 | A model writes most of the code, but the person tests it against the live sandbox and handles credentials. |
| TR04 Transcribe audio with Pidgin or code-switching | 1 | Models produce a draft, but errors are frequent enough that a speaker must correct it. (Revise after the test run.) |

These examples are my starting guesses. Replace them with your own once you have scored.

## Scores file format (`scores_author.csv`)

`task_id, score, reason (one line), confidence (low|med|high), barrier_tags, scoring_date, model_in_mind`

## Model output quality scale (step 4 of the plan)

For tasks run through models, rate each output on a separate 1 to 4 scale. Rate blind: outputs are shuffled and model names are hidden until all ratings are in.

| Rating | Meaning |
|---|---|
| 1 | Unusable: wrong, off-task, or would harm the client if sent. |
| 2 | Heavy edits needed: right direction, but a person redoes most of it. |
| 3 | Light edits needed: a person fixes small errors and style. |
| 4 | Client-ready: a person only reads it and sends it. |

Use the same scale for every task. Ratings 3 and 4 support a score of 2; rating 2 supports a score of 1; rating 1 supports a score of 0 or 1.

## How this differs from published measures

Readers will compare this to existing studies, so these differences go in the brief:

- **"GPTs are GPTs" (Eloundou et al.)** labels a task exposed if an LLM, or software built on one, cuts the time to do it by at least half at the same quality. Its E1 and E2 labels split those two cases. This rubric uses an acceptance standard instead of a time saving, and excludes custom-built software.
- **ILO generative AI exposure index** scores whole occupations (ISCO-08) from task scores. This rubric scores tasks and averages them by category, so the units are different.
- **Anthropic Economic Index** measures observed use of one model, not what could be done.

When the three disagree with this rubric, the first thing to check is whether the definitions, not the tasks, explain it.

## Rubric version and change log

- v1: first draft. Any change after scoring starts must be logged here with the date and what was rescored.
