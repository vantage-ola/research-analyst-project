# Project 1 plan: Nigerian remote work and LLM exposure

## Why this project first

It is the strongest fit for the role that pays fastest. AI evaluation and data quality roles (annotation vendors, eval teams) want three things: a written rubric, consistent scoring of model output, and agreement checks between raters. This project does all three in public. The same work also reads as research (Research Analyst), survey design (Market Research), and data cleaning (Operations).

## Target roles, ranked by money and ease

| Rank | Role | Why | Typical remote pay |
|---|---|---|---|
| 1 | AI Evaluation Analyst / data quality | Hires fast, remote, Nigeria-friendly, your CS + rubric background already matches. Coding-eval tracks pay most. | $15 to $50/hr contract, $1.5k to $4k/mo full-time |
| 2 | Research Analyst (AI policy, think tanks, EA orgs) | Best long-term fit for AI safety, but slower hiring and more competition. Project 1 + 2 together are the ticket. | $2k to $5k/mo |
| 3 | Operations Analyst / data quality | Steady demand at remote startups. Needs SQL and spreadsheet evidence. | $1.2k to $3k/mo |
| 4 | Market Research Analyst | Local roles pay below target in USD. Remote foreign roles want domain experience. | Varies, often under $1.5k locally |

Ranges are rough market estimates, not verified quotes. Check live postings before relying on them.

Do not wait for the project to finish before applying to rank 1. Those pipelines take 1 to 3 weeks and the project can be added to applications as it lands.

## Repo layout

```
job-exposure/
  PLAN.md
  data/
    categories.csv        # 12 categories, why each is included
    tasks.csv             # task_id, category, task text, onet_task_id (if mapped), nigeria_adjustment
    rubric.md             # 0/1/2 definitions, one sentence each, plus edge-case notes
    scores_author.csv     # your scores, with a one-line reason per task
    model_runs/           # prompts, raw outputs, per model, per task
    model_ratings.csv     # quality rating of each output
    survey_responses.csv  # anonymised worker ratings
    external/             # GPTs-are-GPTs task data, ILO index, Anthropic Economic Index
  analysis/
    analysis.py           # joins, agreement stats, rankings, charts
  output/
    ranked_table.csv
    chart_1_exposure_by_category.png
    chart_2_author_vs_workers_vs_studies.png
    brief.md              # 3 to 4 pages
```

## Steps

### 1. Categories (day 1)
12 categories: customer support, data annotation, content writing, virtual assistance, bookkeeping, transcription, translation (English to Yoruba/Igbo/Hausa/Pidgin and back), graphic design, online tutoring, entry-level web dev, social media management, and one Nigeria-specific pick (e.g. remote sales/lead gen or forex/crypto community moderation). Record why each is in, ideally with a source (Upwork/Fiverr category counts, NBS or Jobberman reports).

### 2. Tasks (days 1 to 3)
5 to 8 tasks per category, about 72 total. Start from O*NET task statements and keep the O*NET task ID wherever there is a match, because that ID is the join key to the published studies. Add a `nigeria_adjustment` column for every change, e.g. "client communication over WhatsApp voice notes", "invoicing in naira and dollars via Payoneer/Grey", "transcribing Nigerian-accented English". I can draft the list; you edit it, since your judgment on what Nigerians actually do is the point.

### 3. Rubric and author scores (days 3 to 4)
- 0 = not exposed: an LLM cannot do a meaningful part of this task today without a human doing the core work.
- 1 = partly exposed: an LLM can do part of the task or cut the time noticeably, but a human must do or check a large share.
- 2 = largely exposed: an LLM can produce output a client would accept with light review.

Score all tasks yourself with a one-line reason each. Then score a 20-task subset again a week later without looking, to report your own test-retest consistency. That is a data quality number reviewers like.

### 4. Model tests (days 4 to 8)
- 2 to 3 tasks per category, about 30 tasks.
- 3 models via OpenRouter (one Claude, one GPT, one Gemini or open-weight model like Llama/Qwen, since cost matters to Nigerian freelancers).
- Realistic inputs: a messy customer complaint, a Pidgin voice-note transcript, a bookkeeping CSV with naira entries. Save prompt, model, date, and raw output.
- Rate each output on a 1 to 4 quality scale (unusable / needs heavy edits / light edits / client-ready). Rate blind: shuffle and hide model names before you rate.
- Optional: an LLM judge as a second rater, reported separately, with your agreement against it. Your ratings stay the primary evidence.

### 5. Worker validation (days 3 to 14, runs in parallel)
- Google Form per category: worker rates the same tasks 0/1/2, plus "how many hours a week do you spend on this", "do you already use AI for it", and one free-text question.
- 10 to 15 people across 12 categories is about one per category, which is too thin to compare. Aim for 2 or more per category in at least 8 categories (20 to 25 responses). Where a category has fewer than 2, say so in the table.
- Recruit through your communities, X, WhatsApp freelancer groups, and annotation worker Discords. No names in the data.
- Report agreement as weighted Cohen's kappa (you vs. workers) and simple percent agreement. Disagreements go in the brief as findings.

### 6. Compare with published research (days 8 to 12)
- Eloundou et al., "GPTs are GPTs" (task-level labels published on GitHub, keyed by O*NET task ID): join directly on your mapped tasks.
- ILO generative AI exposure index (Gmyrek, Berg, Bescond 2023, and the 2025 refined index): occupation-level, ISCO-08. Map your categories to ISCO codes.
- Anthropic Economic Index: observed Claude usage by O*NET task. Shows real use, not just possibility. A good third reference and a signal to AI-lab employers.
- Explain differences with concrete causes: payment barriers (no direct access to some paid AI tools), connectivity and power costs, Nigerian languages and accents, informal client relationships, price sensitivity of clients.

### 7. Analysis and outputs (days 12 to 16)
- Ranked table: category, mean task exposure (yours), worker mean, GPTs-are-GPTs mean, ILO score, model quality mean, n workers.
- Chart 1: exposure by category, task-level dots with category mean.
- Chart 2: your score vs. worker score vs. published score per category (dumbbell chart).
- Brief (3 to 4 pages): question, method, results, where studies fit and where they do not, limitations, "how I verified this". State plainly that scores show technical exposure, not job losses.

### 8. Publish (days 16 to 20)
- Repo public on GitHub with data and code.
- Medium post (shorter, chart-led), cross-posted to `~/dev/me/content/posts/`.
- Project page at `~/dev/me/content/projects/nigeria-ai-exposure.md`, same frontmatter as `igopay.md`.
- LinkedIn post with chart 1.

## Who does what

| Work | You | Claude |
|---|---|---|
| Category and task lists | Final edit, Nigerian context | First draft, O*NET mapping |
| Author scores | All of them | Nothing; this must be yours |
| Model runs | Approve prompts and inputs | Script the OpenRouter runs, save outputs |
| Quality ratings | All of them, blind | Shuffle and anonymise outputs |
| Survey | Recruit people | Draft form, clean responses, stats |
| Published data | Read the papers' methods sections | Download, map, join |
| Charts and table | Review | Build |
| Brief and Medium post | Own the argument and voice | Edit, fact-check, tighten |

Rule: no human data is synthetic. If a number came from a person, a real person gave it.

## Resume changes after Project 1

- Headline: "Research and AI Evaluation Analyst" (or a version per role), software background as the support, not the lead.
- Summary: rubric design, model output evaluation, inter-rater agreement, survey data, written briefs.
- Add a "Research" section above Projects with this project: "Scored 72 tasks across 12 Nigerian remote job categories with a published rubric; tested 90 model outputs across 3 LLMs; validated against N worker ratings (weighted kappa X)."
- Reframe Citu/Meta bullets toward data quality, testing, documentation, review. The 50,000-record testing and code review work already fit.
- Cut the long frontend/UI skill block; add Python (pandas), SQL, Google Sheets, survey design, inter-rater reliability.
- Two versions: AI Eval/Data Quality, and Research Analyst.

## Open questions

1. Which 12th category, and any swaps on the list above?
2. Do you have an OpenRouter key with a few dollars on it? Budget is roughly $5 to $15 for the model runs.
3. Where can you realistically find 20+ workers? This is the step most likely to slip, so recruiting should start in week 1.
