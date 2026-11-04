# Sources (checked 2026-11-03)

Full details with checksums are in `sources.csv`. The PDFs aren't in git. Download them from the links below, and check the SHA-256 against `sources.csv` to confirm you have the same file.

## Documents scored

| Country | Document | Date | Where the copy comes from |
|---|---|---|---|
| Nigeria | National Artificial Intelligence Strategy | 19 Sept 2025 | [OECD.AI repository](https://api.oecd.ai/storage//policy-initiatives/Apr2026/117ojp2dncmo9xki2m-Nigeria%20National-Artificial-Intelligence-Strategy-19092025.pdf). The government's NCAIR site only hosts the [August 2024 draft](https://ncair.nitda.gov.ng/wp-content/uploads/2024/08/National-AI-Strategy_01082024-copy.pdf). |
| Kenya | Kenya Artificial Intelligence Strategy 2025-2030 | Mar 2025 | [Data4SDGs copy](https://www.data4sdgs.org/sites/default/files/2025-06/Kenya_AI_Strategy_2025_2030.pdf). The launch is confirmed on the [ministry site](https://ict.go.ke/kenyas-artificial-intelligence-ai-strategy-2025-2030-launched-kicc-nairobi). |
| Rwanda | The National AI Policy | 2023 | [MINICT, official](https://www.minict.gov.rw/fileadmin/user_upload/minict_user_upload/Documents/Artificial_Intelligence_Policy__1_.pdf) |
| Egypt | National AI Strategy, Second Edition (2025-2030) | 2025 | [Ain Shams University copy](https://asu.edu.eg/141090/_mediacenter/2025/pdf/c126e0d5c610f9e67ddb37b06d388bcf.pdf) |
| African Union | Continental Artificial Intelligence Strategy | July 2024 | [AU, official](https://au.int/sites/default/files/documents/44004-doc-EN-_Continental_AI_Strategy_July_2024.pdf) |

Kept for reference, not scored: Nigeria's August 2024 draft, and Kenya's [Implementation Roadmap (Dec 2025)](https://ict.go.ke/sites/default/files/2025-12/Kenya%20National%20AI%20Strategy%202025-2030%20Implementation%20Roadmap.pdf).

## Page numbers and text extraction

- **Every citation uses the PDF page number:** page 1 is the first page of the file, which is what you type into a PDF viewer.
- **Printed page numbers differ in some documents:**
  - Kenya's printed numbers match the PDF pages.
  - The AU's printed numbers are 3 lower (printed page 10 is PDF page 13).
  - Nigeria, Rwanda and Egypt mostly don't print consistent page numbers.
  - The details are in `page_offsets.csv`.
- **Rebuilding the text:** `analysis/extract_text.py` rebuilds the page-by-page text in `sources/text/`, which is kept out of git. The text is normalised, so ligatures like "ﬁ" become "fi".
- **Kenya's full stops:** Kenya's PDF encodes the full stop so it comes out as "�". The script turns it back into "." for that document only. I checked this against the rendered pages.
- **Images and figures:** some content is in images the text extraction can't read, so scorers must look at these pages directly:
  - Nigeria p55 (AI risk matrix)
  - Kenya p84 ("Strategy House" summary)
  - AU p33–34 (focus areas and action areas)
- **Photo pages:** these have no text and are safe to skip: Kenya p13 and p41, and the cover and back pages.

## Why Egypt and not South Africa

South Africa's cabinet approved a draft National AI Policy for public comment in March 2026. The minister withdrew it in April 2026. By July 2026 it was being redrafted as national guidelines for each sector to follow, and there's no current document to score.

## Nigeria's legal position (as of 2026-11-03)

- **The strategy:** final and published (Sept 2025), but non-binding. In early 2026 the minister said it was waiting for National Assembly approval. I found no report that the approval happened.
- **Digital Economy and E-Governance Bill:** it would give NITDA powers over AI and data, with fines up to ₦10 million or 2% of a provider's Nigerian revenue. The most recent report says it passed the House by May 2026 and was waiting on the Senate. There's no confirmed signing.
- **The AI bill:** a Voice of Nigeria report from 23 October 2026 still calls it "proposed".
- **Conclusion:** Nigeria has no AI law in force. Recheck before publishing.

Sources for this section:
- [TechCabal, Aug 2026](https://techcabal.com/2026/08/13/nigerias-identity-law-raises-questions-over-digital-signatures/) (search summary only; the page refused direct access)
- [ThisDay, Jul 2026](https://www.thisdaylive.com/2026/07/09/national-digital-economy-and-e-governance-act-2026-ready-in-weeks/)
- [Bloomberg, Jan 2026](https://www.bloomberg.com/news/articles/2026-01-13/nigeria-set-to-pass-sweeping-ai-rules-for-digital-economy)
- [BusinessDay, on National Assembly approval of the strategy](https://businessday.ng/technology/article/nigeria-awaits-parliamentary-greenlight-for-landmark-national-ai-strategy/)
- [Voice of Nigeria, 23 Oct 2026](https://von.gov.ng/nigerias-ai-bill-targets-sovereignty-investment-power/)
- [Fasken, on South Africa, Mar 2026](https://www.fasken.com/en/knowledge/2026/03/ai-regulation-progress-in-south-africa-a-further-step-in-the-right-direction-2)
- [TechCentral, on South Africa's redraft, Jul 2026](https://techcentral.co.za/radical-rethink-for-south-africas-national-ai-policy/284284/)
