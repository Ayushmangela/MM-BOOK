@TITLE Generative Brand Equity: Auditing How AI Answers Represent Indian D2C Brands
@CENTER [Author 1], [Author 2], [Author 3], [Faculty guide]
@CENTER Mukesh Patel School of Technology Management and Engineering, SVKM's NMIMS, Mumbai, India
@NOTE DRAFT for internal review. Sections 5 and parts of 6 contain placeholders, marked in square brackets, to be completed after the audit is run. Market figures marked [add source] must be filled from a citable source before submission.

# ABSTRACT

Consumers increasingly ask generative AI systems what to buy and receive a short synthesised answer instead of a ranked list of links. In this setting, the classical antecedents of brand performance, such as awareness and perceived quality, are shaped less by exposure a firm buys or controls and more by whether a model retrieves the brand, how it describes it, and which sources it cites in support. This chapter proposes Generative Brand Equity, an adaptation of consumer-based brand equity to machine-mediated discovery, built on four dimensions: model awareness, model prominence, model image and model credibility, with stability treated as a cross-cutting property. The framework is operationalised through a structured prompt-based audit of Indian direct-to-consumer (D2C) brands and established incumbents in two product categories across ChatGPT, Gemini, Perplexity and Google AI Overviews. The chapter contributes a replicable measurement protocol, evidence from an emerging market largely absent from current research, and guidance for resource-constrained brands competing for visibility inside AI answers.

**Keywords:** Generative Engine Optimisation, Brand Visibility, Consumer-Based Brand Equity, Share-of-Model, AI Search, Prompt-Based Audit, D2C Brands, India, Emerging Markets

# INTRODUCTION

For two decades, digital brand discovery followed a familiar logic. A consumer typed a query, a search engine returned a ranked list of links, and brands competed for those positions through search engine optimisation, paid search and marketplace advertising. Even when the consumer did not click, the brand name was visible on the results page. Marketers could observe their rank, buy their way onto the page, and measure what happened next through clicks and conversions.

Generative AI systems change this logic. When a consumer asks ChatGPT, Gemini or Perplexity to recommend a vitamin C serum for oily skin under Rs. 1,000, the system does not return ten links. It returns a short answer naming perhaps three to five brands, with a sentence or two on each, sometimes with citations and sometimes without. Google's AI Overviews now place a similar synthesised answer above traditional search results. The consumer may form a consideration set without ever visiting a brand's website, seeing its advertising, or reading a review directly. The first audience for brand content is no longer the consumer but the retrieval-and-synthesis pipeline that stands between the consumer and the market.

The change has consequences for marketing theory. Established models of brand equity assume that consumers build knowledge of a brand through direct or mediated exposure that the firm can influence (Keller, 1993). Models of mental availability assume that the brand must come to mind in buying situations (Sharp, 2010; Romaniuk & Sharp, 2016). Consideration set research assumes that recall precedes choice (Nedungadi, 1990; Shocker et al., 1991). Under generative mediation, a model's retrieval precedes the consumer's recall, and the model's description of a brand may be the first and only brand image the consumer encounters before deciding.

There are practical consequences too, especially for small and challenger brands. India's direct-to-consumer sector has grown rapidly over the last decade, with brands in personal care, consumer electronics, apparel and food building national presence through social media, influencer marketing and marketplaces rather than mass media [add source on Indian D2C market size and growth]. These brands compete against domestic and global incumbents with far larger media budgets and longer histories of press coverage. If generative systems favour brands with dense coverage in encyclopaedic, editorial and review sources, they may reproduce or even amplify the incumbents' advantage. If they draw heavily on community and review content, they may instead favour digitally native brands. Which of these is happening in India has not yet been studied.

Computer science research has begun to study how content becomes visible in generative engines. Aggarwal et al. (2024) formalised generative engine optimisation (GEO) and showed that traditional keyword tactics have little effect on whether a source is cited, while adding credible statistics and quotations substantially increases it. Marketing scholarship, by contrast, has mostly approached generative AI as a content production tool (Hartmann et al., 2025), as a strategic implementation challenge (Grewal et al., 2025), as a method for consumer research (Yoo et al., 2025), or as an ethics and policy question (Hermann & Puntoni, 2025). Few studies treat the model's representation of a brand as a marketing outcome in its own right, and fewer still offer a measurement protocol that marketing researchers can apply without first reconstructing the technical literature.

In this chapter we take up that gap. Our objectives are to:

- Conceptualise **Generative Brand Equity** as an adaptation of consumer-based brand equity to settings where a model performs the first filtering.
- Design a **replicable prompt-based audit protocol** that treats run-to-run and cross-platform variation as a finding rather than noise.
- Apply the protocol to **Indian D2C and incumbent brands** in two categories across four generative platforms.
- Derive **implications for managers, researchers and policymakers**, particularly for resource-constrained brands.

The rest of the chapter is organised as follows. The next section reviews research on brand equity, mental availability, consideration sets, search and generative engines, and the Indian D2C context. The third section develops the Generative Brand Equity framework and its propositions. The fourth describes the audit method. The fifth reports findings. The sixth and seventh discuss managerial and governance implications. The chapter closes with limitations, future research directions and conclusions.

# BACKGROUND

## Brand Equity and the Exposure Assumption

Consumer-based brand equity is defined as the differential effect of brand knowledge on consumer response to the marketing of the brand (Keller, 1993). Brand knowledge has two components: brand awareness, comprising recognition and recall, and brand image, the set of associations linked to the brand in memory. Aaker (1991) similarly identified awareness, perceived quality, associations and loyalty as the core assets of brand equity. Both frameworks share an underlying assumption: brand knowledge is built through exposure. Advertising, packaging, word of mouth, retail presence and direct experience all place the brand in front of the consumer, and the firm can influence most of these channels.

Hierarchy-of-effects models make the same assumption explicit. Consumers are thought to move from awareness to knowledge, liking, preference, conviction and purchase (Lavidge & Steiner, 1961), with each stage triggered by communication the consumer receives. Digital marketing extended rather than replaced this logic. Search advertising and search engine optimisation placed brands in front of consumers at the moment of intent, and online reviews became a powerful form of mediated word of mouth (Chevalier & Mayzlin, 2006; Dellarocas, 2003). In each case the consumer still encountered the brand, or content about the brand, directly.

Generative discovery weakens this assumption. When a model synthesises an answer, the consumer encounters the model's summary of the brand rather than the brand's own communication or a specific review. The associations conveyed in that summary are selected and phrased by the model. The firm does not control them and may not know what they are.

## Mental Availability and Consideration Sets

The mental availability perspective holds that brands grow primarily by being easy to think of in buying situations, across many category entry points (Romaniuk & Sharp, 2016; Sharp, 2010). Consideration set research similarly shows that brands which are not recalled at the moment of decision are rarely chosen, and that recall can be influenced without changing brand evaluations (Nedungadi, 1990; Shocker et al., 1991).

In a generative setting, the relevant question is not only whether the consumer recalls the brand but whether the model retrieves it. A consumer who asks for a recommendation outsources the first stage of consideration set formation. The model's answer becomes a proposed consideration set. If a brand is absent from that answer, it may never enter the consumer's evoked set, regardless of its mental availability among consumers who search in other ways. This makes the model's retrieval behaviour a new and largely unmeasured layer of brand availability.

## From Search Engines to Answer Engines

Search engines have long been recognised as gatekeepers of visibility whose ranking decisions carry commercial and social consequences (Introna & Nissenbaum, 2000). Their outputs, however, were lists of sources that users could inspect and compare. Generative systems combine retrieval with synthesis. In retrieval-augmented generation, a model retrieves relevant documents and conditions its generated answer on them (Lewis et al., 2020). Some platforms, such as Perplexity and Google AI Overviews, display citations to the retrieved sources. Others, such as ChatGPT in some modes, may answer from parametric knowledge learned during training, with or without live retrieval.

Two features of these systems complicate brand measurement. First, outputs are probabilistic. The same prompt can produce different brand lists and different descriptions on different runs. Second, models can generate fluent but inaccurate statements, a phenomenon widely documented as hallucination (Ji et al., 2023). A brand may therefore be visible but misrepresented, for example with the wrong price band, ingredients or features. Neither feature sits comfortably with the idea of generative visibility as a stable, single-number metric.

## Generative Engine Optimisation

Aggarwal et al. (2024) introduced generative engine optimisation as a framework for improving the visibility of content in generative engine responses. Using a benchmark of diverse queries, they tested content modifications and found that classical keyword-stuffing tactics had a negligible effect, while adding citations, quotations and statistics increased a source's visibility in generated answers. Their findings suggest that credibility signals and citable content matter more than traditional search optimisation techniques.

For marketers, this work prompts two questions. The first is which sources, rather than which pages, models rely on when recommending brands. A brand may be visible not because of its own website but because it is discussed on review platforms, in community forums, in business press or in encyclopaedic entries. The second is whether these source dependencies systematically favour certain kinds of brands. Brands with long histories, large press footprints and Wikipedia entries may enjoy a structural advantage over newer brands, even if the newer brands lead on marketplace ratings or sales.

## Generative AI in Marketing Scholarship

Marketing research on generative AI has grown quickly, but most of it looks at how firms and researchers use the technology. Hartmann et al. (2025) showed that AI-generated visual marketing content can match or exceed human-created content under specified conditions. Grewal et al. (2025) examined how generative AI is reshaping marketing strategy and implementation. Yoo et al. (2025) charted how generative AI can support consumer research. Hermann and Puntoni (2025) set out principles for ethical design and deployment. In all of these, generative AI is an instrument in the hands of marketers. Comparatively little work treats the model as an intermediary whose outputs determine brand visibility, and whose representations of brands deserve measurement as marketing outcomes.

## The Indian D2C Context

India is a useful setting for this question, for three reasons. First, its D2C sector includes many brands that have reached national scale within a few years, particularly in personal care and consumer audio, competing directly against established domestic and multinational incumbents [add source]. Second, Indian consumers' purchase journeys are heavily mediated by marketplaces such as Amazon, Flipkart and category platforms such as Nykaa, which generate large volumes of ratings and reviews that may serve as inputs to generative models. Third, research on generative engine optimisation and AI search has so far focused mainly on English-language, North American and European contexts, leaving emerging markets under-represented. Studying Indian brands therefore extends the evidence base and tests whether patterns observed elsewhere hold where brand histories, media ecosystems and source landscapes differ.

## Research Gap and Questions

Put together, this literature leaves marketing theory without a construct for brand equity that is formed through a model's representation rather than direct exposure, and without an agreed way to measure it. Evidence on how generative systems treat challenger brands in emerging markets is largely absent. We address four research questions:

- **RQ1.** How frequently and how prominently do Indian D2C brands appear in generative answers relative to incumbents?
- **RQ2.** How do models describe these brands, and how closely do those descriptions match the brands' stated positioning?
- **RQ3.** Which sources do the models rely on when recommending brands, and do source patterns differ between D2C brands and incumbents?
- **RQ4.** How stable are these visibility measures across platforms and across repeated runs of the same prompt?

# GENERATIVE BRAND EQUITY: A CONCEPTUAL FRAMEWORK

## Definition

This chapter defines **Generative Brand Equity** as the differential visibility and representation of a brand in the outputs of generative AI systems, relative to competing brands in the same category, in response to category-relevant consumer queries. The definition parallels Keller's (1993) consumer-based brand equity but relocates the site of brand knowledge. Instead of asking what consumers know about a brand, it asks what the model surfaces and says about the brand when consumers ask. It is a property of model outputs, not of consumer memory, and it is measured through systematic observation of those outputs.

## Dimensions

The framework comprises four dimensions, each adapted from an established brand equity component.

**Model awareness** corresponds to brand awareness. It captures whether, and how often, a brand is retrieved in response to category-level prompts that do not name it. A brand with high model awareness appears in a large share of relevant answers. This is the generative analogue of unaided recall.

**Model prominence** captures where the brand appears within an answer. Being named first, or being presented as the top recommendation, is likely to matter more than appearing as the fifth option. Prominence has no exact counterpart in classical brand equity but parallels the importance of top-of-mind awareness and of ranking position in search.

**Model image** corresponds to brand image. It captures the attributes, benefits, price and quality cues, and tone that a model attaches to a brand. Model image can be compared with the brand's own positioning to assess alignment. A brand may be visible but described in ways that conflict with its intended positioning, or with factual errors.

**Model credibility** captures the type and diversity of sources a model cites when recommending a brand. Drawing on the GEO literature (Aggarwal et al., 2024), it distinguishes brand-owned sources, marketplace listings, review and community content, editorial and business press, and encyclopaedic sources. A brand supported by diverse third-party sources may be more robustly visible than one supported mainly by its own website.

**Stability** is treated as a cross-cutting property of all four dimensions. Because generative outputs vary across runs and platforms, each dimension has both a level (how high it is on average) and a stability (how consistent it is). Two brands with the same average share of answers may differ sharply in how reliably they appear. Reporting stability is necessary for any defensible claim about generative visibility.

## Propositions

The framework yields four propositions to guide the empirical audit and future research.

- **P1.** Model awareness will differ systematically between D2C brands and incumbents, and these differences will not simply mirror the brands' marketplace performance.
- **P2.** Model image will diverge from brand positioning more often for brands with thinner third-party coverage.
- **P3.** Brands supported by a greater diversity of third-party source types will show higher model credibility and greater stability across platforms.
- **P4.** Visibility measures will vary meaningfully across platforms and repeated runs, such that single-run or single-platform audits misstate a brand's generative visibility.

The empirical study in this chapter measures model outputs. It does not measure consumer attitudes, consideration or purchase intention. The link between Generative Brand Equity and consumer outcomes is proposed conceptually, on the basis that model answers increasingly function as proposed consideration sets, and is identified as a priority for future research.

# METHOD

## Research Design

The study uses a structured prompt-based audit, an approach adapted from algorithm audit research that examines platform behaviour by systematically querying a system and analysing its outputs (Sandvig et al., 2014). The design is observational and descriptive-comparative. It is intended to be replicable by other researchers and adaptable to other categories and markets.

## Categories and Brands

Two product categories are selected in which Indian D2C brands compete directly with established incumbents and in which consumers commonly seek recommendations: personal skincare (with a focus on face serums and moisturisers) and consumer audio (with a focus on wireless earbuds). In each category, five to six brands are selected to include both Indian D2C brands and established domestic or global incumbents. Selection criteria are national availability, presence on major Indian marketplaces, and a clear stated positioning that can be compared with model descriptions. [Insert final brand list and selection rationale.]

## Prompt Design

A set of approximately 30 prompts per category is developed to reflect realistic Indian shopper queries. Prompts are grouped into four types:

- **Generic category prompts**, for example, "What are the best face serums available in India?"
- **Use-case prompts**, for example, "Which serum is good for oily, acne-prone skin?"
- **Price-band prompts**, for example, "Best wireless earbuds under Rs. 2,000 in India."
- **Comparison prompts**, for example, "Is [Brand A] better than [Brand B] for sensitive skin?"

Generic, use-case and price-band prompts do not name any brand and are used to measure model awareness and prominence. Comparison prompts name brands and are used mainly to assess model image. Prompts are written in English and reviewed by the authors for realism and neutrality. [Insert final prompt list as an appendix.]

## Platforms and Data Collection

Each prompt is submitted to four platforms: ChatGPT, Gemini, Perplexity and Google AI Overviews. Each prompt is run five times on each platform, using a fresh session, without logged-in personalisation where possible, and with location set to India. This yields approximately 30 prompts x 2 categories x 4 platforms x 5 runs, or about 1,200 responses. For every response, the platform, interface, model version where displayed, date, time and full text, including any cited links, are recorded. Data collection is completed within a fixed window of [insert dates] to limit the effect of platform updates. Google AI Overviews do not appear for every query; where no overview is shown, this is recorded as a non-response rather than as zero visibility.

## Coding Scheme

Each response is coded at the brand-mention level for:

- **Mention:** whether each brand in the study set appears, and any other brands named.
- **Position:** the order in which each brand is mentioned, and whether it is presented as a top or primary recommendation.
- **Attributes:** the benefits, features, ingredients, price cues and target users attributed to the brand.
- **Sentiment:** whether the description is positive, neutral, mixed or negative.
- **Accuracy:** whether factual claims (price band, key ingredients or features) are correct when checked against the brand's official information.
- **Citations:** the domains cited, classified as brand-owned, marketplace, review or community, editorial or business press, or encyclopaedic.

## Measures

The coded data are used to compute the following measures for each brand, platform and category:

- **Mention rate:** the share of non-branded responses in which the brand appears.
- **Share-of-model:** the brand's mentions as a share of all study-set brand mentions in the category.
- **First-mention rate:** the share of responses in which the brand is named first.
- **Average position:** the mean order of mention when the brand appears.
- **Positioning alignment:** the share of coded attributes that match the brand's stated positioning.
- **Accuracy rate:** the share of checkable factual claims about the brand that are correct.
- **Citation mix:** the distribution of cited source types supporting the brand.
- **Stability:** the mean pairwise Jaccard similarity of the set of brands recommended across the five runs of the same prompt on the same platform, and the variation in mention rate across platforms.

## Benchmarks

To assess whether generative visibility reflects market presence, model measures are compared with observable benchmarks: marketplace ratings and review counts on Amazon India and Flipkart (and Nykaa for skincare), and, where publicly available, reported revenue or market share. Where benchmarks and model visibility diverge, the case is examined in detail to identify possible explanations in the citation data.

## Reliability

Two authors independently code a random subsample of 20 percent of responses. Inter-coder reliability is assessed using Cohen's kappa (Cohen, 1960) for categorical codes, interpreted using conventional thresholds (Landis & Koch, 1977), and disagreements are resolved through discussion before the remaining responses are coded. The coding manual is refined after the subsample and documented for replication (Krippendorff, 2004).

## Ethical Considerations

The study uses publicly accessible AI systems and does not involve human participants or personal data. Platform terms of use are respected, and no automated scraping is used beyond what the platforms permit. Brand names are reported because the analysis concerns public brand representation, but findings are framed as descriptions of model outputs during a specified window, not as judgements of brand quality.

# FINDINGS

[This section will be completed once the audit is run. The structure below shows the planned analyses and tables.]

## Model Awareness and Prominence (RQ1)

[Report mention rate, share-of-model, first-mention rate and average position for each brand by platform and category. Compare D2C brands with incumbents.]

@TABLE1

## Model Image and Accuracy (RQ2)

[Summarise the most frequent attributes attached to each brand, positioning alignment and accuracy rate. Include short illustrative excerpts from model answers.]

## Sources Behind Recommendations (RQ3)

[Report the citation mix for each brand and platform. Compare the reliance of D2C brands and incumbents on brand-owned, marketplace, review and community, editorial and encyclopaedic sources.]

@TABLE2

## Stability Across Runs and Platforms (RQ4)

[Report Jaccard stability by platform and prompt type, and the spread in mention rate across platforms for each brand.]

## Comparison with Market Benchmarks

[Compare model visibility with marketplace ratings, review counts and available market share data. Identify brands that are over- or under-represented and examine the citation patterns behind those cases.]

# SOLUTIONS AND RECOMMENDATIONS

The recommendations below draw on the framework and on existing GEO evidence. They will be refined and prioritised in light of the audit findings. [Revise after results.]

**Audit generative visibility as a routine brand metric.** Brand managers already track search rank, share of voice and marketplace ratings. Generative visibility should be added to this dashboard. A lightweight version of the protocol in this chapter, with a fixed prompt set run monthly across major platforms, can show whether a brand is being retrieved, how it is described and how this changes over time. Because outputs vary, audits should always use repeated runs and report ranges rather than single values.

**Invest in citable third-party presence, not only owned content.** The GEO evidence suggests that credibility signals and citable content increase visibility in generative answers (Aggarwal et al., 2024). For D2C brands, this means building a footprint in sources that models draw on: substantive coverage in business and category press, detailed and authentic marketplace reviews, accurate entries in reference sources where notability allows, and presence in community discussions. Owned content remains useful but may carry less weight than independent sources.

**Make product facts easy to retrieve and hard to misstate.** Inaccurate model descriptions, such as a wrong price band or ingredient, can damage a brand even when it is visible. Brands can reduce this risk by publishing clear, consistent and structured product information across their own site and marketplace listings, so that the same facts appear wherever a model retrieves them.

**Align positioning across the sources models read.** If a brand positions itself as dermatologist-formulated and affordable, but reviews and press emphasise packaging or influencer campaigns, the model's description may follow the third-party narrative. Monitoring model image against intended positioning can reveal where brand messaging is not reaching the sources that shape generative answers.

**Treat platform differences as strategic information.** A brand that is highly visible on one platform but absent on another may be benefiting from a specific source the first platform relies on. Platform-level citation analysis can point to where visibility efforts will have the largest effect.

# GOVERNANCE AND MARKET STRUCTURE IMPLICATIONS

The issues here go beyond individual brand strategy. If models systematically favour brands with long histories and extensive press coverage, they may raise barriers to entry for new and small brands, concentrating visibility among incumbents. That would undercut one of the main promises of digital commerce: cheaper access to consumers for challenger brands.

Transparency is a second concern. Consumers who receive a synthesised recommendation may not know which sources informed it, whether any commercial relationships influenced it, or how stable it is. Regulatory frameworks are beginning to address related issues. The European Union's Digital Services Act sets transparency obligations for recommender systems on large platforms (Regulation (EU) 2022/2065), and the EU Artificial Intelligence Act introduces transparency requirements for certain AI systems (Regulation (EU) 2024/1689). In India, the Consumer Protection (E-Commerce) Rules, 2020 address disclosure obligations for e-commerce entities. How such frameworks apply to brand recommendations generated by AI assistants is not yet settled. Systematic audits of the kind proposed here can provide the evidence base that regulators and researchers need to assess whether generative recommendations are fair, accurate and transparent.

# FUTURE RESEARCH DIRECTIONS

We see five directions for further work. First, the link between Generative Brand Equity and consumer outcomes needs direct testing. Experimental studies could expose consumers to model answers that vary in brand presence, prominence and description, and measure consideration, brand attitude and purchase intention. Second, the audit could be extended across languages. In India, many consumers search in Hindi, Hinglish and other regional languages, and it is unknown whether models recommend the same brands across languages. Third, longitudinal audits could track how generative visibility changes as platforms update their models and retrieval systems, and whether early visibility advantages persist. Fourth, experimental interventions, such as publishing new third-party content about a brand and observing changes in model outputs, could test the causal mechanisms suggested by the GEO literature in a marketing context. Fifth, the framework could be applied to other high-consideration categories, such as higher education, financial products and healthcare services, and to agentic commerce, where AI assistants not only recommend but also purchase on the consumer's behalf.

# LIMITATIONS

The study has several limitations. Generative platforms change frequently, so findings describe model behaviour during a specific data collection window and may not hold later. The study covers two categories and a limited number of brands, which restricts generalisation. Prompts are in English and may not reflect the full range of Indian consumer queries. Personalisation and location effects cannot be fully controlled on all platforms. Market benchmarks such as marketplace ratings are imperfect proxies for market presence, and reliable market share data for private D2C brands are limited. Finally, the study measures model outputs and does not establish how consumers respond to them.

# CONCLUSION

Brand discovery is moving from ranked links to synthesised answers. In this environment, a brand's visibility and image are increasingly formed by what a generative model retrieves and says about it, before any direct consumer exposure. This chapter has proposed Generative Brand Equity as a way to conceptualise that shift, built on model awareness, model prominence, model image and model credibility, with stability as a cross-cutting property. It has set out a replicable audit protocol and applied it to Indian D2C brands and incumbents across four generative platforms. [Add one to two sentences summarising the key findings.] The practical message for marketers is that brand building now extends to the sources models read, and to making brand facts easy to retrieve accurately. The chapter also gives researchers a working vocabulary and a measurement protocol they can reuse, and gives policymakers a way to check whether generative discovery is widening the gap between established and challenger brands.

# REFERENCES

@REF Aaker, D. A. (1991). Managing brand equity: Capitalizing on the value of a brand name. Free Press.
@REF Aggarwal, P., Murahari, V., Rajpurohit, T., Kalyan, A., Narasimhan, K., & Deshpande, A. (2024). GEO: Generative engine optimization. In Proceedings of the 30th ACM SIGKDD Conference on Knowledge Discovery and Data Mining (pp. 5–16). Association for Computing Machinery. https://doi.org/10.1145/3637528.3671900
@REF Chevalier, J. A., & Mayzlin, D. (2006). The effect of word of mouth on sales: Online book reviews. Journal of Marketing Research, 43(3), 345–354.
@REF Cohen, J. (1960). A coefficient of agreement for nominal scales. Educational and Psychological Measurement, 20(1), 37–46.
@REF Dellarocas, C. (2003). The digitization of word of mouth: Promise and challenges of online feedback mechanisms. Management Science, 49(10), 1407–1424.
@REF European Union. (2022). Regulation (EU) 2022/2065 of the European Parliament and of the Council on a Single Market for Digital Services (Digital Services Act). Official Journal of the European Union.
@REF European Union. (2024). Regulation (EU) 2024/1689 of the European Parliament and of the Council laying down harmonised rules on artificial intelligence (Artificial Intelligence Act). Official Journal of the European Union.
@REF Government of India. (2020). Consumer Protection (E-Commerce) Rules, 2020. Ministry of Consumer Affairs, Food and Public Distribution.
@REF Grewal, D., Satornino, C. B., Davenport, T., & Guha, A. (2025). How generative AI is shaping the future of marketing. Journal of the Academy of Marketing Science, 53(3), 702–722. https://doi.org/10.1007/s11747-024-01064-3
@REF Hartmann, J., Exner, Y., & Domdey, S. (2025). The power of generative marketing: Can generative AI create superhuman visual marketing content? International Journal of Research in Marketing, 42(1), 13–31. https://doi.org/10.1016/j.ijresmar.2024.09.002
@REF Hermann, E., & Puntoni, S. (2025). Generative AI in marketing and principles for ethical design and deployment. Journal of Public Policy & Marketing, 44(3), 332–349. https://doi.org/10.1177/07439156241309874
@REF Introna, L. D., & Nissenbaum, H. (2000). Shaping the web: Why the politics of search engines matters. The Information Society, 16(3), 169–185.
@REF Ji, Z., Lee, N., Frieske, R., Yu, T., Su, D., Xu, Y., Ishii, E., Bang, Y. J., Madotto, A., & Fung, P. (2023). Survey of hallucination in natural language generation. ACM Computing Surveys, 55(12), Article 248.
@REF Keller, K. L. (1993). Conceptualizing, measuring, and managing customer-based brand equity. Journal of Marketing, 57(1), 1–22.
@REF Krippendorff, K. (2004). Content analysis: An introduction to its methodology (2nd ed.). Sage.
@REF Landis, J. R., & Koch, G. G. (1977). The measurement of observer agreement for categorical data. Biometrics, 33(1), 159–174.
@REF Lavidge, R. J., & Steiner, G. A. (1961). A model for predictive measurements of advertising effectiveness. Journal of Marketing, 25(6), 59–62.
@REF Lewis, P., Perez, E., Piktus, A., Petroni, F., Karpukhin, V., Goyal, N., Küttler, H., Lewis, M., Yih, W., Rocktäschel, T., Riedel, S., & Kiela, D. (2020). Retrieval-augmented generation for knowledge-intensive NLP tasks. Advances in Neural Information Processing Systems, 33, 9459–9474.
@REF Nedungadi, P. (1990). Recall and consumer consideration sets: Influencing choice without altering brand evaluations. Journal of Consumer Research, 17(3), 263–276.
@REF Romaniuk, J., & Sharp, B. (2016). How brands grow: Part 2. Oxford University Press.
@REF Sandvig, C., Hamilton, K., Karahalios, K., & Langbort, C. (2014). Auditing algorithms: Research methods for detecting discrimination on internet platforms. Paper presented at Data and Discrimination: Converting Critical Concerns into Productive Inquiry, a preconference of the 64th Annual Meeting of the International Communication Association, Seattle, WA.
@REF Sharp, B. (2010). How brands grow: What marketers don't know. Oxford University Press.
@REF Shocker, A. D., Ben-Akiva, M., Boccara, B., & Nedungadi, P. (1991). Consideration set influences on consumer decision-making and choice: Issues, models, and suggestions. Marketing Letters, 2(3), 181–197.
@REF Yoo, K., Haenlein, M., & Hewett, K. (2025). A whole new world, a new fantastic point of view: Charting unexplored territories in consumer research with generative artificial intelligence. Journal of the Academy of Marketing Science, 53(3), 723–759.

# KEY TERMS AND DEFINITIONS

**Generative Brand Equity:** The differential visibility and representation of a brand in the outputs of generative AI systems, relative to competing brands, in response to category-relevant consumer queries.

**Generative Engine Optimisation (GEO):** Practices intended to increase the likelihood that content is retrieved, cited or reflected in answers produced by generative AI systems.

**Share-of-Model:** A brand's mentions as a proportion of all brand mentions in a category across a defined set of generative AI responses.

**Model Image:** The set of attributes, benefits, price and quality cues, and tone that a generative AI system attaches to a brand in its answers.

**Prompt-Based Audit:** A research method in which a fixed set of prompts is submitted repeatedly to one or more generative AI systems and the outputs are systematically coded and analysed.

**Retrieval-Augmented Generation (RAG):** An approach in which a language model retrieves relevant documents from an external source and conditions its generated answer on them.

**Direct-to-Consumer (D2C) Brand:** A brand that sells primarily through its own digital channels and online marketplaces rather than through traditional distribution and mass-media advertising.

**Stability:** The consistency of a visibility measure across repeated runs of the same prompt and across different generative platforms.
