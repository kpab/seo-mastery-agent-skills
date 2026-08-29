# Research Notes

Verification log behind the reference files in this repository. Every claim **added or corrected in a
verification pass** must be traceable to an entry here, and every entry must carry a source URL. This
file is not a complete audit of every sentence in the skills — it records what each pass actually
checked, so a later pass can tell verified content from inherited content.

**Research date: 2026-08-29** — all "as of" statements below refer to this date.

Rules for this file:

- Primary sources only (Google Search Central, web.dev, Astro docs, Cloudflare docs, Schema.org).
  Secondary sources are used to *locate* a primary source, never as the source itself.
- Record the date the change took effect, not just the date it was found.
- If a claim could not be confirmed against a primary source, mark it `UNCONFIRMED` and keep it out
  of the skill files.

---

## 1. Google Search — specification changes

### 1.1 FAQ rich results fully retired (2026-05-07)

FAQ rich results stopped appearing in Google Search on **2026-05-07**. Google did not publish a blog
post; the change was announced as a note on the FAQ structured data documentation. Downstream
tooling was retired afterwards: Search Console reporting and Rich Results Test support in June 2026,
Search Console API support in August 2026.

`FAQPage` remains valid schema.org markup — keeping it is not a penalty, but it produces no rich
result. This matches the earlier `HowTo` treatment (rich results discontinued in 2023).

**Impact on this repo:** already reflected in `structured-data.md`, `SKILL.md`, `audit-workflow.md`
and both READMEs as of v1.2.1. Confirmed still accurate — the currently supported feature list
(1.2 below) contains neither FAQ nor HowTo.

- <https://developers.google.com/search/docs/appearance/structured-data/faqpage>
- <https://developers.google.com/search/docs/appearance/structured-data/search-gallery>

### 1.2 Structured data features currently producing rich results

Fetched from the Search gallery on 2026-08-29. These are the features Google documents as
supported:

Article, Book actions, Breadcrumb, Carousel, Course list, Dataset, Discussion forum, Education Q&A,
Employer aggregate rating, Event, Image metadata, Job posting, Local business, Math solver, Movie,
Organization, Product, Profile page, Q&A, Recipe, Review snippet, Software app, Speakable,
Subscription and paywalled content, Vacation rental, Video.

Not present (retired):

| Type | Retired | Note |
|------|---------|------|
| FAQ (`FAQPage`) | 2026-05-07 | Limited to government/health sites from Aug 2023, then fully removed |
| HowTo | 2023-09 | Rich results discontinued |
| Sitelinks Search Box (`SearchAction`) | 2024-11 | `WebSite` markup itself remains current for site name |
| Course Info, Claim Review, Estimated Salary, Learning Video, Special Announcement, Vehicle Listing | announced 2025-06-12 | "Simplifying the search results page" |

Note the asymmetry in the 2025-06-12 announcement: seven types were named, but **Book actions is
still listed as a supported feature** in the gallery as of 2026-08-29. Because the gallery is the
authoritative "what works today" list, the repo treats Book actions as still supported and does not
list it among the retired types.

- <https://developers.google.com/search/docs/appearance/structured-data/search-gallery>
- <https://developers.google.com/search/blog/2025/06/simplifying-search-results>

### 1.3 Search generative AI control in Search Console (2026-06-03) — **material change**

This is the most significant correction to the existing repo content.

Google shipped both a **Search generative AI performance report** and a **site-level control** on
2026-06-03, initially to a subset of UK properties, expanding to other regions from July 2026.

The control lives at **Settings → Search generative AI** and offers:

- "Include my site's links and content in Search generative AI features" (**default**)
- "Exclude my site's links and content from Search generative AI features"
- "Inherit control from parent"

Excluding removes the site from AI Overviews, AI Mode, and generative AI features in Discover —
including being linked from them and being used to ground responses. Google states the control
"isn't used as a ranking or inclusion signal affecting other parts of Search," so normal Search and
Discover are unaffected. Changes generally take effect within 1–2 days.

The generative AI optimization guide states the requirement explicitly:

> "In addition to the technical requirements for Search, a site must be included in Search
> generative AI features in Search Console to be eligible for display in generative AI features on
> Google Search."

**Impact on this repo:** `ai-search.md` and `SKILL.md` previously said appearance in AI Overviews /
AI Mode is governed *only* by indexability + snippet eligibility, and that there is "no opt-in."
That is now incomplete — the Search Console control is a third, independent gate, and it is the only
way to opt out of AI features *without* damaging normal snippets. Corrected in v1.4.0.

- <https://support.google.com/webmasters/answer/16908024>
- <https://developers.google.com/search/blog/2026/06/gen-ai-performance-reports>
- <https://blog.google/products-and-platforms/products/search/new-controls-website-owners/>

### 1.4 Generative AI performance reports (2026-06-03)

Dedicated Search Console reports for Search and Discover showing impressions within generative AI
features (AI Overviews, AI Mode, AI features in Discover), broken down by page, country, device and
date. Data starts **2026-05-18** with no historical backfill, and the initial version reports
**impressions only — no clicks**.

**Impact:** `ai-search.md` already mentioned the report; the data start date and the
impressions-only limitation are added in v1.4.0.

- <https://developers.google.com/search/blog/2026/06/gen-ai-performance-reports>

### 1.5 Official generative AI optimization guide (2026-05-15)

Google published "Optimizing your website for generative AI features on Google Search" under a new
*Generative AI fundamentals* documentation section. Key verbatim points:

> "You don't need to create new machine readable files, AI text files, markup, or Markdown to appear
> in Google Search (including its generative AI capabilities), as Google Search itself doesn't use
> them."

> "There's no requirement to break your content into tiny pieces for AI to better understand it."

> "You don't need to write in a specific way just for generative AI search."

> "Structured data isn't required for generative AI search, and there's no special schema.org markup
> you need to add."

This is now the strongest primary source for the "Google does not use llms.txt" claim, replacing the
weaker inference from the older AI features page.

- <https://developers.google.com/search/docs/fundamentals/ai-optimization-guide>
- <https://developers.google.com/search/blog/2026/05/a-new-resource-for-optimizing>

### 1.6 Crawler IP range files moved (2026-03-31)

Google moved the crawler IP range JSON files out of the Search documentation tree because they cover
crawlers beyond Search (Shopping, AdSense, Gemini):

- Old: `https://developers.google.com/search/apis/ipranges/…`
- New: `https://developers.google.com/static/crawling/ipranges/…`
- `googlebot.json` was renamed to **`common-crawlers.json`**

Published files: `common-crawlers.json`, `special-crawlers.json`, `user-triggered-fetchers.json`,
`user-triggered-fetchers-google.json`, `user-triggered-agents.json`. Addresses are in CIDR format.
For Google IPs outside these categories, `https://www.gstatic.com/ipranges/goog.json` is the
fallback. The old path stays available for a transition period Google described as roughly six
months from the announcement.

Verification remains two-track: reverse DNS (must resolve to `googlebot.com`, `google.com`, or
`googleusercontent.com`, then forward-confirm), or matching against the published ranges.

**Impact:** feeds the "verifying legitimate crawlers at the edge" section of the new `edge-seo.md`.

- <https://developers.google.com/search/blog/2026/03/crawler-ip-ranges>
- <https://developers.google.com/search/docs/crawling-indexing/verifying-googlebot>

### 1.7 Google crawler tokens (verified 2026-08-29)

Common crawlers and their robots.txt tokens: `Googlebot`, `Googlebot-Image`, `Googlebot-Video`,
`Googlebot-News`, `Storebot-Google`, `Google-InspectionTool`, `GoogleOther`, `GoogleOther-Image`,
`GoogleOther-Video`, `Google-CloudVertexBot`, `Google-Extended`.

`Google-Extended` is confirmed to control only whether content may be used "for training future
generations of Gemini models" and grounding in AI applications — it is not a crawler and does not
affect Search.

- <https://developers.google.com/search/docs/crawling-indexing/google-common-crawlers>

### 1.8 robots.txt spec (verified 2026-08-29)

- Supported fields: `user-agent`, `allow`, `disallow`, `sitemap`. **`crawl-delay` and `noindex` are
  not supported.**
- Size limit: "Google enforces a robots.txt file size limit of 500 kibibytes (KiB). Content which is
  after the maximum file size is ignored."
- Caching: "Google generally caches the contents of robots.txt file for up to 24 hours."
- Wildcards: `*` (zero or more characters) and `$` (end of URL). Path matching is case-sensitive.
- Precedence: most specific (longest path) rule wins; on a tie, the least restrictive rule applies.
- Group matching: the most specific `user-agent` match determines the group; file order is
  irrelevant.

**Impact:** the audit workflow contained a "Is Crawl-delay set too high?" check, which is misleading
for Google since the directive is ignored. Corrected in v1.4.0.

- <https://developers.google.com/search/docs/crawling-indexing/robots/robots_txt>

### 1.9 Sitemap limits (verified 2026-08-29)

- "All formats limit a single sitemap to 50MB (uncompressed) or 50,000 URLs."
- A sitemap index file may contain up to 50,000 `<loc>` entries; up to 500 sitemap index files may be
  submitted per site.
- Referenced sitemaps must live in the same directory as the index or lower in the hierarchy.
- gzip (`.xml.gz`) is supported.
- `<lastmod>` is used "if it's consistently and verifiably … accurate."
- **Google ignores `<priority>` and `<changefreq>`.**

**Impact:** `technical-seo.md` listed `priority` as a best practice without noting that Google
ignores it. Corrected in v1.4.0.

- <https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap>
- <https://developers.google.com/search/docs/crawling-indexing/sitemaps/large-sitemaps>

### 1.10 Robots meta / X-Robots-Tag directives (verified 2026-08-29)

Active: `noindex`, `nofollow`, `none`, `nosnippet`, `max-snippet:[n]`, `max-image-preview:[setting]`,
`max-video-preview:[n]`, `notranslate`, `noimageindex`, `unavailable_after:[date]`,
`indexifembedded`. Google documents `noarchive` / `nocache` / `nositelinkssearchbox` as no longer
used.

X-Robots-Tag supports per-user-agent targeting:

```
X-Robots-Tag: googlebot: nofollow
X-Robots-Tag: otherbot: noindex, nofollow
```

Rules without a user agent apply to all; on conflict the more restrictive rule wins.

- <https://developers.google.com/search/docs/crawling-indexing/robots-meta-tag>

### 1.11 Ranking system updates during the covered period

Confirmed named updates in 2026: February 2026 Discover core update, March 2026 core update, March
2026 spam update, May 2026 core update (rolled out 2026-05-21 → 2026-06-02), June 2026 spam update.

Also relevant from the Search Central blog: a new "back button hijacking" spam policy (April 2026)
and a site reputation policy update (August 2026, with EEA-specific enforcement).

No ranking-system change in this period alters the guidance in these skills — core updates are not
actionable as configuration. Recorded here so future freshness passes know the window was checked.

- <https://developers.google.com/search/blog>
- <https://developers.google.com/search/docs/appearance/core-updates>

### 1.12 Other documentation updates worth tracking

- 2026-07-24 — review snippet guidelines gained a rule about fake and undisclosed incentivized
  reviews.
- 2026-07-07 — merchant listing docs now accept both merchant-defined and Google-defined categories
  via `Product.category`; new guidance on `validFrom` / `validThrough` / `priceValidUntil` for sale
  prices.
- 2026-07-01 — AMP docs simplified (AMP viewer / AMP Cache / signed exchange references removed;
  Google links directly to publisher AMP pages).

- <https://developers.google.com/search/updates>

---

## 2. Core Web Vitals

Thresholds are **unchanged** as of 2026-08-29:

| Metric | Good | Needs improvement | Poor |
|--------|------|-------------------|------|
| LCP | ≤ 2.5 s | 2.5–4.0 s | > 4.0 s |
| INP | ≤ 200 ms | 200–500 ms | > 500 ms |
| CLS | ≤ 0.1 | 0.1–0.25 | > 0.25 |

Assessment is at the **75th percentile** of field data (CrUX), evaluated separately for mobile and
desktop. INP replaced FID as a Core Web Vital in March 2024; no further metric change has been
announced.

`scheduler.yield()`: supported in Chromium and Firefox, **not supported in Safari**, so it is not
Baseline. Feature detection with a `setTimeout` fallback is still required — the existing code
sample in `core-web-vitals.md` does this correctly, but its "Chrome 129+" comment was narrowed to
Chromium-only and is corrected to name the real support picture.

- <https://web.dev/articles/vitals>
- <https://developer.mozilla.org/en-US/docs/Web/API/Scheduler/yield>

---

## 3. Astro

### 3.1 Astro 6.0 (released 2026-03-10)

Headline features: built-in **Fonts API** (download, cache, fallback generation, preload), built-in
**CSP API** (hashes scripts and styles for static and dynamic output), **Live Content Collections**
(request-time content through the content layer), a redesigned dev server built on Vite's
Environment API running the real production runtime (notably `workerd` for Cloudflare Workers), and
an experimental queued rendering strategy reported at up to 2× faster rendering.

- <https://astro.build/blog/astro-6/>

### 3.2 Astro 6 breaking changes relevant to SEO

| Change | Detail |
|--------|--------|
| `<ViewTransitions />` removed | Renamed to `<ClientRouter />` in v5 (deprecated), **removed entirely in v6**. Replace the import and the component. |
| `Astro.site` in `getStaticPaths()` deprecated | "Replace all occurrences of `Astro.site` with `import.meta.env.SITE`". Accessing other `Astro` properties inside `getStaticPaths()` throws. |
| Endpoint trailing slashes | Custom endpoints whose URL has a file extension (e.g. `sitemap.xml`) "can only be accessed without a trailing slash … regardless of your `build.trailingSlash` configuration". |
| Legacy content collections removed | `src/content/config.ts` is gone; collections must be defined in `src/content.config.ts` with an explicit `loader`. |
| Image behavior | Images never upscale by default; cropping applies by default (drop redundant `fit="contain"`); SVG rasterization when `format` is specified. |
| Heading IDs | Trailing hyphens are no longer stripped from generated Markdown heading IDs — existing anchor links may break. |

- <https://docs.astro.build/en/guides/upgrade-to/v6/>

### 3.3 Client directives (hydration) — verified

| Directive | Hydrates | Options |
|-----------|----------|---------|
| `client:load` | immediately on page load, high priority | — |
| `client:idle` | after load, when `requestIdleCallback` fires (falls back to the `load` event) | `timeout` (ms) |
| `client:visible` | when the component enters the viewport (`IntersectionObserver`) | `rootMargin` |
| `client:media` | when a CSS media query matches | media query string |
| `client:only` | client-only, immediately on page load; no server render | framework name, `slot="fallback"` |

`server:defer` turns a component into a **server island**, rendered on demand outside the main page
render.

- <https://docs.astro.build/en/reference/directives-reference/>

### 3.4 View transitions — verified

Two distinct mechanisms:

1. **Native cross-document (MPA) view transitions** — CSS only, no Astro JavaScript, no router.
2. **`<ClientRouter />`** — converts the MPA into a client-routed app, enabling `transition:persist`,
   shared state, and lifecycle hooks, at the cost of "needing to manually reinitialize scripts or
   state after navigation."

Directives: `transition:name`, `transition:animate` (`slide` / `none` / `initial` / custom),
`transition:persist`.

Lifecycle events, in order: `astro:before-preparation` → `astro:after-preparation` →
`astro:before-swap` → `astro:after-swap` → `astro:page-load`.

Documented caveats that matter for SEO/analytics:

- "Bundled module scripts … are only ever executed once. After initial execution they will be
  ignored" — use `data-astro-rerun` on inline scripts that must run per navigation.
- The router announces page title changes to assistive technology automatically.
- `prefers-reduced-motion` is respected (animations disabled).
- Fallback for non-supporting browsers: `animate`, `swap`, or `none`.

- <https://docs.astro.build/en/guides/view-transitions/>

### 3.5 `@astrojs/sitemap` — verified

Requires `site` in `astro.config.mjs`. Options confirmed present: `filter`, `customPages`,
`customSitemaps`, `entryLimit` (default **45000**), `changefreq`, `lastmod`, `priority`, `serialize`,
`chunks`, `i18n`, `xslURL`, `filenameBase`, `namespaces`.

The `i18n` option (`defaultLocale` + `locales` map) emits `<xhtml:link rel="alternate" hreflang=…>`
entries for each translated page. Output is `sitemap-index.xml` plus `sitemap-0.xml`, `sitemap-1.xml`, …

Note the interaction with 3.2: because `sitemap.xml` has a file extension, link to it **without** a
trailing slash on Astro 6.

- <https://docs.astro.build/en/guides/integrations-guide/sitemap/>

### 3.6 Content Layer API — verified

Collections are defined in `src/content.config.ts` with a required `loader` (`glob()` or `file()`)
and an optional Zod `schema`. Query with `getCollection()` / `getEntry()`; render Markdown/MDX with
`render(entry)`. This is the API the new `astro-seo.md` uses for schema-validated JSON-LD generation.

- <https://docs.astro.build/en/guides/content-collections/>

### 3.7 Context: Cloudflare acquired the Astro team (2026-01-16)

Cloudflare announced the acquisition of The Astro Technology Company on 2026-01-16; Astro remains
open source. This is background, not a technical claim — it is recorded because it explains why the
Astro + Cloudflare pairing is the axis this repo specializes in, and because Astro 6's dev server
runs `workerd` directly.

- <https://www.cloudflare.com/press/press-releases/2026/cloudflare-acquires-astro-to-accelerate-the-future-of-high-performance-web-development/>

---

## 4. Cloudflare Workers / Pages

### 4.1 Platform direction

`_redirects` and `_headers` are supported **natively in Workers with static assets**, with the same
syntax as Pages — the files go in the static asset directory. Cloudflare's migration guide documents
Workers as having "a distinctly broader set of features" and lists Cron Triggers, native Durable
Objects, Tail Workers, Workers Logs, Logpush and the Cloudflare Vite plugin as Workers-only.

The frequently repeated claim that "Pages is in maintenance mode" **could not be confirmed** —
Cloudflare's documentation never uses the words "maintenance mode" or "deprecated". What it does
carry, as a banner at the top of the Pages documentation (last updated 2026-08-25), is:

> "Workers supports most Pages use cases and offers a broader feature set. It is Cloudflare's primary
> platform for building applications. Start new projects with Workers."

That is the strongest primary statement available, and it supports the skill files' framing —
Workers is where new capability lands, both platforms are documented — without asserting a
deprecation Cloudflare has not announced.

- <https://developers.cloudflare.com/workers/static-assets/migration-guides/migrate-from-pages/>

### 4.2 `_redirects` — verified limits

- Format: `[source] [destination] [code?]`; `code` defaults to **302**. `#` starts a comment.
- Supported status codes: **301, 302, 303, 307, 308**. A `200` destination performs a proxy/rewrite
  (relative URLs only).
- Limits: "A `_redirects` file is limited to 2,000 static redirects and 100 dynamic redirects, for a
  combined total of 2,100 redirects." Each declaration has a **1,000-character** limit.
- Placeholders `:name` match "all characters apart from the delimiter, which when part of the host,
  is a period (`.`) or a forward-slash (`/`) and may only be a forward-slash (`/`) when part of the
  path." **A path placeholder therefore matches dots** — `/:slug` also matches `report.pdf`. Splats
  `*` are greedy and only **one per URL** is allowed. Both are referenceable in the destination.
- Not supported: query-parameter matching, domain-level redirects, conditional (country / language /
  cookie) redirects.
- **Critical:** redirects "are not applied to requests served by Pages Functions" / "not applied to
  requests served by your Worker code, even if the request URL matches a rule."

- <https://developers.cloudflare.com/pages/configuration/redirects/>
- <https://developers.cloudflare.com/workers/static-assets/redirects/>

### 4.3 `_headers` — verified limits

- Format: a URL/pattern line, then indented `Name: value` lines.
- Limits: **100 header rules** max; **2,000 characters per line**.
- Same splat/placeholder matching as `_redirects`; `:splat` is referenceable in header *values*.
- `! Header-Name` removes a default or previously applied header.
- **Matching rules accumulate rather than override:** "If a header is applied twice in the `_headers`
  file, the values are joined with a comma separator." This makes Google's per-user-agent
  `X-Robots-Tag` form — which relies on *separate* header lines — inexpressible in `_headers`, and
  makes overlapping `Cache-Control` rules produce a joined value instead of the specific one.
- **Critical:** "Custom headers defined in the `_headers` file are not applied to responses generated
  by Pages Functions" / "by your Worker code, even if the request URL matches a rule" — including SSR
  frameworks, `_worker.js`, and `assets.run_worker_first` routes.

- <https://developers.cloudflare.com/pages/configuration/headers/>
- <https://developers.cloudflare.com/workers/static-assets/headers/>

### 4.4 Static asset configuration keys — verified

Under `assets` in `wrangler.jsonc`: `directory` (required), `binding` (exposes `env.ASSETS.fetch()`),
`run_worker_first` (boolean **or an array of route patterns**, `*` for deep matching and a `!` prefix
for negation; default `false`). Only one static asset collection per Worker.

Two keys decide canonical URL shape before any user-defined redirect runs:

- `html_handling`: `auto-trailing-slash` (**default**), `force-trailing-slash`, `drop-trailing-slash`,
  `none`. In the default mode `/file.html` redirects to `/file` and `/folder/` serves
  `/folder/index.html`; `force-trailing-slash` 307-redirects `/file` to `/file/`.
- `not_found_handling`: `none` (**default**), `404-page`, `single-page-application`. `404-page` serves
  the nearest `404.html` with a 404 status; `single-page-application` returns 200 + `index.html` for
  every unmatched path, which produces indexable soft 404s.

`.assetsignore` prevents files such as `_worker.js`, `_redirects` and `_headers` from being uploaded
as client-side assets.

- <https://developers.cloudflare.com/workers/static-assets/binding/>

### 4.5 HTMLRewriter — verified

`new HTMLRewriter().on(selector, handler).onDocument(handler).transform(response)`. Supported
selectors include `*`, `E`, `.class`, `#id`, `[attr]`, `[attr="v"]`, `[attr^="v"]`, `E F`, `E > F`,
`:nth-child(n)`, `:first-child`, `:not(s)`.

Element handler methods: `getAttribute`, `setAttribute`, `removeAttribute`, `before`, `after`,
`prepend`, `append`, `replace`, `remove`, `setInnerContent`.

Streaming caveat: "Text chunks are not the same thing as text nodes" — a text node may arrive across
several chunks; use `lastInTextNode` when accumulating. A handler that throws aborts parsing and
errors the response body.

- <https://developers.cloudflare.com/workers/runtime-apis/html-rewriter/>

### 4.6 Bot verification at the edge

- **Verified Bots**: Cloudflare's program for bots that identify honestly (Web Bot Auth signature,
  published IP list with a stable user agent, or reverse DNS) and behave (obey robots.txt, reasonable
  rates, no evasion).
- **Web Bot Auth**: cryptographic HTTP message signatures (`Signature`, `Signature-Input`,
  `Signature-Agent` headers, Ed25519 keys) used to verify automated requests. The IETF has chartered
  a Web Bot Auth working group.
- **AI Crawl Control** (formerly *AI Audit*): dashboard for seeing which AI services fetch a site,
  allow/block rules per crawler, robots.txt compliance tracking, and a pay-per-crawl model
  (private beta). Available on all plans.

- <https://developers.cloudflare.com/bots/concepts/bot/verified-bots/>
- <https://developers.cloudflare.com/bots/reference/bot-verification/web-bot-auth/>
- <https://developers.cloudflare.com/ai-crawl-control/>

---

## 5. Corrections applied to existing files

Issues found by re-reading every existing reference file against the findings above. All are fixed
in v1.4.0 and listed in `CHANGELOG.md`.

| File | Problem | Fix |
|------|---------|-----|
| `ai-search.md`, `SKILL.md` | Stated there is no opt-in/opt-out for AI Overviews / AI Mode beyond snippet controls | Added the Search generative AI control (§1.3) as a separate, ranking-neutral gate |
| `ai-search.md` | Cited the May 2025 AI features page as the primary source | Added the 2026-05-15 generative AI optimization guide (§1.5) with its verbatim mythbusting |
| `ai-search.md` | Generative AI report described without limits | Added data start 2026-05-18, impressions-only (§1.4) |
| `technical-seo.md` | Sitemap best-practice table recommended `priority` / `changefreq` without noting Google ignores both | Annotated (§1.9) |
| `technical-seo.md` | Crawl budget section recommended "parameter handling (Search Console)" | Removed — the URL Parameters tool was retired in 2022 |
| `technical-seo.md` | Nuxt SSR example used Nuxt 2 `asyncData` + `$axios` | Replaced with Nuxt 3+ `useAsyncData` / `$fetch` |
| `technical-seo.md` | No pointer to crawler verification | Added reverse-DNS + IP range files with the new paths (§1.6) |
| `core-web-vitals.md` | Nuxt config example used Nuxt 2 `render.http2.push` (HTTP/2 Server Push is removed from Chrome) | Replaced with a Nuxt 3+ config using `@nuxt/image` and preload hints |
| `core-web-vitals.md` | `scheduler.yield()` labelled "Chrome 129+" | Corrected to Chromium + Firefox, not in Safari, not Baseline (§2) |
| `audit-workflow.md` | robots.txt check asked whether `Crawl-delay` is set too high | Replaced — Google ignores `crawl-delay` (§1.8) |
| `audit-workflow.md` | AI readiness phase did not check the Search Console generative AI control | Added as a checklist item (§1.3) |

---

## 6. Second pass — review findings (2026-08-29)

Three independent reviews were run against the v1.4.0 branch. What they overturned:

### 6.1 Article `headline` has no character limit

`astro-seo.md` and `structured-data.md` (the latter since v1.0.0) presented a **110-character limit**
on `headline` as a Google requirement. Google removed that limit from the Article documentation in
January 2023. The current definition is:

> "The title of the article. Consider using a concise title, as long titles may be truncated on some
> devices."

The Article page also states "There are no required properties; instead, add the properties that
apply to your content." The schema cap is retained in the Astro example but relabelled as an
editorial choice.

- <https://developers.google.com/search/docs/appearance/structured-data/article>

### 6.2 Claims removed for lack of a primary source

Written from secondary sources or from general knowledge, now either removed or explicitly
attributed:

| Claim | Status |
|-------|--------|
| "410 is processed faster than 404" | **Removed.** Not in Google's documentation; recent Googler statements describe the difference as negligible. The files now recommend 410 for semantic correctness only |
| Generative AI report data starts 2026-05-18 | **Downgraded.** Not in the launch blog post or the Search Console help page. Attributed in `ai-search.md` as a secondary-source figure; removed from `SKILL.md` |
| Generative AI control "expanding from July 2026" | **Replaced** with Google's own wording: rolling out to a UK subset first, "before rolling them out to website owners globally" |
| Control takes effect "within 1–2 days" | **Corrected** to the help page's fuller wording: exclusion "generally takes a few days", 1–2 days after the control goes live, "but some content may take longer … due to caching and propagation" |

Claims that remain in `edge-seo.md` on operational rather than documentary grounds, flagged here so a
later pass can revisit them: Googlebot crawling predominantly from US IP addresses; sustained 5xx
reducing site-wide crawl rate; crawlers treating 503 + `Retry-After` as "come back later". These are
widely-held operational guidance rather than quoted specification.

### 6.3 Cloudflare corrections

Both were misreadings of the documentation, corrected in §4.2 and §4.3 above: placeholders **do**
match dots inside the path, and repeated header names in `_headers` are **joined with a comma**
rather than overriding.

A third issue was behavioural rather than factual: Cloudflare serves a matching static asset before
invoking the Worker, so middleware-style Workers (HTMLRewriter, query canonicalization) need their
HTML paths listed in `run_worker_first` or they never execute.

- <https://developers.cloudflare.com/workers/static-assets/routing/>

### 6.4 Pages banner

See §4.1 — the review surfaced a quotable primary statement, which replaced the `UNCONFIRMED` note.
