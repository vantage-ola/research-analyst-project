# Worker survey

Workers pick their main job and rate only that job's 7 tasks on the same 0/1/2 scale as the rubric. About 5 minutes. No names, phone numbers or emails are collected.

Read [preview.md](preview.md) before building. To change questions, edit `analysis/build_survey.py` (or the tasks in `data/tasks.csv`) and rerun it, so the form and the analysis stay in sync.

## Build the form (one time, about 3 minutes)

1. Go to https://script.google.com and click **New project**.
2. Delete the sample code, paste in everything from `build_form.gs`, and save.
3. Pick `buildForm` in the function menu and click **Run**. Approve the permission prompt (it only creates a form in your Google Drive).
4. Open **Execution log**. It prints the share link and the edit link.
5. In the form's settings, turn off "Collect email addresses" if Google turned it on, then link responses to a Google Sheet (Responses tab, green Sheets icon).

## Target

20 to 25 responses, at least 2 per job, in at least 8 of the 12 jobs. Track counts in the response sheet and push recruiting toward jobs that are short.

## Recruiting message (edit to your voice)

> Hi! I'm doing a small study on which parts of Nigerian remote and freelance jobs AI can really do, from the people who do the work, not from AI companies. If you do customer support, data annotation, writing, VA work, bookkeeping, transcription, translation, design, tutoring, web dev, social media or sales/lead gen, it takes about 5 minutes and it's anonymous: [link]
>
> I'll share the results with everyone who helps. Please forward to anyone who does this work 🙏

Post it in WhatsApp groups, on X and LinkedIn, and in annotation-worker Discords and Telegram groups. Ask 3 or 4 people directly in each job. Direct asks get far more replies than group posts.

## After responses come in

Export the response sheet as CSV to `data/survey_responses_raw.csv` (do not commit any free-text answer that could identify someone). The analysis step maps the answers back to task IDs by job and task text.
