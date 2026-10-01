# Deviations log

Every change from the submitted proposal (`Book_Chapter_Proposal_8.docx`), the iteration-1 draft (`chapter_6.md`) or the project brief, with the reason. Items marked **[EDITORS]** change something the proposal promised and should be mentioned to the volume editors.

| # | Change | Reason | Flag |
|---|---|---|---|
| 1 | Platforms are reached through official APIs (OpenAI Responses API + web search; Gemini API + Google Search grounding; Perplexity Agent API; Google AI Overviews via SerpApi), not through consumer apps with "fresh session, no personalisation". Method and Limitations rewritten accordingly. | Consumer apps cannot be queried 1,200 times reliably or within their terms. API outputs can differ from consumer interfaces (Marin et al., 2026); stated in Method and Limitations. | **[EDITORS]** |
| 2 | Perplexity arm uses the Agent API "fast" preset. | Perplexity retired Sonar Chat Completions on 27 Sept 2026 and names "fast" as the Sonar replacement. The preset currently generates with an OpenAI model inside Perplexity's search pipeline; recorded per response. | **[EDITORS]** (minor) |
| 3 | Six brands per category: three Indian D2C-origin, three incumbents (proposal: "five to six"). Brands classified by origin, ownership recorded; Minimalist (HUL-owned since 2025) analysed with and without. | Balanced design; within the promised range. Ownership checked on 2026-10-01 from company and press sources (URLs in `config/brands.yaml`). | none |
| 4 | RQ2 now also covers factual accuracy against official product information. | The project brief asked for accuracy; the proposal mentioned only positioning. Adds a measure, removes nothing. | **[EDITORS]** (minor) |
| 5 | Added a DISCUSSION section; added IGI-required items (abstract 100 to 150 words in third person, AI-use disclosure, competing-interests and funding statements, Key Terms, Additional Reading). | Proposal outline listed a Discussion section; IGI author guidelines require the rest. | none |
| 6 | First-pass coding by an LLM (Claude Opus 5.5, Anthropic), validated by two human coders on a stratified 20% sample, plus a 10% LLM test-retest. | Coder provider is independent of all four audited platforms (self-preference bias, Panickssery et al., 2024). Proposal promised two human coders on a subsample; that is kept. | none |
| 7 | "Temperature 0" for the coder is not possible: current Claude models no longer accept sampling parameters. | Mitigated by fixed model ID, frozen prompt and schema, stored raw outputs and the test-retest check. | none |
| 8 | Inference uses a cluster bootstrap over prompts (B = 2,000) and a GEE logistic check, instead of chi-square / Fisher tests. | The five runs of a prompt are not independent, so tests that assume independent responses would overstate precision. | none |
| 9 | Prominence measured as position among ALL brands named (not only study brands), plus a top-pick rate. | Closer to what a reader sees; position among study brands depends on which other study brands happen to appear. First-mention among study brands kept as in the draft. | none |
| 10 | Source types: added "video" and split "review/comparison" from "community/UGC". | YouTube and dedicated review sites behave differently from forums; merging them would hide the distinction RQ3 asks about. | none |
| 11 | Price claims count as correct within 20% of official MRP. | Online prices vary daily around MRP; an exact-match rule would mark most prices wrong for reasons unrelated to the model. | none |
| 12 | AI Overviews captured with device=desktop. | SerpApi's AI Overview parsing is documented for desktop; most Indian searches are on mobile. Stated as a limitation. | none |
| 13 | Gemini requests carry no location parameter (the grounding tool has none); requests originate from Mumbai. | API limitation. Stated in Method. | none |
| 14 | Title: IGI limits subtitles to 50 characters; "Auditing How AI Answers Represent Indian D2C Brands" has 51. Suggested: "Auditing How AI Answers Portray Indian D2C Brands" (49). NOT changed pending your decision. | IGI author guidelines. | **[DECISION NEEDED]** |
| 15 | Collection window: [to be recorded after the run]. | | |
