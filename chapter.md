@TITLE Generative Brand Equity: Auditing How AI Answers Represent Indian D2C Brands
@CENTER [Author 1], [Author 2], [Author 3], [Faculty guide]
@CENTER Mukesh Patel School of Technology Management and Engineering, SVKM's NMIMS, Mumbai, India

# ABSTRACT

[ABSTRACT: written after the audit; 100 to 150 words, third person.]

**Keywords:** Generative Engine Optimisation, Brand Visibility, Consumer-Based Brand Equity, Share-of-Model, AI Search, Algorithm Audit, D2C Brands, India, Emerging Markets

# INTRODUCTION

For roughly two decades, online brand discovery ran on a list. A shopper typed a query, a search engine returned ranked links, and brands competed for position through search engine optimisation, paid search and marketplace advertising. The arrangement was imperfect, but it was legible. A brand could see where it ranked, buy its way onto the page and follow the consequences through clicks and conversions. Even a shopper who never clicked had at least seen the brand name on the results page.

Generative AI systems change that arrangement. Ask ChatGPT, Gemini or Perplexity for a vitamin C serum for oily skin under Rs. 1,000 and the reply is a few paragraphs naming perhaps three to six products, each with a line or two of justification and, on some platforms, a handful of source links. Google's AI Overviews place a similar synthesised paragraph above the familiar results. These answers appear to absorb attention that once went to the links below them. In a panel of United States users observed in March 2025, Google searches that displayed an AI summary led to a click on a traditional result in 8% of visits, against 15% when no summary appeared, and links inside the summary itself were clicked in 1% of visits (Chapekis & Lieb, 2025). The first reader of brand content is increasingly a retrieval-and-synthesis pipeline, and the shopper meets the brand, if at all, through that pipeline's summary.

India is a consequential place to study this shift. OpenAI's chief executive has described India as the company's second-largest market after the United States, and from November 2025 the company offered its ChatGPT Go plan free for a year to users in India (Singh, 2025). Bharti Airtel offered a year of Perplexity Pro to its 360 million customers in July 2025 (Kohli, 2025), and Google's AI Overviews have appeared in Indian search results, in English and Hindi, since August 2024 (News On AIR, 2024). The platform providers are, in effect, competing to become the default first stop for a very large population of new and price-conscious online shoppers.

The shift unsettles assumptions that sit deep in marketing theory. Consumer-based brand equity rests on brand knowledge that consumers build through exposure the firm can shape, much of it through the firm's own communication (Keller, 1993). The mental availability perspective holds that brands grow by coming to mind easily in buying situations (Romaniuk & Sharp, 2016; Sharp, 2010), and consideration set research shows that what is recalled at the point of decision constrains what is chosen (Nedungadi, 1990; Shocker et al., 1991). Under generative mediation the order changes. A model's retrieval precedes the shopper's recall, and the model's few sentences about a brand may be the first, and sometimes the only, account of it that the shopper reads before deciding.

The stakes are uneven. India's direct-to-consumer (D2C) sector is estimated to have grown from under US$5 billion in 2020 to between US$12 and 15 billion in 2025, and to include more than 800 active brands (Srivastava, 2026). Many of these brands, in personal care and consumer electronics especially, reached national scale through social media, influencers and marketplace listings rather than mass media. They compete with domestic and multinational incumbents that have decades of press coverage, reference entries and retail history behind them. Language models answer more reliably about entities that are well documented in their training data (Kandpal et al., 2023; Mallen et al., 2023), and early audits report a tilt towards large and global brands (Chen et al., 2025; Kamruzzaman et al., 2024). If generative systems lean on that kind of documentation, they may reproduce or widen the incumbents' advantage. If they lean instead on recent reviews, community discussion and marketplace content, the same systems could favour brands that were born online. Which of these is happening in India has not been examined.

Research on the question has moved quickly but in separate streams. Computer scientists have formalised generative engine optimisation (GEO) and tested how changes to content affect citation (Aggarwal et al., 2024; Puerto et al., 2025), and a wave of audit studies posted in 2026 has begun to measure which brands language models recommend (Jack et al., 2026; Malthouse et al., 2026; Marin et al., 2026). Marketing scholarship has mostly treated generative AI as a production tool, a strategic capability, a research method or an ethical problem (Grewal et al., 2025; Hartmann et al., 2025; Hermann & Puntoni, 2025; Yoo et al., 2025). What is missing is a marketing construct that treats the model's representation of a brand as an outcome in its own right, connects it to established brand equity theory and measures it with an instrument that respects the non-deterministic behaviour of the systems involved. Evidence from emerging markets, and on challenger brands specifically, is close to absent.

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

Two further properties complicate measurement. Outputs are probabilistic: the same prompt can produce different brands and different descriptions on different occasions, and non-determinism persists even under settings intended to remove it (Atil et al., 2024; Ouyang et al., 2025). Models can also produce fluent statements that are false, the problem studied as hallucination (Ji et al., 2023). A brand can therefore be visible and misdescribed at the same time, with the wrong price band, ingredient or specification attached to it. Neither property fits the idea of generative visibility as a single stable number.

## What Language Models Know About Brands

A model's answer about a product category draws on parametric knowledge absorbed during training and on non-parametric knowledge retrieved at query time. The first kind is uneven. Kandpal et al. (2023) showed that a model's ability to answer a factual question rises with the number of training documents relevant to that question, so that rarely documented facts are learned poorly. Mallen et al. (2023) found the same pattern for entities, with accuracy falling for less popular ones, and showed that retrieval helped most where parametric knowledge was weakest. For brands the implication is direct. A brand with a long trail of press coverage, reference entries and reviews is better represented in what a model knows unaided than a brand a few years old, unless retrieval brings the newer brand into view.

Studies of brand bias point the same way. Kamruzzaman et al. (2024) found that language models associated global brands with positive attributes more readily than local ones, although they also detected country-of-origin effects that could favour local brands in particular contexts. Rienecker et al. (2026) reported that models developed in the United States showed marked preference for American entities across commercial and cultural topics, and Chen et al. (2025) described a "big brand bias" in AI search that niche brands would need to overcome. Research on recommender systems offers two competing expectations. Algorithmic recommendation can concentrate demand on already popular items (Fleder & Hosanagar, 2009), but lower search costs can also spread demand towards niche products (Brynjolfsson et al., 2011). Which tendency dominates in generative answers is an empirical matter, and the answer may differ by category, platform and market.

## Generative Engine Optimisation and Its Limits

Aggarwal et al. (2024) introduced generative engine optimisation as a framework for raising the visibility of content inside generative answers. On a benchmark of diverse queries, they reported that adding citations, quotations and statistics to source pages could raise visibility by up to 40%, while keyword stuffing had little effect, and that the gains varied across domains. Later work has qualified that picture. Puerto et al. (2025) found that most conversational search optimisation methods were largely ineffective, and sometimes harmful, in a benchmark covering question answering and product recommendation; traditional ranking-oriented optimisation worked better, and gains shrank as more competitors adopted the same methods. A 2026 review of 45 GEO studies concluded that the foundational gains hold for content already retrieved into a model's context, and that no reviewed technique had shown a stable, cross-platform effect on organic discoverability (Martinez, 2026).

Other studies show that the selection can be pushed in directions that matter for competition. Kumar and Lakkaraju (2024) showed that a crafted text sequence inserted into a product page raised the chance that a model listed the product as its top recommendation, and Nestaas et al. (2025) demonstrated preference manipulation attacks that steer model-mediated search towards an attacker's content. In skincare, Chu and Hou (2026) found that well-known brands were recommended every time when products were otherwise identical, that a small rating advantage for a competitor was enough to break that dominance, and that authority-style claims, including fabricated clinical evidence, could shift recommendations. Chen et al. (2025) found that AI search leaned heavily on earned, third-party media rather than brand-owned or social content. For marketers, this work raises a question that the GEO literature has not settled: which kinds of sources do platforms actually rely on when they recommend brands, and do those dependencies favour some kinds of brands over others?

## Auditing Brand Recommendations

Algorithm audits study platform behaviour by querying a system systematically and analysing its outputs without access to its internals (Metaxa et al., 2021; Sandvig et al., 2014). The approach has recently been turned on brand recommendations. Malthouse et al. (2026) proposed estimating the probability and rank of brand recommendations by repeated sampling, applied the method to six models in five categories, and found that well-known brands were often omitted and that prominence tracked search interest and online conversation more closely than conventional measures of brand popularity. Jack et al. (2026) audited about 37,000 runs across 19 sectors and reported that roughly half of specialist and regional brands never surfaced at all. A census-based audit of cafes, restaurants and bars in two Indonesian markets found that 85.6% of venues were never recommended, that documentation such as review volume and an own website predicted entry into answers, and that ratings mattered for rank only once a venue had been included (Pitenin, 2026).

Three findings from this work shaped the design of the present study. The first is that answers vary from run to run. Żatuchin (2026a) found that the top recommendation changed across six identical runs for four of six prompts, at the same rate in the ChatGPT web interface and in its API. The second is that what a researcher observes depends on how the system is accessed. Marin et al. (2026) compared consumer interfaces with application programming interfaces (APIs) and found that the domains displayed for the same query overlapped by only 12.0% for ChatGPT and 14.8% for Gemini. The third is that language and location select the market: in Żatuchin's probe, the language of the query decided whether local suppliers appeared at all, while the network location shifted which country's brands were named. Analyses of citations add that third-party sites supply most of the evidence behind brand answers, with Wikipedia the most-cited domain in 11 of 12 languages studied (Żatuchin, 2026b). And an observational study that linked chatbot conversations to clickstream data found that a recommendation from an assistant raised a brand's same-name searches by 4.3 percentage points among users with no recent engagement with the brand (Iannelli & Ai, 2026), early evidence that model recommendations move behaviour outside the chat.

Most of this work is recent and much of it is not yet peer reviewed. It is set largely in North American and European markets, framed in the vocabulary of information retrieval rather than brand theory, and rarely distinguishes challenger brands from incumbents. None of it, to our knowledge, examines Indian brands.

## Generative AI in Marketing Scholarship

Marketing research on generative AI has grown quickly, but most of it concerns how firms and researchers use the technology. Hartmann et al. (2025) showed that AI-generated visual marketing content can match or exceed human-made content under specified conditions. Grewal et al. (2025) examined how generative AI is reshaping marketing strategy and implementation, Yoo et al. (2025) charted its uses in consumer research, and Hermann and Puntoni (2025) set out principles for its ethical design and deployment. In each case the model is an instrument in marketers' hands. Far less work treats the model as an intermediary whose outputs decide which brands consumers hear about and how those brands are described.

## The Indian D2C Context

India suits this question for three reasons. Its D2C sector includes brands that reached national scale within a few years, especially in personal care and consumer audio, and that now compete head-on with domestic and multinational incumbents (Srivastava, 2026). The sector is also consolidating, which blurs the line between challenger and incumbent: Hindustan Unilever, owner of Lakmé, completed the purchase of a 90.5% stake in the skincare brand Minimalist in April 2025 (FashionNetwork, 2025), and The Derma Co belongs to Honasa Consumer, a listed company. Second, Indian purchase journeys run heavily through marketplaces such as Amazon, Flipkart and, in beauty, Nykaa, which generate large volumes of ratings and reviews that may feed generative answers. Third, research on GEO and AI search has concentrated on English-language queries in North American and European markets. The finding that models developed in the United States favour American entities (Rienecker et al., 2026) gives reason to suspect that Indian brands, and young Indian brands in particular, may start at a disadvantage.

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

Two product categories were chosen in which Indian D2C brands compete directly with established incumbents and in which shoppers commonly ask for recommendations: skincare, with a focus on face serums and moisturisers, and wireless earbuds. Skincare is an experience good whose quality is hard to judge before purchase, so brand reputation and third-party testimony carry weight (Chu & Hou, 2026). Wireless earbuds are a specification-heavy category in which Indian D2C brands lead on volume: in the second quarter of 2026, boAt alone held 34.7% of India's earwear shipments according to IDC (TelecomLead, 2026).

Six brands were selected per category, three D2C-origin brands and three incumbents (Table 1). Brands were classified by origin. A D2C-origin brand is an Indian brand launched in 2013 or later that built its business first through its own website and online marketplaces; an incumbent is a brand that was established in the category, in India or globally, before that wave and that sells through multi-channel distribution backed by mass media. Selection criteria were national availability, presence on major Indian marketplaces and a clear positioning statement on the brand's official website. Ownership was verified on the first day of data collection from company announcements and business press, because several Indian D2C brands have been acquired. Minimalist is the clearest case: D2C in origin, it has been majority-owned since 2025 by Hindustan Unilever, which also owns the incumbent Lakmé. The analysis classifies it by origin and repeats key comparisons without it.

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

Access through APIs has a cost that the design cannot remove. API outputs can differ from what a person sees in the consumer app, because the apps add their own system prompts, personalisation, interface features and, in some cases, different search back-ends. Marin et al. (2026) found that domains displayed for the same query overlapped by only 12.0% between ChatGPT's API and its interface, and by 14.8% for Gemini. Żatuchin (2026a), on the other hand, found that the instability of top recommendations was the same in the ChatGPT interface and in the API. The findings below therefore describe what the four systems produce under documented, reproducible conditions, which is close to, but not identical with, what Indian consumers see.

## Coding

Responses were coded at two levels: the response, and each study brand within a response. A written coding manual defined every variable and decision rule before coding began (Krippendorff, 2019).

**Mentions and position** were detected deterministically. Each brand had an alias list covering spelling variants, legal names and distinctive product lines (for example "Airdopes" for boAt and "Hydro Boost" for Neutrogena). Aliases were matched on word boundaries after URLs and citation markers had been removed from the answer text. Four brand names are also ordinary words or ingredients: Minimalist ("a minimalist routine"), Plum ("Kakadu plum extract"), Noise ("noise cancellation") and boAt. For these, matches were case-sensitive where appropriate, known non-brand phrases were excluded, and every remaining match was cross-checked against the coder's judgement described below, with disagreements resolved by a human author. Position is the order in which a brand is first named among all brands in the answer.

**Answer form, top pick, stance, attributes, sentiment and factual claims** were coded with a large language model as first-pass coder, a practice that performs well on annotation tasks but requires validation against human coders (Gilardi et al., 2023; Pangakis et al., 2023). The coder was Claude Opus 5.5 (Anthropic), chosen because its provider is independent of the four audited platforms; language models used as evaluators have been shown to favour text they themselves generated (Panickssery et al., 2024). The coder saw only the shopper's question and the answer text. It did not see the platform, the repetition or any brand's classification. It received the full coding manual and returned output constrained to a fixed schema that required a decision for every study brand in the category. Attributes were coded from a closed list of sixteen codes per category. Sentiment towards each brand was coded as positive, neutral, mixed or negative.

**Factual accuracy** was assessed for claims about price, composition or specification, and origin or ownership. Each claim was compared with a fact sheet compiled from the brand's official website and recorded with source URL and retrieval date. Claims were classed as correct, incorrect or unverifiable; a price counted as correct when it fell within 20% of the official maximum retail price of the product named. Unverifiable claims are reported separately and are not counted as errors.

**Displayed sources** were classified by registered domain into seven types (brand-owned, marketplace or retailer, review or comparison site, community or user-generated, editorial or press, encyclopaedic, video) plus "other", using a hand-built lookup table. Domains not in the table were classified by an author after inspection, never by guesswork. For ChatGPT and Gemini the displayed sources are the inline citations attached to the answer; for Perplexity they are the search results returned as source cards; for AI Overviews they are the references listed in the overview panel.

## Measures

Table 3 defines the measures. Awareness and prominence are computed on the 48 non-branded prompts only. The denominator for every rate is the number of valid responses, which excludes failed calls and AI Overview no-shows; denominators are reported with each estimate.

@TABLE outputs/tables/table3_measures.csv | **Table 3.** Measures of Generative Brand Equity | *Note.* Valid responses exclude failed calls and AI Overview no-shows. J(A, B) = |A ∩ B| / |A ∪ B|; two empty sets are counted as identical (J = 1), and the share of such pairs is reported.

## Analysis

The analysis is descriptive and comparative. Because the five repetitions of a prompt on a platform are not independent of one another, uncertainty is estimated with a cluster bootstrap that resamples prompts rather than individual responses (Field & Welsh, 2007), using 2,000 resamples and percentile 95% confidence intervals. Differences between D2C-origin brands and incumbents are reported as differences in proportions with these intervals. As a check, the same contrasts are estimated with a logistic generalised estimating equation (GEE) with exchangeable correlation within prompts (Liang & Zeger, 1986). Effect sizes are reported alongside any test, and with only six brands per category the brand-type comparisons are treated as descriptive of this brand set rather than as estimates for D2C brands in general. Agreement between model visibility and marketplace benchmarks is summarised with Spearman's rank correlation, with *n* stated.

## Benchmarks

To see whether generative visibility reflects market standing, model measures are compared with two kinds of benchmark. Marketplace ratings and review counts for each brand's best-selling product in the category were recorded by hand by two authors on a single date from Amazon.in, Flipkart and, for skincare, Nykaa; no marketplace was scraped. For earbuds, publicly reported shipment shares from IDC's India wearables tracker are used where available. Market share data for private D2C skincare brands are not public, which limits this comparison for skincare.

## Reliability

Two authors independently coded a stratified random 20% sample of valid responses, stratified by platform and category and drawn with a fixed seed, using the same coding manual as the language model and without seeing its codes. Agreement between the two authors was assessed with Cohen's kappa (Cohen, 1960), interpreted with conventional benchmarks (Landis & Koch, 1977), and disagreements were resolved by discussion to form a consensus code. The language model's codes were then compared with that consensus. To check the coder's consistency, a random 10% of responses was coded a second time in a separate run, and agreement between the two runs is reported. Variables with kappa below 0.60 were to be flagged, the manual revised and the variable re-coded, as recommended in the content analysis literature (Lombard et al., 2002).

## Ethical Considerations and Use of AI Tools

The study involves no human participants and no personal data. All platforms were accessed through their official APIs and within their published terms; no consumer interface was automated and no marketplace was scraped. Brand names are reported because the analysis concerns public representations of brands, but the findings describe model outputs during a specified window and are not judgements of product quality. In line with the publisher's policy on generative AI, the authors disclose that a large language model (Claude Opus 5.5, Anthropic) was used as first-pass coder, with human validation as described above, and that AI assistance was used in writing analysis code and in language editing. The authors take full responsibility for the content.

# FINDINGS

[FINDINGS: written from outputs/tables after the audit and verification. Structure: Collection outcomes; Model Awareness and Prominence (RQ1); Model Image and Accuracy (RQ2); Sources Behind Recommendations (RQ3); Stability Across Runs and Platforms (RQ4); Comparison With Market Benchmarks.]

# DISCUSSION

[DISCUSSION: written after findings.]

# SOLUTIONS AND RECOMMENDATIONS

[RECOMMENDATIONS: revised after findings.]

# GOVERNANCE AND MARKET STRUCTURE

[GOVERNANCE: revised after findings.]

# FUTURE RESEARCH DIRECTIONS

[FUTURE RESEARCH: revised after findings.]

# LIMITATIONS

[LIMITATIONS: revised after findings.]

# CONCLUSION

[CONCLUSION: written after findings.]
