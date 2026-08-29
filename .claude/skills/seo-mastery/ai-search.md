---
last_verified: 2026-08-29
---

# AI Search Reference (AI Overviews / AI Mode / AI Crawlers)

How to optimize for and control generative AI search experiences: Google's AI Overviews and AI Mode, plus third-party AI crawlers (OpenAI, Anthropic, Perplexity, etc.). Based on Google's AI features guide, the generative AI optimization guide published 2026-05-15, and the official crawler documentation.

## Google's Official Guidance (AI Overviews / AI Mode)

Sources: [AI features and your website](https://developers.google.com/search/docs/appearance/ai-features) and [Optimizing your website for generative AI features](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide)

Key points, verified against the official guides:

- **Three eligibility gates.** A page must be **indexable**, **eligible for snippets**, and its site must be **included in Search generative AI features in Search Console**. Google states it directly: "In addition to the technical requirements for Search, a site must be included in Search generative AI features in Search Console to be eligible for display in generative AI features on Google Search."
- **No special markup or files.** "You don't need to create new machine readable files, AI text files, markup, or Markdown to appear in Google Search (including its generative AI capabilities), as Google Search itself doesn't use them." This covers **llms.txt** (see below), content chunking ("There's no requirement to break your content into tiny pieces"), AI-specific writing style, and AI-specific schema ("Structured data isn't required for generative AI search").
- **Standard SEO is the optimization.** Generative AI features are "rooted in core Search ranking and quality systems." Content that ranks well and answers questions clearly is what AI features cite. There is no separate "AI ranking" to optimize for.
- **Appearance is controlled with the Search Console control plus existing snippet controls**, not new directives (see the next two sections).
- **Traffic is reported in Search Console** under the "Web" search type — clicks from AI Overviews / AI Mode count as ordinary clicks there. Since 2026-06-03 there is also a dedicated **Search generative AI performance report** (see the measurement section for its limits).

### The Search Console Generative AI Control

Rolled out from **2026-06-03**, initially "to a subset of website owners in the UK, allowing for thorough testing before rolling them out to website owners globally." This is the only way to opt out of AI features without also damaging your regular search snippets. Check whether your property has the setting rather than assuming availability.

Location: **Settings → Search generative AI**. Three options:

| Option | Effect |
|--------|--------|
| Include my site's links and content in Search generative AI features | **Default.** Content may appear as links and ground AI responses; the site can receive impressions and traffic from these features |
| Exclude my site's links and content from Search generative AI features | Content is not shown in, linked from, or used to ground AI Overviews, AI Mode, or generative AI features in Discover |
| Inherit control from parent | Follows the parent property's setting |

What it does **not** do: Google states the control "isn't used as a ranking or inclusion signal affecting other parts of Search." Normal Search results and the Discover feed are unaffected.

Timing is not instant, and the help page is careful about it: exclusion "generally takes a few days"; content is excluded "within 1-2 days after the control goes live, but some content may take longer to be excluded due to caching and propagation across Google systems." Do not treat the toggle as a takedown mechanism.

Choosing between this and `nosnippet`:

- **Search Console control** — removes AI feature appearance only. Regular snippets, and therefore regular CTR, are untouched. Prefer this when the goal is "stop AI from using my content."
- **`nosnippet` / `max-snippet`** — removes or shortens *all* snippets, including regular search results. Use only when you also want the regular snippet suppressed.

### Controlling Appearance in AI Features

Use the same controls that govern snippets and indexing:

```html
<!-- Exclude the page from Search entirely (also removes it from AI features) -->
<meta name="robots" content="noindex">

<!-- Keep the page indexed but show no snippet (also prevents AI Overviews/AI Mode from using its content) -->
<meta name="robots" content="nosnippet">

<!-- Limit snippet length (also limits what AI features can quote) -->
<meta name="robots" content="max-snippet:160">
```

```html
<!-- Exclude only part of a page from snippets and AI features.
     data-nosnippet is only supported on span, div, and section elements —
     on other elements (e.g. <p>) it is ignored. -->
<p><span data-nosnippet>This text will not appear in snippets or AI Overviews.</span></p>
```

Trade-off: `nosnippet` / aggressive `max-snippet` values also remove or shorten your regular search snippets, which typically lowers CTR. Use them only for content you genuinely do not want quoted — if the goal is AI-only exclusion, use the Search Console control above instead.

## AI Crawler Control (robots.txt)

### Google-Extended — Exact Scope

Source: [Google's common crawlers](https://developers.google.com/search/docs/crawling-indexing/google-common-crawlers)

`Google-Extended` is a **product token**, not a separate crawler. It controls one thing only: whether your content may be used for **training and grounding Gemini-generation models**.

- Blocking `Google-Extended` does **not** remove you from Google Search.
- Blocking `Google-Extended` does **not** remove you from AI Overviews or AI Mode (those are Search features, governed by indexing and snippet controls).
- `Google-Extended` is **not a ranking signal**.

```txt
# Opt out of Gemini training/grounding only — Search and AI Overviews are unaffected
User-agent: Google-Extended
Disallow: /
```

### Major AI Crawler User Agents

| User agent | Operator | Purpose | Effect of blocking |
|------------|----------|---------|--------------------|
| `Google-Extended` | Google | Gemini training/grounding opt-out token | No effect on Search / AI Overviews |
| `GPTBot` | OpenAI | Model training | Content excluded from future training |
| `OAI-SearchBot` | OpenAI | ChatGPT search index | Site not cited in ChatGPT search |
| `ChatGPT-User` | OpenAI | User-initiated fetches from ChatGPT | Limited — OpenAI states robots.txt rules "may not apply" to user-initiated fetches |
| `ClaudeBot` | Anthropic | Model training | Content excluded from future training |
| `Claude-SearchBot` | Anthropic | Claude search index | Site not cited in Claude search |
| `Claude-User` | Anthropic | User-initiated fetches from Claude | Claude cannot open your pages for users |
| `PerplexityBot` | Perplexity | Search index | Site not cited in Perplexity answers |
| `Perplexity-User` | Perplexity | User-initiated fetches | None in practice — Perplexity documents that this fetcher generally ignores robots.txt |
| `Applebot-Extended` | Apple | Model training opt-out token | Content excluded from Apple model training |
| `CCBot` | Common Crawl | Open web corpus (used by many trainers) | Excluded from Common Crawl datasets |
| `Meta-ExternalAgent` | Meta | Model training / indexing | Content excluded from Meta training |
| `Bytespider` | ByteDance | Model training | Content excluded from ByteDance training |

Verify current UA strings against each operator's official documentation before relying on them — names and scopes change. Note that robots.txt is voluntary: well-known operators respect it, but it is not an access control.

### Trade-off: Blocking Training vs. Being Cited in AI Search

Decide separately for two different questions:

1. **"May my content train future models?"** → training crawlers (`GPTBot`, `ClaudeBot`, `Google-Extended`, `Applebot-Extended`, `CCBot`, ...). Blocking these has no effect on today's visibility.
2. **"May AI search products cite and link to me?"** → search/fetch crawlers (`OAI-SearchBot`, `Claude-SearchBot`, `PerplexityBot`, user-initiated fetchers). Blocking these removes you from AI answers **and the referral traffic they send**.

```txt
# Recipe A: opt out of training, stay citable in AI search (common choice for media/blogs)
User-agent: GPTBot
Disallow: /

User-agent: ClaudeBot
Disallow: /

User-agent: Google-Extended
Disallow: /

User-agent: Applebot-Extended
Disallow: /

User-agent: CCBot
Disallow: /

User-agent: Meta-ExternalAgent
Disallow: /

User-agent: Bytespider
Disallow: /
```

```txt
# Recipe B: block all AI access (training AND AI search citations — expect near-zero AI referrals;
# note: user-initiated fetchers such as Perplexity-User and ChatGPT-User may ignore robots.txt)
User-agent: GPTBot
Disallow: /

User-agent: OAI-SearchBot
Disallow: /

User-agent: ChatGPT-User
Disallow: /

User-agent: ClaudeBot
Disallow: /

User-agent: Claude-SearchBot
Disallow: /

User-agent: Claude-User
Disallow: /

User-agent: PerplexityBot
Disallow: /

User-agent: Perplexity-User
Disallow: /

User-agent: Google-Extended
Disallow: /

User-agent: Applebot-Extended
Disallow: /

User-agent: CCBot
Disallow: /

User-agent: Meta-ExternalAgent
Disallow: /

User-agent: Bytespider
Disallow: /
```

## llms.txt

`llms.txt` is a community proposal (a Markdown index of your site placed at `/llms.txt`) intended to help LLMs find your key content.

- **Google does not use it.** The generative AI optimization guide is explicit: no "AI text files" are needed, "as Google Search itself doesn't use them." Do not expect any Google effect from adding it.
- Adoption by other AI vendors is limited and unconfirmed — treat it as optional, low-cost, low-evidence.
- If you choose to publish one for other consumers, the proposed format is:

```txt
# Site Name

> One-line description of the site.

## Main content

- [Page title](https://example.com/page): one-line description
- [Another page](https://example.com/other): one-line description

## Optional

- [Less important page](https://example.com/misc): one-line description
```

## Designing Content That AI Search Cites

AI answers favor content that is easy to extract and attribute. The levers are the same as strong editorial SEO:

- **Conclusion first.** State the answer in the first paragraph, then elaborate. Direct answers to specific questions are easiest to quote.
- **Clear, factual statements.** Concrete numbers, dates, definitions, and steps — not vague marketing prose.
- **Original data and first-hand experience.** Surveys, benchmarks, case studies, and lived experience (the E-E-A-T "Experience") are what AI summaries must cite rather than paraphrase away.
- **Structured headings.** One question or subtopic per H2/H3 so a passage can stand alone; keep question-form headings close to their answers.
- **Attribution-ready pages.** Clear authorship, dates, and sources (E-E-A-T) make your page a safer citation for AI features.

Checklist:

- [ ] The main answer appears within the first ~100 words
- [ ] Each H2/H3 covers exactly one question or subtopic
- [ ] Key facts are stated as extractable sentences (number + unit + date)
- [ ] The page contains something no other page has (data, experience, examples)
- [ ] Author, date, and sources are visible on the page

## Measuring AI Search Traffic

### Search Console

- AI Overviews / AI Mode impressions and clicks are included in the **"Web" search type** of the Performance report (AI Mode included since June 2025).
- The dedicated **Search generative AI performance report** (launched 2026-06-03, with a Discover counterpart) breaks impressions down by page, country, device and date across AI Overviews, AI Mode and generative AI in Discover. Two limits to plan around: the report has **no historical backfill** — it starts shortly before launch, so there is no year-over-year comparison — and it carries **impressions only, no clicks**. (Secondary reports put the first day of data at 2026-05-18; Google's own documentation does not state a date, so treat the exact start as unverified and read it off your own property.)
- Because clicks are missing from the dedicated report, attribution still depends on the "Web" type. Watch for the pattern "impressions stable, clicks down" on informational queries — a common signature of AI Overviews absorbing clicks.

### Analytics (Referral Segmentation)

AI assistant referrals arrive as ordinary referral traffic. Segment them by referrer domain:

```txt
chatgpt.com
perplexity.ai
gemini.google.com
copilot.microsoft.com
claude.ai
```

Example (GA4): create a custom channel group or an exploration filter with a regex condition on "Session source":

```txt
chatgpt\.com|perplexity\.ai|gemini\.google\.com|copilot\.microsoft\.com|claude\.ai
```

Note: some AI surfaces send no referrer, so measured AI traffic is a lower bound.

## Official Resources

- [AI features and your website](https://developers.google.com/search/docs/appearance/ai-features)
- [Optimizing your website for generative AI features on Google Search](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide)
- [Search generative AI control (Search Console Help)](https://support.google.com/webmasters/answer/16908024)
- [Introducing Search Generative AI performance reports](https://developers.google.com/search/blog/2026/06/gen-ai-performance-reports)
- [Google's common crawlers (Google-Extended)](https://developers.google.com/search/docs/crawling-indexing/google-common-crawlers)
- [Snippet controls (meta tags)](https://developers.google.com/search/docs/appearance/snippet)
- [OpenAI crawlers](https://platform.openai.com/docs/bots)
- [Anthropic crawlers](https://support.claude.com/en/articles/8896518-does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-the-crawler)
- [Perplexity crawlers](https://docs.perplexity.ai/guides/bots)
