# Project 2 plan: what African AI policies commit to, and where they're vague

## The question

What do the AI strategies of Nigeria and a few other African countries actually commit to, and where are they vague? And does Nigeria's strategy match what Project 1 found about which jobs AI can do?

## Why this project

Project 1 shows I can test AI and measure work. This one shows I can read long policy documents, score them consistently, cite every claim, and write a clear comparison. That's the core of Research Analyst and AI policy roles, and it's what AI governance and EA-adjacent organisations look for. The two together make one body of work: what AI can do in Nigerian jobs, and what the government says it will do about it.

## Documents (status checked 2026-11-03; confirm each original before scoring)

| Country | Document | What we know | To confirm |
|---|---|---|---|
| Nigeria (anchor) | National AI Strategy 2025 to 2029 (FMCIDE / NITDA) | Published 2025; minister says it's final; non-binding | The official PDF; whether the National Assembly approved it; status of the Digital Economy and E-Governance Bill and the AI Commission Bill |
| Kenya | National AI Strategy 2025 to 2030 | Reported launched April 2025 | Find the PDF on the ICT ministry site |
| Rwanda | National AI Policy (MINICT, 2023) | Official PDF linked from MINICT | Download and confirm the version |
| South Africa | National AI Policy Framework (2024) | A framework, possibly still a draft | Whether a final policy exists; if it's only a discussion draft, swap in Egypt |
| Egypt (backup) | National AI Strategy, 2nd edition, 2025 to 2030 | English PDF found; six pillars; GDP and talent targets | Use only if South Africa's document is too thin |
| African Union | Continental AI Strategy (July 2024) | Official PDF on au.int, adopted by the AU Executive Council July 2024 | Download |

Rule: score only from the original document, never from news coverage. Record the URL, the date accessed and a SHA-256 checksum for each PDF. Keep the PDFs out of git (link to them instead), and store our page-numbered text extracts for checking.

## Rubric (10 criteria, 0 to 2 each)

Each criterion gets one sentence per level, published so readers can disagree.

| # | Criterion | 0 | 1 | 2 |
|---|---|---|---|---|
| 1 | Binding force | Strategy or vision only | Approved by cabinet or parliament, but not law | Law or regulation with legal force |
| 2 | Responsible body | No body named | A body named, but roles unclear or shared loosely | A named body with stated duties |
| 3 | Funding | No money mentioned | Funding mentioned with no amount or source | Amount and source stated |
| 4 | Measurable targets | No numbers | Numbers without dates, or dates without numbers | Numbered targets with deadlines |
| 5 | Jobs and workforce | Not covered | Skills goals only | Skills plus plans for affected workers (transition, protection) |
| 6 | Risk and safety | Not covered | General ethics principles | Specific risk measures (assessments, high-risk categories, testing) |
| 7 | Data protection link | Not mentioned | Mentions privacy in general | Ties to a named data protection law or regulator |
| 8 | Enforcement | None | Says rules will come later | Penalties or an enforcement process stated |
| 9 | Local language and context | Not covered | Mentioned as a goal | Concrete commitments (datasets, models, funding for local languages) |
| 10 | Monitoring and evaluation | None | Promises review with no method | Named indicators, reviewer and schedule |

Every score cites a page and a short quote (under 15 words). No page, no score.

## Steps

### 1. Get and confirm the documents (day 1)
Find each official PDF, check it's the current version, and record source details. Check the Nigerian bills' current status on the National Assembly and NITDA sites. Pick South Africa or Egypt.

### 2. Extract text with page numbers (day 1)
One text file per page, so every citation can be checked against the PDF page.

### 3. Score the documents (days 2 to 4)
No author time needed here. Instead:
- **Rater 1:** I score every document, each score with a page and a short quote.
- **Rater 2:** a fresh AI session scores the same documents from the same rubric and page texts, without seeing rater 1's scores. We report where the two agree and disagree, as in Project 1.
- **Citation check by script:** a script confirms every quoted phrase appears on the page it cites. Any quote that fails is fixed or the score is dropped.
- Disagreements between the raters get a short written resolution, which is published with the data.

### 4. Log vague commitments (days 3 to 5)
For each document, list promises with no owner, no number, no date or no money. Record: quote (short), page, and which of those four is missing. Aim for 5 to 10 per document.

### 5. AI safety check (day 5)
For each document, answer yes or no with a page: does it mention frontier model risks, model evaluation or testing, or incident reporting? Report the answer whichever way it goes. "None of them do" is a useful finding.

### 6. Link to Project 1 (day 6)
Pull every jobs and skills commitment from Nigeria's strategy. Set them beside Project 1's findings: which jobs are most exposed, the failures on local languages and facts, and data annotation being invisible to the big studies. Ask whether the strategy addresses the workers in those jobs.

### 7. Outputs (days 6 to 9)
- **Comparison matrix:** documents × 10 criteria, as a CSV and a heatmap chart.
- **Vague commitments table.**
- **Brief (2 to 3 pages):** plain English, five observations, a limitations section and "How I checked this".
- **Medium article,** a portfolio project page, and an update to the "Link to Nigeria's AI strategy" placeholder in Project 1's brief.

## Who does what

| Work | You | Claude |
|---|---|---|
| Find and confirm documents | Final say on which version | Search, download, checksums |
| Text extraction | | Page-numbered extracts |
| Scores | | Two blind AI scoring passes, citation-check script, written resolution of disagreements |
| Vague commitments | | Full list with pages |
| Safety check | | Full check with pages |
| Charts, brief, article | Read the final brief and article (about 30 minutes); own the voice | Draft, plain English, fact-check |

## Then: applications

Once Project 2 is out (about 10 days), we finish the push:

1. Two resume versions from the draft doc (AI Evaluation, and Research Analyst), with both projects.
2. A target list of 30 to 40 roles. Mix AI evaluation vendors (fast hiring), AI policy and research organisations, and remote analyst roles at African tech companies.
3. A short cover letter template that points to one finding from each project.
4. A LinkedIn post per project, in your short punchy style.

Keep applying to AI evaluation roles in the meantime. They hire fastest, and Project 1 is already enough to show.

## Open questions

1. ~~South Africa or Egypt?~~ Decided 2026-11-03: Egypt. South Africa's draft was withdrawn in April 2026 (see `sources/SOURCES.md`).

The brief will say plainly that two AI scoring passes produced the scores, that a script checked every citation against its page, and that the author reviewed the conclusions, not each score.
