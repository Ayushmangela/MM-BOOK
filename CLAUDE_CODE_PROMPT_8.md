# Prompt for a new Claude Code session

Paste everything below the line into a fresh Claude Code session. Open the session in a folder that contains every file from this package.

---

You are helping our student group run the empirical study for an academic book chapter and write up its results. Our faculty guide is very strict. **Accuracy and traceability matter more than speed.** Every number that ends up in the chapter must be reproducible from raw data by a script in this repo.

## You have real freedom here: use it

Everything below is our **current best plan, not a cage**. Your job is to produce the best possible chapter, one that a strict faculty guide and double-blind IGI reviewers will respect. You are free to add, remove, restructure or replace anything, including: the number of prompts, brands or categories; the platforms; the measures and statistical tests; the framework dimensions; section structure and headings; the figures and tables; the references; and the wording of any part of the draft, including sections already "done". If you find a stronger method, a sharper argument, a better chart, a missing analysis, a weak paragraph, or a flaw in our design, change it. Say what you changed and why in one or two lines, and log it in `logs/deviations.md`.

Push back on us when we are wrong. If a step below is unnecessary, outdated (APIs and platforms change) or worse than an alternative, tell us and propose the better option.

**The only non-negotiables:**
1. No fabricated data, numbers, quotes, citations or sources. Every number is traceable to raw data by code.
2. Honest reporting: limitations, failures and inconvenient results are stated, not hidden.
3. Big or irreversible decisions (spending money, the final brand or prompt set, starting the full data run, changing the research questions or the title) get a quick confirmation from us first. Everything else, just do it and tell us.
4. If you change something the submitted proposal promised (title, RQs, categories, platforms, method), flag it, so we can tell the editors if needed.
5. Style: no em dashes, and nothing that reads as AI-written.

## Step 0: Read the context before doing anything

Read these files fully, in this order:
1. `PROJECT_BRIEF.md`: the whole project, the method, the style rules and the open placeholders
2. `call_for_chapters.txt`: what the book editors want
3. `chapter.md`: the current chapter draft (iteration 1). Read especially the METHOD and FINDINGS sections. Treat it as a starting point. Improve any part of it. Whatever you finally do, the Method text must describe it exactly.
4. `Book_Chapter_Proposal.docx`: read it with pandoc. It was already submitted or is about to be, so the study must stay consistent with it.

Then give me a short summary (10 lines max) of what you understood, and list any inconsistencies you found between the files. Do not write code until I confirm.

## Step 1: Decisions to confirm with me (ask with questions, do not assume)

Ask me about each of these, and offer a recommendation for each:

1. **Access method per platform.** The consumer apps cannot be automated reliably. Check the CURRENT official docs (search the web; do not rely on memory, because APIs change) and recommend one option per platform:
   - ChatGPT: OpenAI API with the web search tool enabled. Check whether user location can be set to India, and which model to use.
   - Gemini: Gemini API with Google Search grounding. It returns grounding sources.
   - Perplexity: Sonar API. It returns citations. Check for location options.
   - Google AI Overviews: there is no official API. Options are a SERP API that returns AI Overviews (for example SerpApi with gl=in, hl=en), or manual collection in a browser. Check what currently works and its cost.

   For each platform, tell me exactly how API output may differ from what a consumer sees. That limitation has to go into the Method and Limitations sections.
2. **Brands.** Propose 5 to 6 brands per category, mixing Indian D2C brands and incumbents. Starting candidates are below. **Verify the current ownership and status of each by web search** and record the source URL and date. Several Indian D2C brands have been acquired by large companies, so we must classify them carefully: for example, "D2C-origin, now owned by X". Some candidates:
   - Skincare D2C: Minimalist, The Derma Co, Dot & Key, Plum, Foxtale, Deconstruct. Incumbents: Lakmé, Pond's, Neutrogena, Cetaphil, L'Oréal Paris, Nivea.
   - Audio D2C: boAt, Noise, Boult. Incumbents: Sony, JBL, Samsung, OnePlus, realme.

   I make the final choice. Also build an **alias list** for each brand, covering spelling variants, "The Derma Co." vs "Derma Co", sub-brand and product-line names, so that mention detection does not miss anything.
3. **API keys and budget.** Estimate the total cost of the full run (all platforms, all runs, plus coding calls) BEFORE running anything. Tell me which keys I need to put in a `.env` file. Never print keys, and never commit `.env`.
4. **Collection window.** This is a fixed window of 2 to 4 consecutive days. Record it.

## Step 2: Build the prompt set (I review it before anything runs)

- About 30 prompts per category, split roughly: 10 generic, 8 use-case, 6 price-band (Rs., realistic Indian price points), 6 comparison (these name two study brands; used only for model image).
- Write them the way Indian shoppers actually ask: natural English, with "in India" where natural. No leading wording, and no brand names in the non-comparison prompts.
- Save as `config/prompts.csv` with columns: prompt_id, category, prompt_type, text, branded (true/false), brands_named.
- Show me the list. After I approve it, **freeze it**: write its SHA-256 hash to `config/FROZEN.txt`. Never change the prompts after the run starts.

## Step 3: Repo structure and collection code

Set up a clean Python project:
```
config/      brands.yaml (brands, type, ownership note, aliases, positioning statement + source URL), prompts.csv, platforms.yaml
data/raw/    one JSONL per platform, APPEND ONLY, never edited or deleted
data/interim/  parsed tables
data/manual/ hand-entered benchmarks and fact sheets (CSV templates)
outputs/tables/  outputs/figures/
src/         collect_*.py, parse.py, code_responses.py, metrics.py, verify.py
logs/        run logs, errors, deviations.md
README.md    how to reproduce every number
```
Requirements for collection:
- Each raw record must contain: run_uuid, prompt_id, platform, repetition (1 to 5), exact request parameters, model name/version returned by the API, UTC and IST timestamps, full response text, full citation/source list with URLs, raw API response JSON, and any error.
- Each repetition is an independent call with no conversation history.
- Randomise the call order with a fixed, logged seed, so that time-of-day effects are spread out.
- Retries: up to 3 with backoff. Log every failure. A call that still fails is recorded as failed, never silently dropped or replaced.
- AI Overview not shown for a query = record as `no_overview` (a non-response), NOT as zero visibility.
- Keep sampling settings at platform defaults, since we are measuring what users get, and record them.
- **Pilot first:** 2 prompts per category x 4 platforms x 1 run. Show me the parsed output, then wait for my go-ahead before the full run.
- Full run: about 60 prompts x 4 platforms x 5 runs, about 1,200 calls. Report the progress and the final counts per platform (success / failed / no_overview).

## Step 4: Coding the responses

Code each response at the brand-mention level. Start from the scheme in `chapter.md` (Method > Coding Scheme), and extend or simplify it if that gives more reliable, more useful data:

1. **Mentions and position (deterministic, no LLM):** match the alias lists with word boundaries and case-insensitive. Position = the order of first occurrence by character offset. Also record non-study brands that are mentioned, using an LLM extraction pass that a human spot-checks. Flag ambiguous matches (for example "Plum" the fruit, or "Noise" the common word) for manual review.
2. **Primary recommendation:** whether the brand is presented as the top or first pick.
3. **Attributes, sentiment, factual claims:** use an LLM coder with a written codebook (`config/codebook.md`), temperature 0, a fixed model version, and a structured JSON output. Save the exact coder prompt and model ID. Sentiment categories: positive / neutral / mixed / negative.
4. **Citations:** extract domains, then classify them with a hand-built lookup table (`config/domain_types.csv`) into brand-owned / marketplace / review or community / editorial or press / encyclopaedic / other. Unknown domains go to a review list for me. Never guess the type.
5. **Positioning alignment:** compare the coded attributes with each brand's positioning statement in `brands.yaml`. That statement comes from the brand's official site, with the URL and retrieval date.
6. **Factual accuracy:** build `data/manual/fact_sheets.csv` (price range, key ingredients or features, from official sites, with URL and date). Check the extracted claims against it. Mark them correct / incorrect / unverifiable. Anything unverifiable stays unverifiable.

## Step 5: Human reliability check (required; the chapter promises it)

- Draw a stratified random 20% subsample (by platform and category, fixed seed) and export it to `outputs/coding_sample.xlsx`, with instructions and drop-down columns.
- Two human authors code it independently. **You must not fill these in.**
- When they return it, compute Cohen's kappa per variable (two humans), plus agreement between the LLM coder and the human consensus. Interpret using Landis & Koch (1977).
- If kappa is below 0.60 for any variable, tell me. Then we refine the codebook and re-code; we do not hide it.
- The chapter must state honestly that an LLM did the first-pass coding, with human validation.

## Step 6: Benchmarks

- Create `data/manual/benchmarks.csv` as a template: brand, platform (Amazon.in / Flipkart / Nykaa), representative product, rating, review count, URL, date checked, checked by. We fill it in by hand on one date. **Do not scrape marketplaces.**
- Only use revenue or market share where a citable public source exists. Store the source.

## Step 7: Metrics

Start from the definitions in the chapter, listed below. Improve, add or drop measures if you can justify it, and update the Method text to match. Compute these for each brand x platform x category, using **non-branded prompts only** for awareness and prominence:
- Mention rate = (responses mentioning the brand) / (valid responses). Valid excludes failed and no_overview; state the denominators.
- Share-of-model = brand mentions / all study-set brand mentions in the category.
- First-mention rate = (responses where the brand is named first among study brands) / (valid responses). Also report it relative to responses mentioning the brand.
- Average position = mean order among study brands, when the brand is mentioned.
- Positioning alignment = matching attributes / coded attributes.
- Accuracy rate = correct / (correct + incorrect). Report unverifiable separately.
- Citation mix = share of each source type among citations attached to answers mentioning the brand. Perplexity, Gemini grounding and AI Overviews show citations; if a platform returns none, say so rather than reporting zeros.
- Stability = mean pairwise Jaccard similarity of the study-brand sets across the 5 runs of each prompt on each platform (10 pairs), averaged by platform and prompt type. Also report the cross-platform spread in mention rate.
- D2C vs incumbent comparison: aggregate by brand type. Where we make a comparative claim, add appropriate tests (for example chi-square or Fisher's exact test for mention rates, with effect sizes) and **bootstrap 95% CIs**, because outputs are non-deterministic. Do not report p-values without effect sizes. Do not over-interpret small differences.
- Model vs benchmark: rank correlation (Spearman) between visibility and the marketplace measures, with n stated, and caveated because n is small.

Outputs:
- `outputs/tables/*.csv` and a formatted `outputs/results_tables.xlsx`, including filled versions of Table 1 (awareness and prominence) and Table 2 (citation mix) from the draft, plus any additional tables.
- Results charts: see Step 8b for the full list and the rules.

## Step 8b: Figures, charts and diagrams (wherever they help the reader)

Before making any figure, check IGI Global's current figure requirements on their author guidelines page (https://www.igi-global.com/publish/contributor-resources/before-you-write/): resolution, file format, whether figures must also be submitted as separate files, colour vs grayscale, and caption and numbering style. Follow those requirements. If they conflict with anything below, IGI wins. Tell me what you found.

**Diagrams.** These can be made now, before the data exists. Show me each one before inserting it.
1. **Figure: Generative Brand Equity framework.** The four dimensions (model awareness, prominence, image, credibility), mapped from Keller's CBBE components, with stability drawn as a cross-cutting layer. Show the link to consumer outcomes as a dashed "proposed, not tested" arrow.
2. **Figure: Research design / audit pipeline.** Prompt set → 4 platforms x 5 runs → raw responses → coding (deterministic + LLM + human validation) → metrics → benchmarks comparison. Put the real counts on the arrows once the data exists.
3. Optional: **Shift from ranked links to synthesised answers** (the old search flow vs the generative flow), for the Introduction, only if it adds something the text does not already say.

**Results charts.** Make these after verification. Every value must come from `outputs/tables`, generated by a script in `src/figures.py`. No hand-typed numbers.
4. Mention rate by brand x platform (grouped bar or heatmap), with D2C and incumbent brands visually distinguished.
5. Share-of-model by brand, per category.
6. Citation mix by source type, D2C vs incumbent and by platform (100% stacked bar).
7. Stability (mean Jaccard) by platform and prompt type, with CIs.
8. Model visibility vs marketplace benchmark (scatter with brand labels, Spearman rho and n in the caption).
9. Positioning alignment / accuracy rate by brand, only if the data is meaningful enough to chart.

Only include a chart if it shows something a table cannot show more clearly. Do not chart the same numbers twice. About 5 to 7 figures is a guide, not a rule. Add or cut figures as the findings demand. The list above is a starting point, not a checklist.

**Rules for all figures:**
- They must be readable in grayscale (use patterns or markers, not only colour) and at print width. Use axis labels with units, n in the caption, and no chart junk or 3D.
- Use the same fonts and style across all figures. Brand names must be spelt exactly as in `brands.yaml`.
- Save each figure as a 300 dpi PNG in `outputs/figures/`, plus whatever separate format IGI requires. Store the diagram source (for example Graphviz, Mermaid or matplotlib code) in the repo, so figures can be regenerated.
- Number figures and tables in order of appearance (Figure 1, Figure 2...). Give each one a full caption that says what it shows, the data source and the n. Each must be referenced in the text BEFORE it appears ("as shown in Figure 3").
- Extend `build.js` to support a line like `@FIG path/to/file.png | Figure 3. Caption text` that inserts the image (docx `ImageRun`, with `type` set, scaled to page width) with its caption below. Add filled-in tables the same way (`@TABLE` from a CSV), so that the tables in the .docx are generated from `outputs/tables` rather than typed by hand.
- After rebuilding, convert the .docx to PDF and look at every page that has a figure or table. Check sizing, that nothing is cut off, that captions sit next to their figures, and that the numbering is correct.
- Add the figures and tables to the traceability check in Step 9: every chart value must match `outputs/tables`.

**Every figure must be backed by data or code (non-negotiable):**
- **No AI image generators**, ever. No DALL-E or similar, and no "illustrations". Every chart and diagram is produced by code that lives in the repo.
- Results charts are built only by `src/figures.py`, which reads `outputs/tables/*.csv`. For each figure, also save the exact plotted values as `outputs/figures/figN_data.csv`, so that anyone can check the chart against the numbers.
- Diagrams are written as code: Graphviz `.dot` or matplotlib, saved in `figures_src/`. Labels and counts on the pipeline diagram are read from the output tables, not typed in.
- Keep `outputs/figures/MANIFEST.csv` with these columns: figure number, caption, file, generating script, data file, source table(s), and the git commit it was generated at.
- One command regenerates every figure from scratch: `python src/figures.py --all`. `verify.py` must assert that each `figN_data.csv` matches the source tables.
- Make a `Figure_Data_Appendix.xlsx`, with one sheet per figure holding its plotted data. Our prof can ask for it.

**Charts must look like journal figures, not AI or dashboard output:**
- Use a plain academic style, like figures in the *Journal of Marketing* or the *Journal of Advertising*. Write a single matplotlib style file (`figures_src/chapter.mplstyle`) and use it for every chart.
- White background, thin black axes, no top or right spines, no gridlines (or very light horizontal ones only), no background shading.
- One font family throughout, matched to the chapter (Times New Roman or a close serif). Sizes must be readable at print width, with no tiny text.
- Grayscale, plus at most one muted accent colour (for example, D2C in dark grey and incumbents in light grey, with hatching). No rainbow or default seaborn or plotly palettes, and no gradients, shadows, rounded bars, 3D, emoji or icons.
- **No title inside the chart image.** The numbered caption in the document carries the title. No subtitles or "insight" text boxes in the image.
- Sort the bars meaningfully (for example by value or by brand type), not alphabetically by default. Label lines and series directly where possible, instead of using big legends.
- Do not print a number on every bar. Exact values belong in the tables. Annotate only what the text discusses.
- Use plain, specific axis labels with units, for example "Mention rate (% of valid responses)", not "Visibility Score".
- Diagrams: simple black-outline rectangles, plain arrows, short labels and white fill. No pastel blobs, icons, cartoon shapes or clip-art.
- Before inserting anything, show me every figure side by side as a contact sheet, so I can reject any that look generic.

## Step 8: Verification (do this before writing any prose)

- Write `src/verify.py`. It recomputes every reported metric from `data/raw` in a separate code path, and asserts that it matches `outputs/tables`.
- Check: total counts add up; no duplicate run_uuids; every prompt x platform x repetition is accounted for; no raw files modified (compare against checksums recorded at collection time).
- Manually spot-check 20 random responses against their coded rows and show me the results.
- Report every anomaly in `logs/deviations.md`: any deviation from the planned method, failures, platform quirks, prompts with no overview, and so on.

## Step 9: Write the results into the chapter

Only after verification passes and I have seen the tables:
1. In `chapter.md`, replace every placeholder in METHOD with what we actually did: access method per platform, models/versions, exact dates, final brand list with ownership notes, final counts, kappa values, and the deviations. Move the full prompt list into an appendix.
2. Write Section 5 FINDINGS, organised by RQ1 to RQ4 plus the benchmarks. Report the numbers exactly as in the output tables, with denominators. Describe, do not over-claim. No causal language. No purchase-intention claims. Use 2 to 4 short verbatim excerpts from real responses, with platform and date, as illustrations.
3. Update the Abstract, the Recommendations, the Limitations (API vs consumer interface, the snapshot window, English only, the sample size, LLM-assisted coding) and the Conclusion, so that they match the actual findings.
4. Fill in the `[add source]` markers only with a verified, citable source. Give me the URL and let me confirm it. Otherwise leave the marker in place.
5. Add any new references in APA 7. Verify each one exists (with a DOI or publisher page) before adding it.
6. Style rules: **no em dashes anywhere**, British spelling as used in the draft, and nothing that reads as AI-written (vary sentence length; avoid "not X but Y", rule-of-three lists, "crucial", "landscape", "delve", "notably"). The target is that the full chapter reaches 10,000 or more words including references, without padding.
7. Insert the diagrams and the results figures and tables from Step 8b in the right places: the framework figure in the Conceptual Framework section, the pipeline figure in Method, and the results charts in Findings. Rebuild with `node build.js`, then check that the .docx renders: convert it to PDF and look at every page.
8. Write a traceability check: every number in the Findings text must appear in `outputs/tables`. Write a script that extracts the numbers from the Findings section and confirms each one, then show me the result.

## Ground rules for the whole session

- **Never fabricate data, numbers, quotes, citations or sources. Never fill gaps with estimates.** If something is missing, say so and leave a visible placeholder.
- Never edit or delete `data/raw`.
- Stop and ask me at every decision point listed above, and whenever something unexpected happens: an API behaving differently from its docs, high failure rates, or results that contradict the draft's framing. Report it plainly. Do not quietly adjust the method.
- Use git and commit after each step, with clear messages. Never commit `.env`.
- Keep a running `logs/session_log.md` of what was done and decided, so that another person or session can continue.
- Be concise in your messages to me.
