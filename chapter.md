@TITLE Generative Brand Equity: Auditing How AI Answers Represent Indian D2C Brands
@CENTER [Author 1], [Author 2], [Author 3], [Faculty guide]
@CENTER Mukesh Patel School of Technology Management and Engineering, SVKM's NMIMS, Mumbai, India

# ABSTRACT

[ABSTRACT: written after the audit; 100 to 150 words, third person.]

**Keywords:** Generative Engine Optimisation, Brand Visibility, Consumer-Based Brand Equity, Share-of-Model, AI Search, Algorithm Audit, D2C Brands, India, Emerging Markets

# INTRODUCTION

For roughly two decades, online brand discovery ran on a list. A shopper typed a query, a search engine returned ranked links, and brands competed for position through search engine optimisation, paid search and marketplace advertising. The arrangement was imperfect, but it was legible. A brand could see where it ranked, buy its way onto the page and follow the consequences through clicks and conversions. Even a shopper who never clicked had at least seen the brand name on the results page.

Generative AI systems change that arrangement. Ask ChatGPT, Gemini or Perplexity for a vitamin C serum for oily skin under Rs. 1,000 and the reply is a few paragraphs naming perhaps three to six products, each with a line or two of justification and, on some platforms, a handful of source links. Google's AI Overviews place a similar synthesised paragraph above the familiar results. These answers appear to absorb attention that once went to the links below them. In a panel of United States users observed in March 2025, Google searches that displayed an AI summary led to a click on a traditional result in 8% of visits, against 15% when no summary appeared. Links inside the summary itself were clicked in 1% of visits (Chapekis & Lieb, 2025). The first reader of brand content is increasingly a retrieval-and-synthesis pipeline, and the shopper meets the brand, if at all, through that pipeline's summary.

India is a consequential place to study this shift. OpenAI's chief executive has described India as the company's second-largest market after the United States, and from November 2025 the company offered its ChatGPT Go plan free for a year to users in India (Singh, 2025). Bharti Airtel offered a year of Perplexity Pro to its 360 million customers in July 2025 (Kohli, 2025), and Google's AI Overviews have appeared in Indian search results, in English and Hindi, since August 2024 (News On AIR, 2024). The platform providers are, in effect, competing to become the default first stop for a very large population of new and price-conscious online shoppers.

The shift unsettles assumptions that sit deep in marketing theory. Consumer-based brand equity rests on brand knowledge that consumers build through exposure the firm can shape, much of it through the firm's own communication (Keller, 1993). The mental availability perspective holds that brands grow by coming to mind easily in buying situations (Romaniuk & Sharp, 2016; Sharp, 2010), and consideration set research shows that what is recalled at the point of decision constrains what is chosen (Nedungadi, 1990; Shocker et al., 1991). Under generative mediation the order changes. A model's retrieval precedes the shopper's recall, and the model's few sentences about a brand may be the first, and sometimes the only, account of it that the shopper reads before deciding.

The stakes are uneven. India's direct-to-consumer (D2C) sector is estimated to have grown from under US$5 billion in 2020 to between US$12 and 15 billion in 2025, and to include more than 800 active brands (Srivastava, 2026). Many of these brands, in personal care and consumer electronics especially, reached national scale through social media, influencers and marketplace listings rather than mass media. They compete with domestic and multinational incumbents that have decades of press coverage, reference entries and retail history behind them. Language models answer more reliably about entities that are well documented in their training data (Kandpal et al., 2023; Mallen et al., 2023), and early audits report a tilt towards large and global brands (Chen et al., 2025; Kamruzzaman et al., 2024). If generative systems lean on that kind of documentation, they may reproduce or widen the incumbents' advantage. If they lean instead on recent reviews, community discussion and marketplace content, the same systems could favour brands that were born online. Which of these is happening in India has not been examined.

Research on the question has moved quickly but in separate streams. Computer scientists have formalised generative engine optimisation (GEO) and tested how changes to content affect citation (Aggarwal et al., 2024; Puerto et al., 2025). A wave of audit studies posted in 2026 has begun to measure which brands language models recommend (Jack et al., 2026; Malthouse et al., 2026; Marin et al., 2026). Marketing scholarship has mostly treated generative AI as a production tool, a strategic capability, a research method or an ethical problem (Grewal et al., 2025; Hartmann et al., 2025; Hermann & Puntoni, 2025; Yoo et al., 2025). What is missing is a marketing construct that treats the model's representation of a brand as an outcome in its own right, connects it to established brand equity theory and measures it with an instrument that respects the non-deterministic behaviour of the systems involved. Evidence from emerging markets, and on challenger brands specifically, is close to absent.

This chapter addresses that gap. Its objectives are to:

- conceptualise **Generative Brand Equity** as an adaptation of consumer-based brand equity for settings in which a model performs the first filtering of brands;
- design a **replicable prompt-based audit protocol** that measures run-to-run and cross-platform variation instead of averaging it away;
- apply the protocol to **six Indian D2C-origin brands and six incumbents** in skincare and wireless earbuds across ChatGPT, Gemini, Perplexity and Google AI Overviews; and
- derive **implications for managers, researchers and policymakers**, with particular attention to resource-constrained brands.

The Background section reviews work on brand equity, salience and consideration, answer engines, what language models know about brands, GEO and recent audits, and then sets out the Indian D2C context and four research questions. The next section develops the Generative Brand Equity framework and its propositions. The Method section describes the audit, and the Findings section reports results by research question. The chapter then discusses what the results mean for theory, offers recommendations for brands and for governance, and closes with future research directions, limitations and conclusions.

# BACKGROUND

## Brand Equity and the Exposure Assumption

Keller (1993) defined customer-based brand equity as the differential effect of brand knowledge on consumer response to the marketing of a brand. Brand knowledge has two parts: brand awareness, made up of recognition and recall, and brand image, the set of associations held in memory and characterised by their strength, favourability and uniqueness. Aaker (1991) described a similar set of assets and added perceived quality and loyalty. Later work extended the idea in a direction that matters here. Erdem and Swait (1998, 2004) showed that a brand works partly as a credible signal under uncertainty, so that consumers' belief in what the brand claims shapes both consideration and choice. Keller (2016), looking back on two decades of research, observed that digital channels had multiplied the touchpoints through which brand knowledge forms while leaving the underlying mechanism in place.

That mechanism is exposure. Advertising, packaging, retail presence, word of mouth and use experience put the brand, or content about it, in front of the consumer, and the firm can influence most of those encounters. Hierarchy-of-effects models make the same assumption: consumers move from awareness through knowledge and liking towards purchase as communications reach them (Lavidge & Steiner, 1961). Digital marketing widened the set of encounters without changing their nature (Kannan & Li, 2017). Search advertising placed brands in front of consumers at the moment of intent, and online reviews became a strong form of mediated word of mouth (Chevalier & Mayzlin, 2006; Dellarocas, 2003). In each case the consumer still met the brand, or a particular person's account of it, directly.

Generative answers weaken this assumption in a specific way. They resemble word of mouth, in that someone other than the firm supplies the description, yet they differ from it twice over. The account is a single synthesis rather than many independent voices, so disagreement among reviewers is often compressed into one confident sentence. And the sources behind it are partly hidden: a shopper can read a review and judge its author, whereas a model's description blends sources that may or may not be displayed. The firm neither writes the description nor, in most cases, knows what it says.

## Salience, Consideration and Delegated Choice

Romaniuk and Sharp (2004) defined brand salience as the propensity of a brand to be noticed or to come to mind in buying situations, and argued that it depends on the number and quality of links between the brand and the cues buyers use. Later work organised those cues as category entry points, the needs, occasions and constraints from which a purchase starts (Romaniuk & Sharp, 2016; Sharp, 2010). Consideration set research adds that recall can change choice without any change in how brands are evaluated (Nedungadi, 1990) and that choice is usually made from a small set of brands that pass an initial screen (Shocker et al., 1991).

Asking an AI system for a recommendation hands that initial screen to the system. Research on online decision aids anticipated some of the consequences. Häubl and Trifts (2000) found that a recommendation agent reduced the size of shoppers' consideration sets while raising their quality, and Xiao and Benbasat's (2007) review showed that recommendation agents shape both the decision process and its outcome. Dellaert et al. (2020) argued that AI voice assistants go further, because consumers delegate the search itself and see only the few options the assistant chooses to present. Puntoni et al. (2021) described the same move from the consumer's side as an experience of delegation. A generative answer is, in this sense, a proposed consideration set. A brand absent from it may never reach the shopper's evoked set, however salient the brand is among people who shop in other ways. Prompts that specify a use case or a price ceiling are close equivalents of category entry points, which suggests that a brand's generative visibility should be measured across several of them rather than for one generic query.

## From Search Engines to Answer Engines

Search engines have long been understood as gatekeepers whose ranking choices carry commercial and political consequences (Introna & Nissenbaum, 2000). Position on a results page matters. Users trust higher-ranked results even when relevance is held constant (Pan et al., 2007), rankings causally affect which products consumers examine (Ursu, 2018), and the design of a results page can steer traffic towards a platform's own services (Edelman & Lai, 2016). The marketing response was search engine optimisation and paid search, both built on a visible, ordered list.

Answer engines combine retrieval with synthesis. In retrieval-augmented generation, a model retrieves documents relevant to a query and conditions its answer on them (Lewis et al., 2020). Perplexity, Google's AI Overviews and the search-enabled modes of ChatGPT and Gemini all work broadly this way, although each decides differently when to search, how many sources to read and which to display. The citations they show are not always faithful to the answer. In a human evaluation of four generative search engines, Liu et al. (2023) found that only 51.5% of generated sentences were fully supported by their citations and that 74.5% of citations supported the sentence to which they were attached. Sharma et al. (2024) found that conversational search led users towards more confirmatory information seeking than conventional search.

Two further properties complicate measurement. Outputs are probabilistic: the same prompt can produce different brands and different descriptions on different occasions, and non-determinism persists even under settings intended to remove it (Atıl et al., 2025; Ouyang et al., 2025). Models can also produce fluent statements that are false, the problem studied as hallucination (Ji et al., 2023). A brand can therefore be visible and misdescribed at the same time, with the wrong price band, ingredient or specification attached to it. Neither property fits the idea of generative visibility as a single stable number.

## What Language Models Know About Brands

A model's answer about a product category draws on parametric knowledge absorbed during training and on non-parametric knowledge retrieved at query time. The first kind is uneven. Kandpal et al. (2023) showed that a model's ability to answer a factual question rises with the number of training documents relevant to that question, so that rarely documented facts are learned poorly. Mallen et al. (2023) found the same pattern for entities, with accuracy falling for less popular ones, and showed that retrieval helped most where parametric knowledge was weakest. For brands the implication is direct. A brand with a long trail of press coverage, reference entries and reviews is better represented in what a model knows unaided than a brand a few years old, unless retrieval brings the newer brand into view.

Studies of brand bias point the same way. Kamruzzaman et al. (2024) found that language models associated global brands with positive attributes more readily than local ones, although they also detected country-of-origin effects that could favour local brands in particular contexts. Rienecker et al. (2026) reported that models developed in the United States showed marked preference for American entities across commercial and cultural topics, and Chen et al. (2025) described a "big brand bias" in AI search that niche brands would need to overcome. Research on recommender systems offers two competing expectations. Algorithmic recommendation can concentrate demand on already popular items (Fleder & Hosanagar, 2009), but lower search costs can also spread demand towards niche products (Brynjolfsson et al., 2011). Which tendency dominates in generative answers is an empirical matter, and the answer may differ by category, platform and market.

## Generative Engine Optimisation and Its Limits

Aggarwal et al. (2024) introduced generative engine optimisation as a framework for raising the visibility of content inside generative answers. On a benchmark of diverse queries, they reported that adding citations, quotations and statistics to source pages could raise visibility by up to 40%, while keyword stuffing had little effect, and that the gains varied across domains. Later work has qualified that picture. Puerto et al. (2025) found that most conversational search optimisation methods were largely ineffective, and sometimes harmful, in a benchmark covering question answering and product recommendation; traditional ranking-oriented optimisation worked better, and gains shrank as more competitors adopted the same methods. A 2026 review of 45 GEO studies concluded that the foundational gains hold for content already retrieved into a model's context, and that no reviewed technique had shown a stable, cross-platform effect on organic discoverability (Martinez, 2026).

Other studies show that the selection can be pushed in directions that matter for competition. Kumar and Lakkaraju (2024) showed that a crafted text sequence inserted into a product page raised the chance that a model listed the product as its top recommendation, and Nestaas et al. (2025) demonstrated preference manipulation attacks that steer model-mediated search towards an attacker's content. In skincare, Chu and Hou (2026) found that well-known brands were recommended every time when products were otherwise identical, that a small rating advantage for a competitor was enough to break that dominance, and that authority-style claims, including fabricated clinical evidence, could shift recommendations. Chen et al. (2025) found that AI search leaned heavily on earned, third-party media rather than brand-owned or social content. For marketers, this work raises a question that the GEO literature has not settled: which kinds of sources do platforms actually rely on when they recommend brands, and do those dependencies favour some kinds of brands over others?

## Auditing Brand Recommendations

Algorithm audits study platform behaviour by querying a system systematically and analysing its outputs without access to its internals (Metaxa et al., 2021; Sandvig et al., 2014). The approach has recently been turned on brand recommendations. Malthouse et al. (2026) proposed estimating the probability and rank of brand recommendations by repeated sampling and applied the method to six models in five categories. They found that well-known brands were often omitted and that prominence tracked search interest and online conversation more closely than conventional measures of brand popularity. Jack et al. (2026) audited about 37,000 runs across 19 sectors and reported that roughly half of specialist and regional brands never surfaced at all. A census-based audit of cafes, restaurants and bars in two Indonesian markets found that 85.6% of venues were never recommended (Pitenin, 2026). Documentation such as review volume and an own website predicted entry into answers, while ratings mattered for rank only once a venue had been included.

Three findings from this work shaped the design of the present study. The first is that answers vary from run to run. Żatuchin (2026b) found that the top recommendation changed across six identical runs for four of six prompts, at the same rate in the ChatGPT web interface and in its API. The second is that what a researcher observes depends on how the system is accessed. Marin et al. (2026) compared consumer interfaces with application programming interfaces (APIs) and found that the domains displayed for the same query overlapped by only 12.0% for ChatGPT and 14.8% for Gemini. The third is that language and location select the market: in Żatuchin's (2026b) probe, the language of the query decided whether local suppliers appeared at all, while the network location shifted which country's brands were named. Analyses of citations add that third-party sites supply most of the evidence behind brand answers, with Wikipedia the most-cited domain in 11 of 12 languages studied (Żatuchin, 2026a). Finally, an observational study that linked chatbot conversations to clickstream data found that a recommendation from an assistant raised a brand's same-name searches by 4.3 percentage points among users with no recent engagement with the brand (Iannelli & Ai, 2026). It is early evidence that model recommendations change behaviour outside the chat.

Most of this work is recent and much of it is not yet peer reviewed. It is set largely in North American and European markets, framed in the vocabulary of information retrieval rather than brand theory, and rarely distinguishes challenger brands from incumbents. None of it, to our knowledge, examines Indian brands.

## Generative AI in Marketing Scholarship

Marketing research on generative AI has grown quickly, but most of it concerns how firms and researchers use the technology. Hartmann et al. (2025) showed that AI-generated visual marketing content can match or exceed human-made content under specified conditions. Grewal et al. (2025) examined how generative AI is reshaping marketing strategy and implementation, Yoo et al. (2025) charted its uses in consumer research, and Hermann and Puntoni (2025) set out principles for its ethical design and deployment. In each case the model is an instrument in marketers' hands. Far less work treats the model as an intermediary whose outputs decide which brands consumers hear about and how those brands are described.

## The Indian D2C Context

India suits this question for three reasons. Its D2C sector includes brands that reached national scale within a few years, especially in personal care and consumer audio, and that now compete head-on with domestic and multinational incumbents (Srivastava, 2026). The sector is also consolidating, which blurs the line between challenger and incumbent. Hindustan Unilever, owner of Lakmé, completed the purchase of a 90.5% stake in the skincare brand Minimalist in April 2025 (Martins, 2025), and The Derma Co belongs to the listed Honasa Consumer. Second, Indian purchase journeys run heavily through marketplaces such as Amazon, Flipkart and, in beauty, Nykaa, which generate large volumes of ratings and reviews that may feed generative answers. Third, research on GEO and AI search has concentrated on English-language queries in North American and European markets. The finding that models developed in the United States favour American entities (Rienecker et al., 2026) gives reason to suspect that Indian brands, and young Indian brands in particular, may start at a disadvantage.

## Research Gap and Questions

Taken together, the literature lacks a marketing construct for brand equity that forms through a model's representation rather than through direct exposure, and it has no agreed instrument for measuring such equity. Evidence on how generative systems treat challenger brands in emerging markets is close to absent. The chapter addresses four research questions:

- **RQ1.** How frequently and how prominently do Indian D2C-origin brands appear in generative answers relative to incumbents?
- **RQ2.** How do the platforms describe these brands, and how closely do the descriptions match the brands' stated positioning and verifiable product facts?
- **RQ3.** Which kinds of sources do the platforms display when they recommend brands, and do source patterns differ between D2C-origin brands and incumbents?
- **RQ4.** How stable are these measures across repeated runs of the same prompt and across platforms?

# GENERATIVE BRAND EQUITY: A CONCEPTUAL FRAMEWORK

## Definition

We define **Generative Brand Equity** as the differential visibility and representation of a brand in the outputs of generative AI systems, relative to competing brands in its category, in response to category-relevant shopper queries. The definition deliberately parallels Keller's (1993) but moves the site of brand knowledge. It asks what models surface and say about a brand when shoppers ask, rather than what consumers know about it.

Three features follow from this choice. Generative Brand Equity is a property of a distribution of outputs, because any single answer is one draw from a system that would answer differently if asked again. It is relative to a platform, since the same brand can be prominent on one system and missing from another. And it is relative to the query, because a brand may be retrieved for one category entry point and not for the next. Measuring it therefore calls for repeated sampling across platforms and query types, which is the design adopted in this chapter.

## Dimensions

The framework has four dimensions, each adapted from an established component of brand equity, and treats stability as a property of every one of them. Figure 1 sets out the mapping.

@FIG outputs/figures/fig1_framework.png | **Figure 1.** The Generative Brand Equity framework. Each dimension adapts a component of consumer-based brand equity; stability across repeated runs and platforms applies to all four. Dashed elements mark the proposed link to consumer response, which this chapter does not test.

**Model awareness** corresponds to brand awareness. It captures whether, and how often, a brand is retrieved in answer to category-level prompts that do not name it, and is the generative analogue of unaided recall.

**Model prominence** captures where the brand appears within an answer. Being named first, or being presented as the single best choice, plausibly matters more than appearing fifth in a list, given what is known about position effects in search (Pan et al., 2007; Ursu, 2018). Prominence has no exact counterpart in Keller's framework, but it parallels top-of-mind awareness and the salience of a brand relative to its competitors (Romaniuk & Sharp, 2004).

**Model image** corresponds to brand image. It covers the attributes, benefits, price cues and tone that a model attaches to a brand. Model image can be compared with the brand's own positioning to assess alignment, and its factual claims can be checked against official product information. A brand may be visible yet described in ways that conflict with its positioning, or described wrongly.

**Model credibility** captures the kinds of sources a platform displays in support of what it says about a brand. It draws on the idea that a brand's claims persuade in proportion to their credibility (Erdem & Swait, 2004) and on the older finding that the perceived credibility of a source shapes the effect of a message (Hovland & Weiss, 1951). The framework distinguishes brand-owned sites, marketplace listings, review and community content, editorial and business press, encyclopaedic sources and video. A brand described on the strength of independent sources stands on different ground from one described mainly from its own website.

**Stability** is treated as a property of all four dimensions. Because outputs vary across runs and platforms, each dimension has a level, how high it is on average, and a stability, how consistently that level is reproduced. Two brands with the same average share of answers may differ sharply in how reliably they appear. No claim about a brand's generative visibility is defensible without some statement of its stability.

## Propositions

The framework yields four propositions that guide the audit and that future work can test more directly.

- **P1.** Model awareness and prominence will differ systematically between D2C-origin brands and incumbents, and the differences will not simply mirror the brands' marketplace standing.
- **P2.** Model image will diverge from a brand's positioning more often for brands with thinner third-party coverage.
- **P3.** Brands supported by a wider range of third-party source types will show more stable visibility across platforms.
- **P4.** Visibility will vary across platforms and repeated runs enough that single-run or single-platform audits misstate a brand's generative visibility.

## Scope and Boundary Conditions

Generative Brand Equity is a property of model outputs, not of consumer memory, and the audit reported here measures outputs only. It does not measure attitudes, consideration or purchase intention. The proposed link to consumer response rests on two arguments. The first is structural: a generative answer works as a proposed consideration set, and decision aids that narrow consideration sets are known to shape choice (Häubl & Trifts, 2000; Xiao & Benbasat, 2007). The second is emerging evidence that being recommended by an assistant changes what people search for afterwards (Iannelli & Ai, 2026). Both make the link plausible; neither establishes its size in Indian categories, which is why it appears as a dashed line in Figure 1.

The construct also differs from share of voice. Share of voice measures what a firm pays to say relative to its competitors. Share of model, as used here, measures what a model chooses to say. A firm can buy the first but can influence the second only indirectly, through the sources that models read and display, which is why model credibility belongs in the framework rather than outside it.

# METHOD

## Research Design

The study is a structured prompt-based audit, adapted from algorithm audit research that examines platform behaviour by querying a system systematically and analysing its outputs (Metaxa et al., 2021; Sandvig et al., 2014). The design is observational and descriptive-comparative. It follows the recommendation emerging from recent audits to treat brand recommendation as a stochastic process, estimated by repeated sampling rather than inferred from single answers (Malthouse et al., 2026; Martinez, 2026). All code, prompts, coding instructions, raw responses and derived tables are kept in a version-controlled repository so that every number reported in this chapter can be regenerated from the raw data.

## Categories and Brands

Two product categories were chosen in which Indian D2C brands compete directly with established incumbents and in which shoppers commonly ask for recommendations: skincare, with a focus on face serums and moisturisers, and wireless earbuds. Skincare is an experience good whose quality is hard to judge before purchase, so brand reputation and third-party testimony carry weight (Chu & Hou, 2026). Wireless earbuds are a specification-heavy category in which Indian D2C brands lead on volume: in the second quarter of 2026, boAt alone held 34.7% of India's earwear shipments according to IDC (Baburajan, 2026).

Six brands were selected per category, three D2C-origin brands and three incumbents (Table 1). Brands were classified by origin. A D2C-origin brand is an Indian brand launched in 2013 or later that built its business first through its own website and online marketplaces. An incumbent is a brand established in the category, in India or globally, before that wave, and sold through multi-channel distribution backed by mass media. Selection criteria were national availability, presence on major Indian marketplaces and a clear positioning statement on the brand's official website. Ownership was verified on the first day of data collection from company announcements and business press, because several Indian D2C brands have been acquired. Minimalist is the clearest case: D2C in origin, it has been majority-owned since 2025 by Hindustan Unilever, which also owns the incumbent Lakmé. The analysis classifies it by origin and repeats key comparisons without it.

Each brand's positioning was taken from its own website on the same day and coded into a closed set of attribute codes, the same codes later applied to model descriptions. Only attributes the brand claims for itself in its own words were coded.

@TABLE outputs/tables/table1_brands.csv | **Table 1.** Study brands, origin, ownership and self-declared positioning | *Note.* Ownership and positioning verified from company websites and announcements on [DATE]. Positioning attributes were coded from the brand's own wording using the attribute codes in the coding manual; source URLs are listed in the replication files.

## Prompt Design

Thirty prompts were written for each category, in four types (Table 2). Generic prompts ask for the best products in the category. Use-case prompts add a need or situation, such as oily skin, humid weather in Mumbai or calls on a local train, and correspond to category entry points. Price-band prompts set a ceiling in rupees at realistic Indian price points. Comparison prompts name one D2C-origin brand and one incumbent. The comparison pairs were balanced so that each study brand appears in exactly two prompts, and the D2C-origin brand is named first in half of them.

Prompts were written in plain English in the way Indian shoppers phrase such questions, with "in India" where it would naturally appear. No generic, use-case or price-band prompt names a brand; a script confirmed that none contains any brand name or alias in the study set. These 48 prompts are used for awareness, prominence and sources. The 12 comparison prompts are used only for model image and accuracy, because naming a brand in the prompt guarantees its appearance in the answer. The full prompt set is reproduced in Appendix A. It was frozen, and its SHA-256 hash recorded, before data collection began.

@TABLE outputs/tables/table2_prompt_design.csv | **Table 2.** Prompt design | *Note.* Full prompt list in Appendix A. Rs. denotes Indian rupees.

## Platforms and Data Collection

Each prompt was submitted five times to each of four platforms, giving 60 prompts x 4 platforms x 5 repetitions = 1,200 scheduled calls. The platforms were reached through the official programmatic interfaces each provider offers, because the consumer apps cannot be queried at this scale reliably or within their terms of use.

- **ChatGPT** was represented by the OpenAI Responses API with its built-in web search tool, using [MODEL], the API counterpart of the default model for free ChatGPT users at the time of collection. The approximate user location was set to Mumbai, India, and the model was left to decide whether to search, as in the consumer product.
- **Gemini** was represented by the Gemini API with grounding in Google Search, using [MODEL], the model then serving free users of the Gemini app. The grounding tool accepts no location parameter; all requests originated from Mumbai.
- **Perplexity** was represented by the Perplexity Agent API with its "fast" preset, which Perplexity designates as the successor to the Sonar model it retired on 27 September 2026. The preset bundles Perplexity's own system prompt and search configuration; at the time of collection it generated answers with [MODEL]. Location was set to Mumbai, India.
- **Google AI Overviews** were captured from Google Search results for India (google.co.in, English, location Mumbai) through the SerpApi service, with caching disabled so that every repetition triggered a fresh search. When Google showed no AI Overview for a query, the call was recorded as "no overview", a non-response, rather than as zero visibility.

Each repetition was an independent call with no conversation history. Sampling settings were left at platform defaults, since the aim was to observe what the systems produce by default, and no system prompt was added. The 1,200 calls were placed in an order randomised with a fixed seed, so that time-of-day effects were spread across prompts and platforms rather than concentrated on any of them. Data were collected between [START] and [END] IST. Each record stores the exact request parameters, the model identifier returned by the platform, timestamps in UTC and IST, the full response text, every displayed source with its URL, and the raw response. Failed calls were retried up to twice with back-off and recorded as failures if they still failed; none were dropped or replaced. Figure 2 summarises the pipeline with the realised counts.

@FIG outputs/figures/fig2_pipeline.png | **Figure 2.** Audit pipeline with realised counts. All counts are read by script from the collection log and output tables.

Access through APIs has a cost that the design cannot remove. API outputs can differ from what a person sees in the consumer app, because the apps add their own system prompts, personalisation, interface features and, in some cases, different search back-ends. Marin et al. (2026) found that domains displayed for the same query overlapped by only 12.0% between ChatGPT's API and its interface, and by 14.8% for Gemini. Żatuchin (2026b), on the other hand, found that the instability of top recommendations was the same in the ChatGPT interface and in the API. The findings below therefore describe what the four systems produce under documented, reproducible conditions, which is close to, but not identical with, what Indian consumers see.

## Coding

Responses were coded at two levels: the response, and each study brand within a response. A written coding manual defined every variable and decision rule before coding began (Krippendorff, 2019).

**Mentions and position** were detected deterministically. Each brand had an alias list covering spelling variants, legal names and distinctive product lines (for example "Airdopes" for boAt and "Hydro Boost" for Neutrogena). Aliases were matched on word boundaries after URLs and citation markers had been removed from the answer text. Four brand names are also ordinary words or ingredients: Minimalist ("a minimalist routine"), Plum ("Kakadu plum extract"), Noise ("noise cancellation") and boAt. For these, matches were case-sensitive where appropriate, known non-brand phrases were excluded, and every remaining match was cross-checked against the coder's judgement described below, with disagreements resolved by a human author. Position is the order in which a brand is first named among all brands in the answer.

**Answer form, top pick, stance, attributes, sentiment and factual claims** were coded with a large language model as first-pass coder, a practice that performs well on annotation tasks but requires validation against human coders (Gilardi et al., 2023; Pangakis et al., 2023). The coder was Claude Opus 5.5 (Anthropic), chosen because its provider is independent of the four audited platforms; language models used as evaluators have been shown to favour text they themselves generated (Panickssery et al., 2024). The coder saw only the shopper's question and the answer text. It did not see the platform, the repetition or any brand's classification. It received the full coding manual and returned output constrained to a fixed schema that required a decision for every study brand in the category. Attributes were coded from a closed list of sixteen codes per category. Sentiment towards each brand was coded as positive, neutral, mixed or negative.

**Factual accuracy** was assessed for claims about price, composition or specification, and origin or ownership. Each claim was compared with a fact sheet compiled from the brand's official website and recorded with source URL and retrieval date. Claims were classed as correct, incorrect or unverifiable; a price counted as correct when it fell within 20% of the official maximum retail price of the product named. Unverifiable claims are reported separately and are not counted as errors.

**Displayed sources** were classified by registered domain into seven types (brand-owned, marketplace or retailer, review or comparison site, community or user-generated, editorial or press, encyclopaedic, video) plus "other", using a hand-built lookup table. Domains not in the table were classified by an author after inspection, never by guesswork. For ChatGPT and Gemini the displayed sources are the inline citations attached to the answer; for Perplexity they are the search results returned as source cards; for AI Overviews they are the references listed in the overview panel.

## Measures

Table 3 defines the measures. Awareness and prominence are computed on the 48 non-branded prompts only. The denominator for every rate is the number of valid responses, which excludes failed calls and AI Overview no-shows; denominators are reported with each estimate.

@TABLE outputs/tables/table3_measures.csv | **Table 3.** Measures of Generative Brand Equity | *Note.* Valid responses exclude failed calls and AI Overview no-shows. Jaccard (1912) similarity J(A, B) = |A ∩ B| / |A ∪ B|; two empty sets are counted as identical (J = 1), and the share of such pairs is reported.

## Analysis

The analysis is descriptive and comparative. Because the five repetitions of a prompt on a platform are not independent of one another, uncertainty is estimated with a cluster bootstrap that resamples prompts rather than individual responses (Field & Welsh, 2007), using 2,000 resamples and percentile 95% confidence intervals (Efron & Tibshirani, 1994). Differences between D2C-origin brands and incumbents are reported as differences in proportions with these intervals. As a check, the same contrasts are estimated with a logistic generalised estimating equation (GEE) with exchangeable correlation within prompts (Liang & Zeger, 1986). Effect sizes are reported alongside any test, and with only six brands per category the brand-type comparisons are treated as descriptive of this brand set rather than as estimates for D2C brands in general. Agreement between model visibility and marketplace benchmarks is summarised with Spearman's rank correlation, with *n* stated.

## Benchmarks

To see whether generative visibility reflects market standing, model measures are compared with two kinds of benchmark. Marketplace ratings and review counts for each brand's best-selling product in the category were recorded by hand by two authors on a single date from Amazon.in, Flipkart and, for skincare, Nykaa; no marketplace was scraped. For earbuds, publicly reported shipment shares from IDC's India wearables tracker are used where available. Market share data for private D2C skincare brands are not public, which limits this comparison for skincare.

## Reliability

Two authors independently coded a stratified random 20% sample of valid responses, stratified by platform and category and drawn with a fixed seed, using the same coding manual as the language model and without seeing its codes. Agreement between the two authors was assessed with Cohen's kappa (Cohen, 1960), interpreted with conventional benchmarks (Landis & Koch, 1977), and disagreements were resolved by discussion to form a consensus code. The language model's codes were then compared with that consensus. To check the coder's consistency, a random 10% of responses was coded a second time in a separate run, and agreement between the two runs is reported. Variables with kappa below 0.60 were to be flagged, the manual revised and the variable re-coded, as recommended in the content analysis literature (Lombard et al., 2002).

## Ethical Considerations and Use of AI Tools

The study involves no human participants and no personal data. All platforms were accessed through their official APIs and within their published terms; no consumer interface was automated and no marketplace was scraped. Brand names are reported because the analysis concerns public representations of brands, but the findings describe model outputs during a specified window and are not judgements of product quality. In line with the publisher's policy on generative AI, the authors disclose two uses. A large language model (Claude Opus 5.5, Anthropic) served as first-pass coder, with human validation as described above, and AI assistance was used in writing analysis code and in language editing. The authors take full responsibility for the content.

# FINDINGS

[FINDINGS: written from outputs/tables after the audit and verification. Structure: Collection outcomes; Model Awareness and Prominence (RQ1); Model Image and Accuracy (RQ2); Sources Behind Recommendations (RQ3); Stability Across Runs and Platforms (RQ4); Comparison With Market Benchmarks.]

# DISCUSSION

[DISCUSSION: written after findings.]

# SOLUTIONS AND RECOMMENDATIONS

[RECOMMENDATIONS: revised after findings.]

# GOVERNANCE AND MARKET STRUCTURE

[GOVERNANCE-FINDINGS: one or two sentences linking the findings to concentration.] If generative systems systematically favour brands with long histories and dense press coverage, they create a new barrier to entry at the very point where digital commerce was supposed to lower one. Wen et al. (2026) argue that generative engine optimisation concentrates influence in the hands of whoever can supply the evidence that models read, and that oversight should therefore look at answers rather than at individual web pages.

Disclosure is the second concern. A shopper who receives a synthesised recommendation usually cannot tell which sources informed it, whether a commercial relationship shaped it, or how much it would change if the question were asked again. Advertising is now arriving inside these systems. In January 2026 OpenAI announced that it would test advertisements in the free and Go tiers of ChatGPT in the United States, labelled as sponsored and kept separate from answers, and stated that answers would not be influenced by advertisers (OpenAI, 2026). Whether that separation holds, and how anyone outside the company could check it, are open questions.

Existing rules reach these issues only at their edges. In the European Union, the Digital Services Act requires online platforms to explain the main parameters of their recommender systems (European Parliament & Council of the European Union, 2022). The Artificial Intelligence Act adds transparency duties for certain AI systems (European Parliament & Council of the European Union, 2024). In India, the Central Consumer Protection Authority's 2023 guidelines list "disguised advertisement", advertising made to look like reviews, news or other content, among prohibited dark patterns (Central Consumer Protection Authority, 2023). Amendments to the Consumer Protection (E-Commerce) Rules, notified in September 2026 and in force from January 2027, require marketplaces to label sponsored listings clearly and to explain, in order of importance, the parameters that determine ranking. They also extend the idea of ranking to prominence given "irrespective of the technology used" (George et al., 2026). That wording may reach AI shopping assistants operated by marketplaces, but general-purpose assistants such as ChatGPT or Gemini are not marketplaces, and India's AI Governance Guidelines of November 2025 favour voluntary measures over new statutory duties (Ministry of Electronics and Information Technology, 2025). How any of these instruments applies to an assistant that names three serums in reply to a question is unsettled. Repeatable audits of the kind reported here could give regulators evidence they do not currently have: which brands are shown, on what evidence, and how consistently.

# FUTURE RESEARCH DIRECTIONS

[FUTURE-FINDINGS: one sentence tying the agenda to the main finding.] Six directions follow from the framework and from the limits of this study.

The first is the link between Generative Brand Equity and consumer response, which the framework proposes and the audit does not test. Experiments could show participants answers that vary a brand's presence, position and description while holding everything else constant, and measure consideration, attitude and choice. Field evidence that assistant recommendations change later search behaviour (Iannelli & Ai, 2026) makes this link worth estimating carefully in Indian categories.

The second is language. Indian shoppers search in Hindi, Hinglish, Tamil, Marathi and other languages, AI Overviews are offered in several of them, and query language can decide whether local brands appear at all (Żatuchin, 2026b). Repeating the audit across languages, with prompts translated and back-translated rather than machine-rendered, would show whether Indian D2C brands fare differently when the question is asked in an Indian language.

The third is time. A single collection window shows a snapshot. Monthly or quarterly repetition with a frozen prompt set would show whether visibility advantages persist through model updates, and whether a brand's position changes after an event such as an acquisition, a product recall or a burst of press coverage.

The fourth is intervention. The GEO evidence is strongest for content already retrieved into a model's context and weakest for effects on organic discoverability (Martinez, 2026). Field experiments in which brands publish new third-party content, such as independent reviews, expert explainers or corrected reference entries, and auditors measure the change in model outputs before and after, would test the mechanisms that this chapter can only describe.

The fifth is the consumer interface. API-based audits trade realism for reproducibility. Data-donation designs, in which consenting shoppers share the answers they actually received on their phones, could measure how far personalisation, interface features and mobile layouts move the results reported here.

The sixth is agentic commerce. Assistants are beginning to compare, add to cart and purchase on a shopper's behalf. When the model's choice replaces the consumer's, model awareness and prominence stop being antecedents of choice and become the choice itself. The measurement protocol in this chapter could be extended to agentic settings, and to the shopping assistants run by marketplaces, which fall more clearly under India's e-commerce rules.

# LIMITATIONS

[LIMITATIONS-FINDINGS: add any limitation revealed by the data, such as the AI Overview trigger rate.] The study has limits that bear on how its findings should be read. It observes four systems through their APIs during one short window, and both the systems and the models behind them are updated often; the results describe model behaviour at that time and may not hold later. API outputs can differ from what consumers see in the apps (Marin et al., 2026), and the personalisation that consumer apps apply is absent here. The prompts are in English, although many Indian shoppers search in other languages and query language can change which brands appear (Żatuchin, 2026b). Two categories and twelve brands cannot represent the Indian D2C sector, so the brand-type comparisons describe this brand set and are not estimates for D2C brands in general. AI Overviews were captured on desktop through a third-party service, whereas most Indian searches take place on mobile. A language model performed the first pass of coding; its agreement with human coders is reported, but some coding error remains, and accuracy could be assessed only for claims that official sources could confirm or contradict. Marketplace ratings and review counts are imperfect proxies for market presence, and market shares of private D2C skincare brands are not public. Finally, the study measures what models say. It does not establish how consumers respond.

# CONCLUSION

[CONCLUSION: written after findings.]

# REFERENCES

@REF Aaker, D. A. (1991). *Managing brand equity: Capitalizing on the value of a brand name*. Free Press.
@REF Aggarwal, P., Murahari, V., Rajpurohit, T., Kalyan, A., Narasimhan, K., & Deshpande, A. (2024). GEO: Generative engine optimization. In *Proceedings of the 30th ACM SIGKDD Conference on Knowledge Discovery and Data Mining* (pp. 5–16). Association for Computing Machinery. https://doi.org/10.1145/3637528.3671900
@REF Atıl, B., Aykent, S., Chittams, A., Fu, L., Passonneau, R. J., Radcliffe, E., Rajagopal, G. R., Sloan, A., Tudrej, T., Ture, F., Wu, Z., Xu, L., & Baldwin, B. (2025). Non-determinism of "deterministic" LLM system settings in hosted environments. In *Proceedings of the 5th Workshop on Evaluation and Comparison of NLP Systems* (pp. 135–148). Association for Computational Linguistics. https://doi.org/10.18653/v1/2025.eval4nlp-1.12
@REF Baburajan, K. (2026, September 8). India wearables market falls 7.4% to 24.7 million units in Q2 2026 as premium smartwatches, AI earwear gain ground. *TelecomLead*. https://telecomlead.com/smart-phone/india-wearables-market-falls-7-4-to-24-7-million-units-in-q2-2026-as-premium-smartwatches-ai-earwear-gain-ground-127638
@REF Brynjolfsson, E., Hu, Y., & Simester, D. (2011). Goodbye Pareto principle, hello long tail: The effect of search costs on the concentration of product sales. *Management Science, 57*(8), 1373–1386. https://doi.org/10.1287/mnsc.1110.1371
@REF Central Consumer Protection Authority. (2023). *Guidelines for prevention and regulation of dark patterns, 2023*. Government of India.
@REF Chapekis, A., & Lieb, A. (2025, July 22). *Google users are less likely to click on links when an AI summary appears in the results*. Pew Research Center. https://www.pewresearch.org/short-reads/2025/07/22/google-users-are-less-likely-to-click-on-links-when-an-ai-summary-appears-in-the-results/
@REF Chen, M., Wang, X., Chen, K., & Koudas, N. (2025). *Generative engine optimization: How to dominate AI search* (arXiv:2509.08919). arXiv. https://doi.org/10.48550/arXiv.2509.08919
@REF Chevalier, J. A., & Mayzlin, D. (2006). The effect of word of mouth on sales: Online book reviews. *Journal of Marketing Research, 43*(3), 345–354. https://doi.org/10.1509/jmkr.43.3.345
@REF Chu, X., & Hou, Y. (2026). *Incumbent advantage: Brand bias and cognitive manipulation dynamics in LLM recommendation systems* (arXiv:2606.17443). arXiv. https://doi.org/10.48550/arXiv.2606.17443
@REF Cohen, J. (1960). A coefficient of agreement for nominal scales. *Educational and Psychological Measurement, 20*(1), 37–46. https://doi.org/10.1177/001316446002000104
@REF Dellaert, B. G. C., Shu, S. B., Arentze, T. A., Baker, T., Diehl, K., Donkers, B., Fast, N. J., Häubl, G., Johnson, H., Karmarkar, U. R., Oppewal, H., Schmitt, B. H., Schroeder, J., Spiller, S. A., & Steffel, M. (2020). Consumer decisions with artificially intelligent voice assistants. *Marketing Letters, 31*(4), 335–347. https://doi.org/10.1007/s11002-020-09537-5
@REF Dellarocas, C. (2003). The digitization of word of mouth: Promise and challenges of online feedback mechanisms. *Management Science, 49*(10), 1407–1424. https://doi.org/10.1287/mnsc.49.10.1407.17308
@REF Edelman, B., & Lai, Z. (2016). Design of search engine services: Channel interdependence in search engine results. *Journal of Marketing Research, 53*(6), 881–900. https://doi.org/10.1509/jmr.14.0528
@REF Efron, B., & Tibshirani, R. J. (1994). *An introduction to the bootstrap*. Chapman & Hall/CRC. https://doi.org/10.1201/9780429246593
@REF Erdem, T., & Swait, J. (1998). Brand equity as a signaling phenomenon. *Journal of Consumer Psychology, 7*(2), 131–157. https://doi.org/10.1207/s15327663jcp0702_02
@REF Erdem, T., & Swait, J. (2004). Brand credibility, brand consideration, and choice. *Journal of Consumer Research, 31*(1), 191–198. https://doi.org/10.1086/383434
@REF European Parliament & Council of the European Union. (2022). Regulation (EU) 2022/2065 of 19 October 2022 on a Single Market for Digital Services and amending Directive 2000/31/EC (Digital Services Act). *Official Journal of the European Union*, L 277, 1–102. http://data.europa.eu/eli/reg/2022/2065/oj
@REF European Parliament & Council of the European Union. (2024). Regulation (EU) 2024/1689 of 13 June 2024 laying down harmonised rules on artificial intelligence (Artificial Intelligence Act). *Official Journal of the European Union*, L, 2024/1689. http://data.europa.eu/eli/reg/2024/1689/oj
@REF Field, C. A., & Welsh, A. H. (2007). Bootstrapping clustered data. *Journal of the Royal Statistical Society: Series B (Statistical Methodology), 69*(3), 369–390. https://doi.org/10.1111/j.1467-9868.2007.00593.x
@REF Fleder, D., & Hosanagar, K. (2009). Blockbuster culture's next rise or fall: The impact of recommender systems on sales diversity. *Management Science, 55*(5), 697–712. https://doi.org/10.1287/mnsc.1080.0974
@REF George, S., Sudersan, H., & Lateefi, B. (2026, September 28). Consumer Protection (E-Commerce) (Amendment) Rules 2026: From consumer disclosure to platform governance. *Bar & Bench*. https://www.barandbench.com/law-firms/view-point/consumer-protection-e-commerce-amendment-rules-2026-from-consumer-disclosure-to-platform-governance
@REF Gilardi, F., Alizadeh, M., & Kubli, M. (2023). ChatGPT outperforms crowd workers for text-annotation tasks. *Proceedings of the National Academy of Sciences, 120*(30), Article e2305016120. https://doi.org/10.1073/pnas.2305016120
@REF Grewal, D., Satornino, C. B., Davenport, T., & Guha, A. (2025). How generative AI is shaping the future of marketing. *Journal of the Academy of Marketing Science, 53*(3), 702–722. https://doi.org/10.1007/s11747-024-01064-3
@REF Hartmann, J., Exner, Y., & Domdey, S. (2025). The power of generative marketing: Can generative AI create superhuman visual marketing content? *International Journal of Research in Marketing, 42*(1), 13–31. https://doi.org/10.1016/j.ijresmar.2024.09.002
@REF Häubl, G., & Trifts, V. (2000). Consumer decision making in online shopping environments: The effects of interactive decision aids. *Marketing Science, 19*(1), 4–21. https://doi.org/10.1287/mksc.19.1.4.15178
@REF Hermann, E., & Puntoni, S. (2025). Generative AI in marketing and principles for ethical design and deployment. *Journal of Public Policy & Marketing, 44*(3), 332–349. https://doi.org/10.1177/07439156241309874
@REF Hovland, C. I., & Weiss, W. (1951). The influence of source credibility on communication effectiveness. *Public Opinion Quarterly, 15*(4), 635–650. https://doi.org/10.1086/266350
@REF Iannelli, M., & Ai, A. (2026). *From prompt to purchase: How AI brand recommendations move consumers on the open web* (arXiv:2606.10907). arXiv. https://doi.org/10.48550/arXiv.2606.10907
@REF Introna, L. D., & Nissenbaum, H. (2000). Shaping the web: Why the politics of search engines matters. *The Information Society, 16*(3), 169–185. https://doi.org/10.1080/01972240050133634
@REF Jaccard, P. (1912). The distribution of the flora in the alpine zone. *New Phytologist, 11*(2), 37–50. https://doi.org/10.1111/j.1469-8137.1912.tb05611.x
@REF Jack, W., Lehman, N., Maloney, K., & Xu, S. (2026). *Prominence-stratified failure modes in retrieval-augmented commercial recommendation: A 37,000-run audit* (arXiv:2605.27439). arXiv. https://doi.org/10.48550/arXiv.2605.27439
@REF Ji, Z., Lee, N., Frieske, R., Yu, T., Su, D., Xu, Y., Ishii, E., Bang, Y. J., Madotto, A., & Fung, P. (2023). Survey of hallucination in natural language generation. *ACM Computing Surveys, 55*(12), Article 248. https://doi.org/10.1145/3571730
@REF Kamruzzaman, M., Nguyen, H. M., & Kim, G. L. (2024). "Global is good, local is bad?": Understanding brand bias in LLMs. In *Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing* (pp. 12695–12702). Association for Computational Linguistics. https://doi.org/10.18653/v1/2024.emnlp-main.707
@REF Kandpal, N., Deng, H., Roberts, A., Wallace, E., & Raffel, C. (2023). Large language models struggle to learn long-tail knowledge. In *Proceedings of the 40th International Conference on Machine Learning* (Proceedings of Machine Learning Research, Vol. 202, pp. 15696–15707). PMLR. https://proceedings.mlr.press/v202/kandpal23a.html
@REF Kannan, P. K., & Li, H. A. (2017). Digital marketing: A framework, review and research agenda. *International Journal of Research in Marketing, 34*(1), 22–45. https://doi.org/10.1016/j.ijresmar.2016.11.006
@REF Keller, K. L. (1993). Conceptualizing, measuring, and managing customer-based brand equity. *Journal of Marketing, 57*(1), 1–22. https://doi.org/10.1177/002224299305700101
@REF Keller, K. L. (2016). Reflections on customer-based brand equity: Perspectives, progress, and priorities. *AMS Review, 6*(1–2), 1–16. https://doi.org/10.1007/s13162-016-0078-z
@REF Kohli, C. (2025, July 18). Airtel partners with Perplexity to offer free Pro subscriptions. *MediaNama*. https://www.medianama.com/2025/07/223-airtel-partners-perplexity-free-pro-subscriptions/
@REF Krippendorff, K. (2019). *Content analysis: An introduction to its methodology* (4th ed.). SAGE. https://doi.org/10.4135/9781071878781
@REF Kumar, A., & Lakkaraju, H. (2024). *Manipulating large language models to increase product visibility* (arXiv:2404.07981). arXiv. https://doi.org/10.48550/arXiv.2404.07981
@REF Landis, J. R., & Koch, G. G. (1977). The measurement of observer agreement for categorical data. *Biometrics, 33*(1), 159–174. https://doi.org/10.2307/2529310
@REF Lavidge, R. J., & Steiner, G. A. (1961). A model for predictive measurements of advertising effectiveness. *Journal of Marketing, 25*(6), 59–62. https://doi.org/10.1177/002224296102500611
@REF Lewis, P., Perez, E., Piktus, A., Petroni, F., Karpukhin, V., Goyal, N., Küttler, H., Lewis, M., Yih, W., Rocktäschel, T., Riedel, S., & Kiela, D. (2020). Retrieval-augmented generation for knowledge-intensive NLP tasks. In *Advances in Neural Information Processing Systems* (Vol. 33, pp. 9459–9474). Curran Associates.
@REF Liang, K.-Y., & Zeger, S. L. (1986). Longitudinal data analysis using generalized linear models. *Biometrika, 73*(1), 13–22. https://doi.org/10.1093/biomet/73.1.13
@REF Liu, N. F., Zhang, T., & Liang, P. (2023). Evaluating verifiability in generative search engines. In *Findings of the Association for Computational Linguistics: EMNLP 2023* (pp. 7001–7025). Association for Computational Linguistics. https://doi.org/10.18653/v1/2023.findings-emnlp.467
@REF Lombard, M., Snyder-Duch, J., & Bracken, C. C. (2002). Content analysis in mass communication: Assessment and reporting of intercoder reliability. *Human Communication Research, 28*(4), 587–604. https://doi.org/10.1111/j.1468-2958.2002.tb00826.x
@REF Mallen, A., Asai, A., Zhong, V., Das, R., Khashabi, D., & Hajishirzi, H. (2023). When not to trust language models: Investigating effectiveness of parametric and non-parametric memories. In *Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)* (pp. 9802–9822). Association for Computational Linguistics. https://doi.org/10.18653/v1/2023.acl-long.546
@REF Malthouse, E., Lee, K.-Y., Yang, J., Pal, S., & Feng, X. (2026). *Evaluating brand retrieval and ranking in large language model recommendations* (arXiv:2609.16304). arXiv. https://doi.org/10.48550/arXiv.2609.16304
@REF Marin, L. G. U.-B., Bertaglia, T., Astante, G., Rijsbosch, B., van Dijck, G., Hannák, A., Spanakis, G., & Kollnig, K. (2026). *"If I had to buy just ONE: Galaxy S26 Ultra": Auditing AI-generated product recommendations* (arXiv:2609.18729). arXiv. https://doi.org/10.48550/arXiv.2609.18729
@REF Martinez, O. (2026). *Optimizing visibility in generative engines: A critical survey of generative engine optimization (2023–2026)* (arXiv:2607.14035). arXiv. https://doi.org/10.48550/arXiv.2607.14035
@REF Martins, M. (2025, April 23). Hindustan Unilever completes acquisition of 90.5 percent stake in Minimalist for Rs 2,706 crore. *FashionNetwork*. https://in.fashionnetwork.com/news/Hindustan-unilever-completes-acquisition-of-90-5-percent-stake-in-minimalist-for-rs-2-706-crore,1722276.html
@REF Metaxa, D., Park, J. S., Robertson, R. E., Karahalios, K., Wilson, C., Hancock, J., & Sandvig, C. (2021). Auditing algorithms: Understanding algorithmic systems from the outside in. *Foundations and Trends in Human–Computer Interaction, 14*(4), 272–344. https://doi.org/10.1561/1100000083
@REF Ministry of Electronics and Information Technology. (2025). *India AI governance guidelines: Enabling safe and trusted AI innovation*. Government of India. https://static.pib.gov.in/WriteReadData/specificdocs/documents/2025/nov/doc2025115685601.pdf
@REF Nedungadi, P. (1990). Recall and consumer consideration sets: Influencing choice without altering brand evaluations. *Journal of Consumer Research, 17*(3), 263–276. https://doi.org/10.1086/208556
@REF Nestaas, F., Debenedetti, E., & Tramèr, F. (2025). Adversarial search engine optimization for large language models. In *The Thirteenth International Conference on Learning Representations (ICLR 2025)*. https://openreview.net/forum?id=hkdqxN3c7t
@REF News On AIR. (2024, August 15). *Google expands 'AI Overviews' feature to India & five other countries*. Prasar Bharati. https://www.newsonair.gov.in/google-expands-ai-overviews-feature-to-india-five-other-countries
@REF OpenAI. (2026, January 16). *Our approach to advertising and expanding access to ChatGPT*. https://openai.com/index/our-approach-to-advertising-and-expanding-access/
@REF Ouyang, S., Zhang, J. M., Harman, M., & Wang, M. (2025). An empirical study of the non-determinism of ChatGPT in code generation. *ACM Transactions on Software Engineering and Methodology, 34*(2), 1–28. https://doi.org/10.1145/3697010
@REF Pan, B., Hembrooke, H., Joachims, T., Lorigo, L., Gay, G., & Granka, L. (2007). In Google we trust: Users' decisions on rank, position, and relevance. *Journal of Computer-Mediated Communication, 12*(3), 801–823. https://doi.org/10.1111/j.1083-6101.2007.00351.x
@REF Pangakis, N., Wolken, S., & Fasching, N. (2023). *Automated annotation with generative AI requires validation* (arXiv:2306.00176). arXiv. https://doi.org/10.48550/arXiv.2306.00176
@REF Panickssery, A., Bowman, S. R., & Feng, S. (2024). LLM evaluators recognize and favor their own generations. In *Advances in Neural Information Processing Systems* (Vol. 37, pp. 68772–68802). Curran Associates. https://doi.org/10.52202/079017-2197
@REF Pitenin, V. (2026). *Invisible to the machine: Auditing AI restaurant, cafe, and bar recommendation against a complete market census* (arXiv:2608.07069). arXiv. https://doi.org/10.48550/arXiv.2608.07069
@REF Puerto, H., Gubri, M., Green, T., Oh, S. J., & Yun, S. (2025). C-SEO Bench: Does conversational SEO work? In *Advances in Neural Information Processing Systems 38: Datasets and Benchmarks Track*. https://openreview.net/forum?id=oTeixD3oZO
@REF Puntoni, S., Reczek, R. W., Giesler, M., & Botti, S. (2021). Consumers and artificial intelligence: An experiential perspective. *Journal of Marketing, 85*(1), 131–151. https://doi.org/10.1177/0022242920953847
@REF Rienecker, J., Mpofu, K., Goel, N., Datta, S., Zhao, J., Danielsson, O., & Thorsen, F. (2026). *Auditing preferences for brands and cultures in LLMs* (arXiv:2603.18300). arXiv. https://doi.org/10.48550/arXiv.2603.18300
@REF Romaniuk, J., & Sharp, B. (2004). Conceptualizing and measuring brand salience. *Marketing Theory, 4*(4), 327–342. https://doi.org/10.1177/1470593104047643
@REF Romaniuk, J., & Sharp, B. (2016). *How brands grow: Part 2*. Oxford University Press.
@REF Sandvig, C., Hamilton, K., Karahalios, K., & Langbort, C. (2014, May 22). *Auditing algorithms: Research methods for detecting discrimination on internet platforms* [Paper presentation]. Data and Discrimination: Converting Critical Concerns into Productive Inquiry, preconference of the 64th Annual Meeting of the International Communication Association, Seattle, WA, United States.
@REF Sharma, N., Liao, Q. V., & Xiao, Z. (2024). Generative echo chamber? Effect of LLM-powered search systems on diverse information seeking. In *Proceedings of the 2024 CHI Conference on Human Factors in Computing Systems* (pp. 1–17). Association for Computing Machinery. https://doi.org/10.1145/3613904.3642459
@REF Sharp, B. (2010). *How brands grow: What marketers don't know*. Oxford University Press.
@REF Shocker, A. D., Ben-Akiva, M., Boccara, B., & Nedungadi, P. (1991). Consideration set influences on consumer decision-making and choice: Issues, models, and suggestions. *Marketing Letters, 2*(3), 181–197. https://doi.org/10.1007/BF00554125
@REF Singh, J. (2025, October 27). OpenAI offers free ChatGPT Go for one year to all users in India. *TechCrunch*. https://techcrunch.com/2025/10/27/openai-offers-free-chatgpt-go-for-one-year-to-all-users-in-india/
@REF Srivastava, S. (2026, February 27). India's D2C journey: After a rapid scale-up, why it's now all about discipline. *Forbes India*. https://www.forbesindia.com/article/enterprise/startups/indias-d2c-journey-after-a-rapid-scale-up-why-its-now-all-about-discipline/2991796/1
@REF Ursu, R. M. (2018). The power of rankings: Quantifying the effect of rankings on online consumer search and purchase decisions. *Marketing Science, 37*(4), 530–552. https://doi.org/10.1287/mksc.2017.1072
@REF Wen, Y., Zhang, N., Yuan, H., Chen, X., Zhang, H., & Guo, H. (2026). *Position: Generative engine optimization creates underexamined risks, governance must target concentration, disclosure, and academic blind spots* (arXiv:2606.12439). arXiv. https://doi.org/10.48550/arXiv.2606.12439
@REF Xiao, B., & Benbasat, I. (2007). E-commerce product recommendation agents: Use, characteristics, and impact. *MIS Quarterly, 31*(1), 137–209. https://doi.org/10.2307/25148784
@REF Yoo, K., Haenlein, M., & Hewett, K. (2025). A whole new world, a new fantastic point of view: Charting unexplored territories in consumer research with generative artificial intelligence. *Journal of the Academy of Marketing Science, 53*(3), 723–759. https://doi.org/10.1007/s11747-025-01097-2
@REF Żatuchin, D. (2026a). *How large language models source brand reputation across languages and markets* (arXiv:2606.25787). arXiv. https://doi.org/10.48550/arXiv.2606.25787
@REF Żatuchin, D. (2026b). *The language of the question selects the market: Query language and exit IP as separable factors in commercial recommendations from a generative search interface* (arXiv:2608.30052). arXiv. https://doi.org/10.48550/arXiv.2608.30052

# ADDITIONAL READING

@REF Bruns, D., Kopka, J. F., Borgmann, L., Prior, S., & Langner, T. (2025). Measuring gaining and holding attention to social media ads with viewport logging: A validation study using mobile eye-tracking. *Journal of Advertising, 54*(5), 655–672. https://doi.org/10.1080/00913367.2025.2524186
@REF Hayes, A. F., & Krippendorff, K. (2007). Answering the call for a standard reliability measure for coding data. *Communication Methods and Measures, 1*(1), 77–89. https://doi.org/10.1080/19312450709336664
@REF Liu, N. F., Lin, K., Hewitt, J., Paranjape, A., Bevilacqua, M., Petroni, F., & Liang, P. (2024). Lost in the middle: How language models use long contexts. *Transactions of the Association for Computational Linguistics, 12*, 157–173. https://doi.org/10.1162/tacl_a_00638
@REF Simonson, I., & Rosen, E. (2014). *Absolute value: What really influences customers in the age of (nearly) perfect information*. HarperBusiness.

# KEY TERMS AND DEFINITIONS

**Generative Brand Equity:** The differential visibility and representation of a brand in the outputs of generative AI systems, relative to competing brands in its category, in response to category-relevant shopper queries.

**Model Awareness:** The share of relevant AI answers that retrieve a brand when the question does not name it; the generative counterpart of unaided recall.

**Model Prominence:** Where a brand appears within an AI answer, captured by its order of mention and by whether it is presented as the single best choice.

**Model Image:** The attributes, benefits, price cues and tone that an AI system attaches to a brand, assessed against the brand's own positioning and against verifiable product facts.

**Model Credibility:** The kinds of sources an AI system displays in support of what it says about a brand, from the brand's own website to marketplaces, reviews, press, reference works and video.

**Share of Model:** A brand's mentions as a proportion of all mentions of a defined set of competing brands across a defined set of AI answers.

**Generative Engine Optimisation (GEO):** Practices intended to raise the likelihood that content is retrieved, cited or reflected in answers produced by generative AI systems.

**Prompt-Based Audit:** A research design in which a frozen set of prompts is submitted repeatedly to one or more AI systems under documented conditions, and the outputs are coded and analysed.

**Run-to-Run Stability:** The consistency of a visibility measure when the same prompt is submitted repeatedly to the same system, measured here as the mean pairwise Jaccard similarity of the brands named.

**D2C-Origin Brand:** A brand that built its business first through its own website and online marketplaces rather than through traditional distribution and mass media, whatever its current ownership.

# APPENDIX A: PROMPT SET

@TABLE outputs/tables/appendix_prompts.csv | **Table A1.** Prompts submitted to all four platforms (frozen before collection) | *Note.* Each prompt was submitted five times to each platform as an independent request. Comparison prompts (SK-C and AU-C) are excluded from awareness and prominence measures.

# DECLARATIONS

**Competing interests.** The authors declare no competing interests. None of the authors has a commercial relationship with any brand, platform or service named in this chapter.

**Funding.** [State any funding, or: This research received no specific grant from any funding agency in the public, commercial or not-for-profit sectors. API costs were met by the authors.]

**Use of generative AI.** A large language model (Claude Opus 5.5, Anthropic) served as the first-pass coder of AI responses, under a written coding manual and with validation against two human coders, as described in the Method section. AI assistance was also used to write analysis code and for language editing. All analyses, interpretations and conclusions are the authors' own, and the authors take full responsibility for the content.

**Data availability.** Prompts, coding manual, analysis code and derived tables are available from the corresponding author on request [or: in a public repository, URL to be added after review to preserve anonymity].
