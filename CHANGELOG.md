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
  hreflang, view transitions (native vs. `<ClientRouter />`) and their analytics pitfalls, and an
  Astro 6 migration table for SEO-affecting breaking changes
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

- Skill descriptions now include Astro and Cloudflare Workers/Pages invocation triggers
- `SKILL.md` (EN/JP) gained an "Astro and Edge (Cloudflare) Specifics" section and registered the
  two new reference files
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
- Search generative AI performance report described with its actual limits: data starts 2026-05-18,
  no historical backfill, impressions only
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
