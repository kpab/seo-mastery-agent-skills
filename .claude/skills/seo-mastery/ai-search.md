# AI Search Reference (AI Overviews / AI Mode / AI Crawlers)

How to optimize for and control generative AI search experiences: Google's AI Overviews and AI Mode, plus third-party AI crawlers (OpenAI, Anthropic, Perplexity, etc.). Based on Google's official AI features guide (published May 2025) and the official crawler documentation.

## Google's Official Guidance (AI Overviews / AI Mode)

Source: [AI features and your website](https://developers.google.com/search/docs/appearance/ai-features)

Key points, verified against the official guide:

- **No additional requirements.** There is no special markup, file, or opt-in to appear in AI Overviews or AI Mode. The prerequisites are the same as for regular Search: the page must be **indexable** and **eligible for snippets**.
- **No new machine-readable files are needed.** Google explicitly states that no "AI text files" or special markup are required — i.e. **Google does not use llms.txt** (see the llms.txt section below).
- **Standard SEO is the optimization.** Content that ranks well and answers questions clearly is what AI features cite. There is no separate "AI ranking" to optimize for.
- **Appearance is controlled with existing snippet controls**, not new directives (see next section).
- **Traffic is reported in Search Console** under the "Web" search type. AI Mode data has been included in the Performance report since June 2025. Clicks from AI Overviews/AI Mode count as ordinary clicks within the "Web" type; since June 2026 Search Console also offers a dedicated Generative AI performance report (impressions only).

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

Trade-off: `nosnippet` / aggressive `max-snippet` values also remove or shorten your regular search snippets, which typically lowers CTR. Use them only for content you genuinely do not want quoted.

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

- **Google does not use it.** The official AI features guide states no new machine-readable files are needed for AI Overviews / AI Mode. Do not expect any Google effect from adding it.
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

- AI Overviews / AI Mode impressions and clicks are included in the **"Web" search type** of the Performance report (AI Mode included since June 2025). Since June 2026 there is also a dedicated **Generative AI performance report** (impressions only — no click breakdown).
- Watch for the pattern "impressions stable, clicks down" on informational queries — a common signature of AI Overviews absorbing clicks.

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
- [Google's common crawlers (Google-Extended)](https://developers.google.com/search/docs/crawling-indexing/google-common-crawlers)
- [Snippet controls (meta tags)](https://developers.google.com/search/docs/appearance/snippet)
- [OpenAI crawlers](https://platform.openai.com/docs/bots)
- [Anthropic crawlers](https://support.claude.com/en/articles/8896518-does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-the-crawler)
- [Perplexity crawlers](https://docs.perplexity.ai/guides/bots)
