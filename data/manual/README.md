# Hand-entered data (never scraped)

- `benchmarks.csv`: one row per brand x marketplace (Amazon.in, Flipkart, and Nykaa for skincare).
  Choose the brand's best-selling product in the study category on that marketplace (the first
  product of that brand under the marketplace's "best sellers" or "popularity" sort for the category).
  Record rating (out of 5), number of ratings or reviews, full product URL, date and initials.
  Two authors fill this on the SAME date. Do not use any scraping tool.
- `fact_sheets.csv`: official product facts used to check model claims. One row per fact.
  fact_type is one of: price_mrp, ingredient, concentration, spec, feature, origin, ownership.
  Source must be the brand's official website (or the company's own announcement for ownership).
- `ambiguity_review.csv`: human decisions on brand-mention cases where the alias matcher and the
  LLM coder disagree. decision = brand | not_brand; decided_by = initials.
- `coding_sample_coder_A.xlsx`, `coding_sample_coder_B.xlsx`: completed reliability workbooks.
- `coding_consensus.xlsx`: consensus codes after the two coders discuss disagreements.
