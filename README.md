# Generative Brand Equity: audit pipeline and chapter

Replication package for the IGI Global chapter *Generative Brand Equity: Auditing How AI Answers Represent Indian D2C Brands*. Every number in the chapter is produced by a script in `src/` from the raw responses in `data/raw/`.

## Layout

```
config/          brands.yaml, prompts.csv, platforms.yaml, codebook.md, attribute_codes.csv, domain_types.csv,
                 schedule_*.csv (frozen call order), FROZEN.txt (prompt-set hash)
data/raw/        one JSONL per platform, append-only, never edited
data/interim/    parsed responses, sources, mentions, LLM codes
data/manual/     hand-entered benchmarks, fact sheets, human decisions and reliability workbooks
outputs/tables/  every table and number used in the chapter
outputs/figures/ figures (PNG + TIFF), figN_data.csv, MANIFEST.csv
figures_src/     diagram code and the shared matplotlib style
src/             pipeline code (below)
logs/            collection logs, raw line hashes, deviations.md, session_log.md, verify_report.txt
refs/            reference verification script and Crossref/arXiv metadata
original_package/ the handoff files as received
```

## Reproduce

```bash
python3 -m venv .venv && .venv/bin/pip install requests pyyaml pandas numpy scipy matplotlib openpyxl statsmodels tldextract anthropic pillow
npm install docx@9
cp .env.example .env   # add keys; .env is git-ignored
```

| Step | Command |
|---|---|
| Static design tables | `python src/tables_static.py` |
| Pilot (16 calls) | `python src/collect.py run --batch pilot --pilot` |
| Full run (1,200 calls, resumable) | `python src/collect.py run --batch main` |
| Parse | `python src/parse.py main` |
| Deterministic mentions | `python src/mentions.py main` |
| LLM coding (batch) | `python src/code_responses.py submit --tag main --recode-sample 0.10`, then `collect --batch-id ...`, then `table --tag main` |
| Metrics | `python src/metrics.py --tag main` (use `--provisional` only before human ambiguity decisions exist) |
| Reliability workbooks / kappa | `python src/reliability.py export`, later `python src/reliability.py score` |
| Figures | `python figures_src/diagrams.py framework`, `python figures_src/diagrams.py pipeline`, `python src/figures.py --all` |
| Verification | `python src/verify.py --tag main` |
| Chapter .docx | `node build.js chapter.md Book_Chapter_Generative_Brand_Equity.docx` |

## What humans must do (the code never fills these in)

1. Two authors complete `outputs/coding_sample_coder_A.xlsx` and `_B.xlsx` independently, then a consensus file.
2. Two authors fill `data/manual/benchmarks.csv` by hand on one date.
3. An author confirms or corrects every row of `data/manual/ambiguity_review.csv` (first-pass decisions are marked as such).
4. An author checks `config/domain_types.csv` and `config/brands.yaml` (positioning codes).

See `logs/deviations.md` for every change from the proposal and why.
