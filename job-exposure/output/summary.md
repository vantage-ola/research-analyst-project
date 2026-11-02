## Task scores: author vs Claude (84 tasks)

- Exact agreement: 49%; within one point: 99%; weighted kappa: 0.20
- Mean score (0-2): author 1.64, Claude 1.38
- Author scored higher on 33 tasks, Claude on 10

## Output ratings: author vs Claude (66 outputs)

- Exact agreement: 64%; within one point: 97%; weighted kappa: 0.20
- Mean rating (1-4): author 3.86, Claude 3.53
- Rating distribution, author: {3: 9, 4: 57}; Claude: {1: 1, 2: 1, 3: 26, 4: 38}
- Kappa is unreliable when one rater uses a narrow range of the scale; read it with the exact-agreement figure.

### By model (unblinded)

| Model | n | Author mean | Claude mean | Author % client-ready | Claude % client-ready |
|---|---|---|---|---|---|
| claude-haiku-5-5 | 22 | 3.82 | 3.18 | 82% | 32% |
| claude-opus-5-5 | 22 | 3.91 | 3.73 | 91% | 73% |
| claude-sonnet-5-5 | 22 | 3.86 | 3.68 | 86% | 68% |

Caveat: Claude rated outputs that include its own model family. The author rated blind; Claude rated blind to model names but could not be blind to its own style. Treat model-vs-model differences as indicative only (22 tasks, one run each).

## Prior scores vs tested quality (22 tested tasks)

- Author scored 'partly or not exposed' (0-1) but outputs averaged 3.5+ out of 4: 3 tasks (CS02, DA03, DA07)
- Author scored 'largely exposed' (2) but outputs averaged under 3.5: 1 tasks (TR06)
- Spearman between author score and mean author rating across the 22 tasks: 0.22

## Ranked table (by author mean exposure)

| # | Category | Author (0-2) | Claude (0-2) | Tested rating (1-4) | GPTs human (0-1) | GPTs n | ILO (0-1) | AEI observed (0-1) |
|---|---|---|---|---|---|---|---|---|
| 1 | Virtual assistance | 2 | 1.43 | 4 | 0.58 | 6 | 0.58 | 0.4528 |
| 2 | Graphic design | 2 | 1.43 | - | 0.5 | 4 | 0.49 | 0.3672 |
| 3 | Entry-level web development | 2 | 1.57 | 4 | 0.64 | 7 | 0.6 | 0.4802 |
| 4 | Content writing | 1.86 | 1.71 | 3.83 | 1.0 | 6 | 0.55 | 0.2462 |
| 5 | Bookkeeping | 1.86 | 1.29 | 4 | 0.43 | 7 | 0.64 | 0.3104 |
| 6 | Transcription | 1.86 | 1.29 | 3.5 | 0.83 | 6 | 0.65 | 0.2385 |
| 7 | Customer support | 1.43 | 1.29 | 4 | 0.9 | 5 | 0.58 | 0.7011 |
| 8 | Translation and localisation | 1.43 | 1 | 3.67 | 1.0 | 7 | 0.59 | 0.4304 |
| 9 | Online tutoring | 1.43 | 1.29 | 4 | 0.43 | 7 | 0.33 | 0.4077 |
| 10 | Social media management | 1.43 | 1.43 | 3.83 | 0.5 | 2 | 0.55 | 0.6483 |
| 11 | Remote sales and lead generation | 1.29 | 1.29 | 3.67 | 0.57 | 7 | 0.61 | 0.2852 |
| 12 | Data annotation and AI training | 1.14 | 1.57 | 4 | 0.5 | 1 | 0.7 | 0.6707 |

### Rank correlation of category scores (Spearman, 12 categories)

- Author vs Claude: 0.30
- Author vs ILO: -0.25
- Author vs AEI observed: -0.25
- Claude vs ILO: -0.10
- Claude vs AEI observed: 0.16
- ILO vs AEI observed: -0.06

GPTs-are-GPTs is left out of the correlation table: it covers 1 to 2 mapped tasks for data annotation and social media management, so category means are not comparable.

