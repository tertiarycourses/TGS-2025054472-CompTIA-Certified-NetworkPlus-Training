"""Concept-enrichment slides imported from the reference deck
"Architecting Brand Trust — Aligning Strategy, Emotion, and Agentic AI"
(courseware/PPT References/Architecting_Brand_Trust (2).pptx).

Each Learning Unit gets a set of insight slides rendered AFTER its
Key Concepts slide. Content was transcribed from the reference deck and
redrawn in the Tertiary house white theme; three diagram-heavy visuals
are imported directly (assets/brandtrust/*.png, watermark removed).

Slide spec kinds understood by build_slides.py:
  pillars   -> tile_grid of (title, desc) tuples
  table     -> two-column comparison table with coloured headers
  stats     -> big-number stat tiles + optional callout band
  image     -> full-width imported visual with house header
  quote     -> big statement slide
  flow      -> horizontal chevron flow (optional note band)
  playbook  -> numbered 01..04 columns + tagline band
  twocol    -> two-column comparison panels
"""

BRAND_TRUST = {

# ---------------------------------------------------------------- LU1
1: [
    ("pillars", dict(
        title="The Modern Brand Ecosystem",
        kicker="LU1 · THE BIG PICTURE",
        intro="Four forces now shape how customers trust and choose brands.",
        items=[
            ("The Shift — Philosophy",
             "Moving from product-centric innovation to a customer-back business "
             "model (CBM) to drive sustainable growth."),
            ("The Mechanics — System",
             "Abandoning the linear funnel for a non-linear, infinitely looping "
             "customer journey."),
            ("The Core — Emotion",
             "Engineering authenticity and shared values as the primary engines "
             "of brand loyalty and trust."),
            ("The Scale — AI",
             "Governing the new frontier where agentic AI acts autonomously on "
             "behalf of the brand."),
        ])),
    ("table", dict(
        title="The Strategic Paradigm Shift",
        kicker="LU1 · PRODUCT vs CUSTOMER",
        intro="Customer-centric organisations think, innovate and measure differently.",
        colheads=("Product-Centric", "Customer-Centric"),
        rows=[
            ("Core philosophy", "“If we build it, they will come”",
             "“Obsession with customer pain points and delight”"),
            ("Innovation style", "High-risk, creates new markets, heavy R&D",
             "Incremental, read-and-react, user research-driven"),
            ("Risk profile", "High tolerance for failure and pivots",
             "Lower risk, focused on continuous feedback loops"),
            ("Success metric", "One-time, big-ticket sales",
             "Lifetime value, reduced churn, Net Promoter Scores"),
        ])),
    ("stats", dict(
        title="The Economics of Customer Obsession",
        kicker="LU1 · WHY IT PAYS",
        intro="Firms implementing a customer-experience (CX) approach routinely "
              "outperform product-led peers.",
        stats=[("+49%", "Faster profit growth"),
               ("+41%", "Higher revenue expansion"),
               ("+51%", "Stronger customer retention")],
        note="73% of customers now expect companies to treat them as individuals, "
             "not numbers — up from just 39% in 2023.")),
],

# ---------------------------------------------------------------- LU2
2: [
    ("table", dict(
        title="The Marketing Funnel vs the Customer Journey",
        kicker="LU2 · TWO MENTAL MODELS",
        intro="The funnel explains where customers drop off; the journey explains why.",
        colheads=("Marketing Funnel — business-centric", "Customer Journey — customer-centric"),
        rows=[
            ("Shape", "Linear, top-down: Awareness → Interest → Consideration → "
             "Intent → Evaluation → Purchase",
             "An infinite loop: Discovery → Research → Purchase → Experience → "
             "Retention → Advocacy"),
            ("Progression", "Ends at conversion — the sale is the finish line",
             "Non-linear, interconnected moments that continue after purchase"),
            ("What it tracks", "Drop-offs and acquisition costs",
             "Retention, advocacy, satisfaction and long-term value"),
            ("Blind spot", "Explains where customers drop off, not why",
             "Requires richer behavioural data to map honestly"),
        ])),
    ("image", dict(
        title="Mapping the 5-Stage Journey Loop",
        kicker="LU2 · THE JOURNEY LOOP",
        path="brandtrust/bt-journey-loop.png",
        intro="Awareness → Consideration → Decision → Retention → Advocacy — and "
              "advocacy feeds awareness again.")),
    ("stats", dict(
        title="The Engine of Loyalty: Emotional Branding",
        kicker="LU2 · EMOTION DRIVES PERCEPTION",
        intro="Affect-driven purchasing decisions outpace purely rational choices.",
        stats=[("45.2%", "say an emotional connection with a brand is very important"),
               ("42%", "associate their favourite brands with trust & reliability"),
               ("88.1%", "actively choose branded products over non-branded alternatives")],
        note="55% of loyalty is driven by quality — but 32% is driven entirely by "
             "customer service and emotional support.")),
],

# ---------------------------------------------------------------- LU3
3: [
    ("pillars", dict(
        title="The Anatomy of Brand Authenticity",
        kicker="LU3 · AUTHENTICITY",
        intro="Authenticity is engineered through four repeatable practices.",
        items=[
            ("Radical Transparency",
             "Open communication about business practices and product origins — "
             "e.g. Patagonia's Footprint Chronicles detailing supply-chain realities."),
            ("Value Alignment",
             "Emotional connection forged through shared beliefs and societal "
             "commitment — e.g. Ben & Jerry's integration of social justice into "
             "core operations."),
            ("Authentic Storytelling",
             "Humanising the brand through relatable, non-fabricated narratives — "
             "e.g. Nike highlighting genuine struggles and triumphs of real athletes."),
            ("Quality Assurance",
             "Trust earned through unwavering consistency and reliability — "
             "e.g. Toyota's rigorous quality control building global dependability."),
        ])),
    ("twocol", dict(
        title="The Trust Fracture: the Say-Do Gap",
        kicker="LU3 · WHAT BREAKS TRUST",
        lhead="How trust fractures",
        rhead="Case: the Volkswagen emissions scandal",
        left=[
            "Brand authenticity is destroyed by inauthentic practices — when a "
            "company's actions contradict its stated promises.",
            "Discrepancies between marketing claims and operational reality create "
            "a trust fracture that severs the customer journey loop permanently.",
            "PR campaigns can only amplify what operations can prove.",
        ],
        right=[
            "Software was installed to cheat emissions tests.",
            "The deception directly contradicted public claims of environmental "
            "responsibility.",
            "Result: immediate, catastrophic loss of consumer trust — a say-do "
            "gap no campaign could repair.",
        ])),
],

# ---------------------------------------------------------------- LU4
4: [
    ("quote", dict(
        line1="“The agent is becoming the brand.”",
        line2="Nine in ten US marketing agencies now use generative AI, and half use "
              "agentic AI for execution. AI is no longer just generating content — it "
              "is deciding, spending, personalising and interacting directly with "
              "customers.",
        kicker="LU4 · THE NEXT FRONTIER: AGENTIC AI")),
    ("flow", dict(
        title="The Risk Vector: Authority Concentration",
        kicker="LU4 · AI BRAND RISK",
        color="VIOLET",
        steps=[
            "Content agent — permission to draft copy + access the CMS",
            "Media agent — permission to optimise spend + finance workflows",
            "Personalisation engine — tailors experiences + sensitive data",
            "Concentration node — combined permissions create high risk",
        ],
        note="In an agentic enterprise, risk moves through authority pathways, not "
             "people. Human approvals cannot scale at machine speed to monitor "
             "these intersections.")),
    ("flow", dict(
        title="The Brand Authority Model",
        kicker="LU4 · GOVERNANCE",
        color="BLUE",
        steps=[
            "Identity — which human and non-human identities can act on behalf of the brand?",
            "Access — what systems, data and workflows are they permitted to touch?",
            "Inheritance — what authority do they hold after delegation and integrations?",
            "Concentration — where does authority unintentionally combine into high risk?",
            "Revocation — how quickly can authority be severed if boundaries are breached?",
        ],
        note="Enterprise Authority Assurance replaces the editorial calendar.")),
    ("image", dict(
        title="The Architecture of Modern Brand Trust",
        kicker="LU4 · PUTTING IT TOGETHER",
        path="brandtrust/bt-architecture.png",
        intro="The customer at the centre — anchored by emotion, navigated through "
              "journey mapping, scaled safely within strict AI authority boundaries.")),
    ("playbook", dict(
        title="The Executive Playbook",
        kicker="LU4 · FROM INSIGHT TO ACTION",
        items=[
            ("Shift the Metric",
             "Move away from pure acquisition costs. Restructure KPIs around "
             "lifetime value, Net Promoter Scores and journey retention."),
            ("Map the Reality, Not the Theory",
             "Audit the 5-stage customer journey loop using actual behavioural "
             "data, not internal corporate assumptions. Find the friction."),
            ("Close the Say-Do Gap",
             "Audit your brand's authenticity. Ensure marketing claims — "
             "environmental, social, quality — are rigidly matched by operational "
             "reality."),
            ("Build the Authority Model",
             "Stop relying on human bottlenecks for AI approval. Map identity, "
             "access and authority concentration for every agentic system touching "
             "your brand."),
        ],
        tagline="Trust cannot be retrofitted. It must be engineered.")),
],
}
