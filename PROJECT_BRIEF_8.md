# Project Brief: IGI Global Book Chapter (Generative Brand Equity)

Read this first. It explains the whole project so far, so anyone (or any Claude session) can pick it up without the earlier conversation.

## 1. What this is

A group of MBA Tech students at MPSTME, SVKM's NMIMS Mumbai, is writing a book chapter, guided by a faculty member, for an IGI Global call for chapters. The faculty guide is strict about accuracy. Every number in the chapter must be traceable to raw data.

- **Book:** *Digital Marketing and Brand Visibility in the Age of Generative Discovery*
- **Editors:** Lara Bacalhau, Miguel Pereira, Paula Pinheiro (Polytechnic University of Coimbra / University of Aveiro, Portugal)
- **Publisher:** IGI Global Scientific Publishing, expected 2027
- **Full call text:** `call_for_chapters.txt`

### Deadlines
| Date | Milestone |
|---|---|
| Oct 25, 2026 | Proposal (1,000 to 2,000 words) via eEditorial Discovery |
| Nov 8, 2026 | Acceptance notification |
| Jan 17, 2027 | Full chapter, minimum 10,000 words including references |
| Feb 28, 2027 | Review results |
| Mar 28, 2027 | Final acceptance |
| Apr 4, 2027 | Final chapter |

Review is double-anonymized. There are no fees. Scopus indexing is not guaranteed.

## 2. What the book wants

The book treats **brand visibility as a dependent variable** when an AI model sits between the consumer and the market (ChatGPT, Gemini, Perplexity, Google AI Overviews). Chapters should address one or more of the following: how attention and salience work when a model filters first; how to **measure** visibility with defensible instruments; what marketing actions influence it; and the regulatory and distributional consequences.

## 3. Our chapter

**Title:** Generative Brand Equity: Auditing How AI Answers Represent Indian D2C Brands

**Core idea:** Adapt Keller's (1993) consumer-based brand equity to AI answers. We run a structured, repeated prompt audit of Indian D2C brands and incumbents across 4 generative platforms, in 2 categories.

**Framework dimensions:**
- Model awareness: is the brand retrieved?
- Model prominence: where in the answer does it appear?
- Model image: how is it described, and does that match its positioning?
- Model credibility: which source types are cited?
- Stability: a cross-cutting property, meaning consistency across runs and platforms.

**Research questions**
- RQ1: How often and how prominently do D2C brands appear compared with incumbents?
- RQ2: How do models describe them, and how well does that match positioning and facts?
- RQ3: Which sources do models rely on, and do they differ for D2C brands and incumbents?
- RQ4: How stable are the measures across runs and platforms?

**Important framing:** we measure model outputs, NOT consumer purchase intention. Never claim purchase intention effects.

## 4. Current state (iteration 1, done)

- `Book_Chapter_Proposal.docx`: final proposal, about 1,500 words.
- `Book_Chapter_Draft.docx`: full chapter draft, about 5,500 words. All sections are written except **Findings**, which has placeholders and two empty template tables. Bracketed placeholders `[ ... ]` mark everything still missing.
- `chapter.md` + `build.js`: the source of the draft. Edit `chapter.md`, then run `node build.js` (needs the `docx` npm package) to regenerate the .docx. Syntax: `# H1`, `## H2`, `- bullet`, `**bold**`, `@REF` reference, `@TABLE1/@TABLE2` table templates, `@NOTE` yellow note, `@TITLE`, `@CENTER`.

### Placeholders still open
- Final brand list and selection rationale (Method > Categories and Brands)
- Final prompt list as an appendix (Method > Prompt Design)
- Data collection dates (Method > Platforms and Data Collection)
- All of Section 5, Findings (needs the data)
- `[add source]` markers: an Indian D2C market size and growth figure from a citable report
- One or two sentences of key findings in the Conclusion
- The Recommendations section to be revised in light of the results
- Author names and corresponding email

## 5. Planned method (as written in the draft)

- 2 categories: skincare (face serums, moisturisers) and consumer audio (wireless earbuds)
- 5 to 6 brands per category, mixing Indian D2C brands and incumbents
- About 30 prompts per category, of four types: generic, use-case, price-band (in Rs.), and comparison (names brands; used for model image only)
- 4 platforms x 5 repeated runs per prompt, about 1,200 responses
- Coding: mention, position, attributes, sentiment, factual accuracy, cited domains (brand-owned / marketplace / review or community / editorial or press / encyclopaedic)
- Measures: mention rate, share-of-model, first-mention rate, average position, positioning alignment, accuracy rate, citation mix, stability (mean pairwise Jaccard across the 5 runs)
- Benchmarks: Amazon India / Flipkart / Nykaa ratings and review counts; reported revenue or share where public
- Reliability: two human authors double-code a 20% random subsample, with Cohen's kappa
- Ethics: no human subjects, no scraping beyond platform terms

**Known issue to resolve:** the draft says "fresh session, no personalisation, location India". If the data is collected through APIs rather than the consumer apps, the Method section MUST be rewritten to say so. API outputs can differ from what consumers see.

## 6. Style rules for all chapter text

- No em dashes anywhere.
- Plain academic British-leaning spelling, as already used (optimisation, synthesised).
- It must not read as AI-written: vary sentence length, avoid "not X but Y" and rule-of-three patterns, and avoid filler like "plays a crucial role", "in today's landscape", "delve".
- Never invent numbers, citations or quotes. A missing value stays as a visible `[placeholder]`.
- References in APA 7, and only ones that are verified to exist.

## 7. Group preferences

Concise, direct, honest feedback. Point out problems instead of glossing over them. Work step by step and check in at decision points.

## 8. Freedom to improve

Everything in this brief and in the draft is the current best plan, not a fixed spec. Any session working on this may add, remove or restructure anything (method, measures, sections, figures, wording) if that makes the chapter stronger. The conditions: log the change and the reason; never fabricate anything; and flag any change to what the proposal promised to the editors.
