# Changelog

All notable changes to the `seo-mastery` and `seo-mastery-jp` skills are documented here. Both
skills share version numbers.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Versioning policy for a knowledge repository:

- **MAJOR** — a breaking change to structure: a reference file removed or renamed, a skill renamed,
  or guidance reversed in a way that invalidates advice given by an earlier version.
- **MINOR** — new knowledge: a new reference file, a new template, a new section, expanded coverage.
- **PATCH** — corrections and freshness: fixing an inaccuracy, updating a retired feature, refreshing
  `last_verified` dates, wording and tooling fixes.

Every reference file carries a `last_verified` date in its frontmatter. See
[docs/research-notes.md](docs/research-notes.md) for the sources behind each factual claim.

## [Unreleased]

## [1.4.0] - 2026-08-29

### Added

- **`astro-seo.md` (EN/JP)** — Astro-specific SEO layer: `client:*` directives mapped to INP/LCP
  costs, `server:defer` server islands, canonical and Open Graph generation from
  `Astro.site` + `Astro.url`, JSON-LD generated from Content Collections schemas (with
  `</script>` escaping), `@astrojs/sitemap` configuration including multilingual sitemaps with
  hreflang, view transitions (native vs. `<ClientRouter />`) and their analytics pitfalls, and
  version migration notes for the SEO-affecting breaking changes in Astro 7 (Rust compiler HTML
  validation, `compressHTML: 'jsx'` collapsing whitespace in indexable text, the Sätteri Markdown
  pipeline) and Astro 6
- **`edge-seo.md` (EN/JP)** — Cloudflare Workers/Pages SEO layer: `_redirects` design and limits,
  `_headers` with `X-Robots-Tag` and cache strategy, the static-asset vs. Worker-code blind spot,
  dynamic `sitemap.xml` generation from D1/KV with edge caching, crawler verification by published
  IP ranges and Web Bot Auth, HTMLRewriter metadata rewriting and JSON-LD injection, and the
  relationship between edge caching and crawl budget
- `last_verified` frontmatter on every skill markdown file, enforced by CI
- `docs/research-notes.md` — the verification log behind every factual claim, with source URLs
- `.github/workflows/freshness-reminder.yml` — opens a freshness-check issue on the 1st of each
  month with the list of sources to re-verify
- `.github/workflows/release.yml` — publishes a GitHub Release on `v*` tags, using the matching
  CHANGELOG section as the release notes
- Versioning policy section in both READMEs, and Astro / Cloudflare Workers/Pages in Supported
  Frameworks

### Changed

- Skill descriptions now include Astro and Cloudflare Workers/Pages invocation triggers, and state
  which of the two skills to load: English input selects `seo-mastery`, Japanese input selects
  `seo-mastery-jp`. Previously the two descriptions were near-identical, so either could fire
- `SKILL.md` (EN/JP) gained an "Astro and Edge (Cloudflare) Specifics" section, registered the two
  new reference files, and now states that topic files and platform files must be read *together* —
  sitemaps, hreflang and crawl budget each span more than one file
- `audit-workflow.md` (EN/JP) points at the platform files, since several audit phases surface
  findings whose cause is platform-specific
- README positioning no longer claims freshness is "guaranteed": what is guaranteed is the process
  and the date stamp. Supported Frameworks now links each entry to the file that backs it, and drops
  the WordPress entry, which had no supporting content anywhere in the repo
- `CONTRIBUTING.md`'s Japanese section is a full translation rather than a summary; it previously
  omitted the repository layout, the one-language-PR rule, the freshness workflow, and all four
  content guidelines
- `marketplace.json` gained `astro`, `cloudflare-workers` and `edge-seo` keywords
- CHANGELOG restructured to Keep a Changelog format; historical entries re-dated from git history
  (the v1.0.0 entry previously read "2025-01"; the initial commits are dated 2025-12-29/30)
- `scripts/validate.py` now verifies `last_verified` on every skill markdown file (present, ISO
  format, not in the future, identical between EN and JP) and ignores `#` lines inside fenced code
  blocks when comparing document structure

### Fixed

- **AI search eligibility was incomplete.** `ai-search.md` and `SKILL.md` stated that indexability
  plus snippet eligibility were the only requirements for AI Overviews / AI Mode. Google's
  generative AI optimization guide (2026-05-15) adds a third: the site must be included in Search
  generative AI features in Search Console. Documented the **Search generative AI control**
  (Settings → Search generative AI, rolled out 2026-06-03), its three options, and the fact that
  Google states it "isn't used as a ranking or inclusion signal affecting other parts of Search" —
  making it the correct tool for AI-only exclusion, unlike `nosnippet`
- `ai-search.md` now cites the 2026 generative AI optimization guide, including its verbatim
  mythbusting on llms.txt, content chunking, AI-specific writing, and AI-specific schema
- Search generative AI performance report described with its actual limits: no historical backfill,
  impressions only. The 2026-05-18 data start is attributed as a secondary-source figure, since
  Google's own documentation does not state one
- `technical-seo.md` sitemap best practices: noted that **Google ignores `<priority>` and
  `<changefreq>`**, that `lastmod` is only used when consistently accurate, and added the sitemap
  index limits
- `technical-seo.md` crawl budget: removed "parameter handling (Search Console)" — the URL
  Parameters tool was retired in 2022
- `technical-seo.md` gained the robots.txt limits Google actually enforces (500 KiB, 24-hour cache,
  `crawl-delay` and `noindex` unsupported, longest-match precedence)
- `technical-seo.md` Nuxt SSR example replaced Nuxt 2 `asyncData` + `$axios` with Nuxt 3+
  `useAsyncData` / `$fetch`
- `core-web-vitals.md` Nuxt example replaced `render.http2.push` (HTTP/2 Server Push, removed from
  Chrome) with a Nuxt 3+ `@nuxt/image` config and explicit LCP preload
- `core-web-vitals.md` corrected the `scheduler.yield()` support note: Chromium and Firefox, not
  Safari, not Baseline
- `audit-workflow.md` robots.txt check no longer asks whether `Crawl-delay` is set too high; it now
  flags `crawl-delay` / `noindex` lines as ineffective for Google
- `audit-workflow.md` AI readiness phase now checks the Search Console generative AI control

Found by review of this branch before release:

- **Article `headline` has no 110-character limit.** Google removed it from the documentation in
  January 2023; the current wording only warns that long titles may be truncated. The claim was
  presented as a Google requirement in `structured-data.md` (since v1.0.0) and `astro-seo.md`
- **`_redirects` placeholders do match dots inside the path.** The delimiter is `/` in the path and
  `.` or `/` only in the host, so `/:slug` also matches `report.pdf` — the previous wording made
  such rules look safe for file URLs
- **`_headers` rules accumulate rather than override**, joining repeated header names with a comma.
  The per-crawler `X-Robots-Tag` example would therefore have shipped one combined header that
  Google does not document parsing; removed, with the collision rule documented. The `/*.html`
  cache rule was dropped too — under `auto-trailing-slash` it matches nothing
- **Middleware-style Workers need `run_worker_first`.** Cloudflare serves a matching static asset
  before invoking the Worker, so the HTMLRewriter and query-canonicalization examples could never
  have executed under the config shown
- Supplied the `ipInCidr` implementation the crawler check called but never defined; made the range
  lookup fail open rather than 500 on a fetch error; stopped an empty KV value poisoning the cache
- Dynamic sitemap generation no longer 500s on a NULL or non-ISO `updated_at`, strips
  XML-illegal control characters, and cannot emit a zero-entry sitemap index
- HTMLRewriter handlers now catch their own exceptions (a throwing handler errors the response
  body), guard missing values, and scope the selector to `head > title` so inline SVG titles are
  left alone
- Removed the unsourced claim that 410 is processed faster than 404; attributed the generative AI
  report's 2026-05-18 data start as a secondary-source figure and removed it from `SKILL.md`;
  replaced "expanding from July 2026" and "takes effect within 1–2 days" with Google's own wording
- `freshness-reminder.yml` declared only `issues: write`, which sets every other scope to `none` —
  `actions/checkout` would have failed on the very first run
- `validate.py` crashed with a traceback on a syntactically valid but impossible date, could fail in
  CI for a file stamped "today" in JST, mispaired indented code fences, and reported one malformed
  file three times. It also now checks that every declared version agrees — v1.2.1 and v1.2.2
  shipped with both manifests still reading 1.2.0
- `release.yml`'s empty-section guard could never fire (the extracted section always contains a
  newline), the notes regex now terminates on end-of-file rather than relying on the link-definition
  block, and a re-run updates the release instead of failing on "already exists"

Found by a second review pass on the same branch:

- **The dynamic sitemap published 404s for hierarchical slugs.** `locFor()` ran
  `encodeURIComponent()` over the whole slug, so `2026/my-post` became `2026%2Fmy-post` — a
  different URL, submitted to Google as canonical. It now encodes each path segment
- **The tracking-parameter 301 rewrote parameters it was not meant to touch.** Mutating
  `url.searchParams` re-serialises the whole query, turning `?q=a%20b` into `?q=a+b`; an origin that
  normalises it back would bounce the request between the two rules. It now rebuilds the query from
  the raw pairs
- The sitemap Worker called `cache.put()` without checking the method, so a HEAD from any crawler or
  uptime monitor rejected inside `waitUntil`; it also ran a cache lookup before routing, on every
  static asset request, and spent a second `COUNT(*)` query per page purely to bound the page number

## [1.3.0] - 2026-08-28

### Added

- New reference file `ai-search.md` (EN/JP): Google's official AI features guidance (AI Overviews /
  AI Mode prerequisites, snippet controls, measurement), the exact scope of `Google-Extended`, AI
  crawler UA list with robots.txt recipes (training opt-out vs. AI search citations), llms.txt
  positioning (Google does not use it), and AI-citable content design (#6)
- "AI Search Readiness" phase (2.6) in the audit workflow: robots.txt AI crawler intent check and
  snippet control intent check

### Changed

- Registered the new file in the SKILL.md file table and added an AI search overview section; added
  AI trigger words (AI Overviews / AIO, AI Mode, generative AI search, llms.txt, GPTBot, ClaudeBot,
  Google-Extended) to both skill descriptions

## [1.2.2] - 2026-08-28

### Fixed

- Replaced the "WebSite (Sitelinks Search Box)" template with a plain WebSite template (`name` /
  `alternateName` / `url`): the Sitelinks Search Box (`potentialAction` / `SearchAction`) was
  retired in November 2024, while WebSite markup remains current for site name recognition (#5)

## [1.2.1] - 2026-08-28

### Fixed

- Updated FAQ rich results guidance: Google retired FAQ rich results entirely on 2026-05-07
  (documentation and Search Console reports removed); FAQPage markup is now documented as
  semantic-only, matching the HowTo treatment (#4)
- Replaced the FAQ structured data example in the competitive gap analysis template with video
  structured data

### Added

- Audit checklist item to detect markup for deprecated rich results (FAQ, HowTo, Sitelinks Search
  Box) and propose removal or annotation

## [1.2.0] - 2026-07-10

### Added

- CONTRIBUTING.md with the EN/JP synchronization policy (English is the source of truth)
- CI (GitHub Actions) validating frontmatter, JSON-LD template syntax, manifests, and EN/JP
  structural sync
- Official Claude Code plugin marketplace support
  (`claude plugin marketplace add kpab/seo-mastery-agent-skills`)
- Explicit "use when" invocation triggers in both skill descriptions

### Changed

- Restructured SKILL.md as a lightweight overview + navigation layer; templates and detailed
  procedures now live only in the reference files

### Fixed

- Updated stale Google Search guidance: replaced the retired Mobile-Friendly Test with
  Lighthouse-based checks; noted that FAQ rich results are restricted and HowTo rich results were
  discontinued (2023)

## [1.1.0] - 2026-06-17

### Added

- "Handling Untrusted External Content" guidance to mitigate indirect prompt injection from fetched
  pages
- Repository discoverability improvements and corrected skill install instructions

### Changed

- Fetched content is now treated as untrusted data with explicit boundary markers

## [1.0.0] - 2025-12-30

### Added

- Initial release, created from Google's official SEO guides
- Comprehensive technical SEO, content SEO, and structured data coverage
- Core Web Vitals (INP-compliant)
- E-E-A-T optimization checklist
- Site audit workflow
- English and Japanese skill variants

[Unreleased]: https://github.com/kpab/seo-mastery-agent-skills/compare/v1.4.0...HEAD
[1.4.0]: https://github.com/kpab/seo-mastery-agent-skills/compare/v1.3.0...v1.4.0
[1.3.0]: https://github.com/kpab/seo-mastery-agent-skills/compare/v1.2.2...v1.3.0
[1.2.2]: https://github.com/kpab/seo-mastery-agent-skills/compare/v1.2.1...v1.2.2
[1.2.1]: https://github.com/kpab/seo-mastery-agent-skills/compare/v1.2.0...v1.2.1
[1.2.0]: https://github.com/kpab/seo-mastery-agent-skills/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/kpab/seo-mastery-agent-skills/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/kpab/seo-mastery-agent-skills/releases/tag/v1.0.0
