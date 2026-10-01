# Coding Manual: Generative Brand Equity Audit

Version 1.0 (frozen before coding). This manual is used, word for word, by the LLM first-pass coder and by the two human coders. Any change after coding starts creates a new version and triggers re-coding.

## 1. Units

- **Response**: one answer returned by one platform for one prompt on one repetition.
- **Brand-in-response**: one study brand that is referred to in one response. Most variables are coded at this level.

Code only what the response text says. Do not use outside knowledge about a brand when coding attributes or sentiment. Product names count as references to their brand (for example, "Airdopes 141" refers to boAt; "Hydro Boost" refers to Neutrogena; "Galaxy Buds" refers to Samsung).

## 2. Response-level variables

**R1. all_brands** (ordered list). Every brand the response names, in order of first appearance, written in its usual brand name (for example "The Derma Co", not "Derma Co."). Include brands named in passing. Exclude retailers and marketplaces (Amazon, Flipkart, Nykaa, Myntra, Tira) unless they are named as the maker of a product (for example, Nykaa's own label "Kay Beauty" is a brand; "available on Nykaa" is not).

**R2. answer_form** (one of):
- `list`: recommends two or more brands or products as options
- `single`: recommends one brand or product
- `comparison`: weighs two or more named options against each other without a single generic list
- `no_recommendation`: declines, asks a clarifying question, or gives only general advice with no brand

**R3. top_pick**: the brand presented as the best, first-choice or "overall" pick, if the response clearly signals one (words such as "best overall", "top pick", "my recommendation", "go for X", or a ranked list headed "1."). If the response is an unranked list with no signal of preference, code `none`. Placement first in an unranked list is NOT enough; position is captured separately by code.

## 3. Brand-in-response variables

Code these for each study brand listed in the coding sheet for that response.

**B1. is_brand_reference** (yes/no). Yes if the word refers to the brand. No if it is a common word or ingredient (for example "noise cancellation", "Kakadu plum extract", "a minimalist routine").

**B2. stance** (one of):
- `recommended`: offered as a suitable choice
- `mentioned_neutral`: named without being recommended or rejected (for example in a list of brands that exist)
- `discouraged`: advised against, or named as an inferior alternative

**B3. attributes** (zero or more codes from `config/attribute_codes.csv` for the response's category). Assign a code only if the response attaches that quality to THIS brand or one of its products. Generic advice ("look for niacinamide") is not an attribute of any brand. Use at most the codes that are clearly supported; do not infer.

**B4. sentiment** toward the brand in this response (one of):
- `positive`: only favourable description
- `negative`: only unfavourable description
- `mixed`: both favourable and unfavourable points (for example "great bass but weak mic")
- `neutral`: named or described without evaluation

**B5. factual_claims** (list). Each checkable statement of fact about the brand or one of its products, copied verbatim as a short span, with a claim type:
- `price`: a price, price range or price band (for example "around Rs. 599")
- `composition_or_spec`: an ingredient, concentration, or technical specification (for example "10% niacinamide", "50 hours battery", "IP55")
- `origin_or_ownership`: country of origin, parent company, founding (for example "Indian brand", "owned by HUL")
- `other_fact`: any other checkable fact (for example "fragrance-free", "has ANC")
Evaluations ("good value", "great sound") are not factual claims.

**B6. products** (list): product names given for the brand, as written.

## 4. Decision rules

1. If a brand appears only inside a citation title or URL and not in the answer text, it is not coded as mentioned.
2. Comparison prompts name two brands. Code them like any other response; their awareness and prominence values are excluded from the visibility measures at analysis stage, not at coding stage.
3. If the response is cut off or garbled, code what is present and flag `truncated = yes`.
4. When unsure between two sentiment values, choose `mixed` only if both a favourable and an unfavourable point are explicit; otherwise choose the value supported by the text.
5. Do not correct the response. A wrong price is still coded as a price claim.

## 5. Factual accuracy (coded later against fact sheets)

Each claim from B5 is checked against `data/manual/fact_sheets.csv`, which records official information with a source URL and retrieval date:
- `correct`: matches the fact sheet. Prices count as correct if within 20% of the official MRP of the named product, or within the brand's official price range when no product is named.
- `incorrect`: contradicts the fact sheet.
- `unverifiable`: the fact sheet has no entry that can confirm or contradict it.
