# SEO Mastery Agent Skills

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Agent%20Skill-7C3AED)](https://docs.claude.com/en/docs/claude-code/overview)
[![Languages: EN | JP](https://img.shields.io/badge/Languages-EN%20%7C%20JP-success)](docs/README.ja.md)

Comprehensive SEO optimization Agent Skills for Claude Code & Codex. Based on Google's official documentation, providing integrated support for technical SEO, content SEO, structured data, Core Web Vitals, E-E-A-T, AI search, edge/static-site SEO, and site audits.

[日本語版 README はこちら](docs/README.ja.md)

## Why This Skill

- **Lightweight, zero dependency.** Markdown only — no API keys, no MCP server, no scripts to install, nothing to run. Copy the folder and the skill works offline.
- **Strong on edge and static sites.** Dedicated reference layers for **Astro** and **Cloudflare Workers/Pages**: island hydration vs. INP/LCP, `_redirects` / `_headers` and their Worker-code blind spots, dynamic sitemaps from D1/KV, crawler verification at the edge.
- **Staleness is tracked, not hoped away.** Every reference file carries a `last_verified` date that CI enforces; claims added or corrected in a verification pass are traceable to a primary source in [docs/research-notes.md](docs/research-notes.md); changes are recorded in [CHANGELOG.md](CHANGELOG.md) under semver; and a scheduled workflow opens a re-verification issue every month. What is guaranteed is the process and the date stamp — not that every line is currently correct.

## Features

- **Technical SEO Checklist** - robots.txt, sitemap, canonical, hreflang, etc.
- **Content SEO Optimization** - Meta tags, heading structure, E-E-A-T strategies
- **Structured Data Templates** - Article, FAQ, Product, LocalBusiness, etc.
- **Core Web Vitals Support** - Detailed optimization techniques for LCP, INP, CLS
- **AI Search** - AI Overviews / AI Mode eligibility and controls, AI crawler management
- **Astro & Edge SEO** - Astro-specific patterns and Cloudflare Workers/Pages edge SEO
- **Site Audit Workflow** - Systematic audit process and report formats
- **Practical Code Examples** - Ready-to-use templates

## Installation

Each skill is made up of `SKILL.md` plus several reference files (`technical-seo.md`, `content-seo.md`, etc.). Install **all** files in a skill folder — fetching only `SKILL.md` leaves the skill incomplete.

### Recommended: Claude Code plugin

```bash
claude plugin marketplace add kpab/seo-mastery-agent-skills
claude plugin install seo-mastery@seo-mastery-agent-skills
```

This installs both the English and Japanese skills and keeps them updatable via the plugin manager.

### Alternative: clone the whole repo

```bash
git clone https://github.com/kpab/seo-mastery-agent-skills.git
# Then copy the skill folder(s) you want:
cp -r seo-mastery-agent-skills/.claude/skills/seo-mastery     .claude/skills/      # English
cp -r seo-mastery-agent-skills/.claude/skills/seo-mastery-jp  .claude/skills/      # Japanese
```

### Claude Code / Claude.ai (download all files)

```bash
SKILL=seo-mastery   # or seo-mastery-jp
BASE=https://raw.githubusercontent.com/kpab/seo-mastery-agent-skills/main/.claude/skills/$SKILL
mkdir -p .claude/skills/$SKILL
for f in SKILL.md technical-seo.md content-seo.md structured-data.md core-web-vitals.md ai-search.md astro-seo.md edge-seo.md audit-workflow.md; do
  curl -fsSL -o .claude/skills/$SKILL/$f "$BASE/$f"
done
```

### Codex

```bash
# Same as above, but target a Codex skills directory.
# Project local: .codex/skills/$SKILL   |   User global: ~/.codex/skills/$SKILL
SKILL=seo-mastery   # or seo-mastery-jp
BASE=https://raw.githubusercontent.com/kpab/seo-mastery-agent-skills/main/.claude/skills/$SKILL
mkdir -p .codex/skills/$SKILL
for f in SKILL.md technical-seo.md content-seo.md structured-data.md core-web-vitals.md ai-search.md astro-seo.md edge-seo.md audit-workflow.md; do
  curl -fsSL -o .codex/skills/$SKILL/$f "$BASE/$f"
done
```

## File Structure

```
.claude/skills/
├── seo-mastery/              # English version
│   ├── SKILL.md              # Main skill file
│   ├── technical-seo.md      # Technical SEO details
│   ├── content-seo.md        # Content SEO details
│   ├── structured-data.md    # Structured data details
│   ├── core-web-vitals.md    # Core Web Vitals details
│   ├── ai-search.md          # AI search details
│   ├── astro-seo.md          # Astro-specific SEO
│   ├── edge-seo.md           # Cloudflare Workers/Pages edge SEO
│   └── audit-workflow.md     # Audit workflow details
└── seo-mastery-jp/           # Japanese version
    ├── SKILL.md              # Main skill file
    ├── technical-seo.md      # Technical SEO details
    ├── content-seo.md        # Content SEO details
    ├── structured-data.md    # Structured data details
    ├── core-web-vitals.md    # Core Web Vitals details
    ├── ai-search.md          # AI search details
    ├── astro-seo.md          # Astro-specific SEO
    ├── edge-seo.md           # Cloudflare Workers/Pages edge SEO
    └── audit-workflow.md     # Audit workflow details

docs/research-notes.md        # Verification log: every claim, with its source
CHANGELOG.md                  # Keep a Changelog + semver release history
```

Every file under `.claude/skills/` carries a `last_verified: YYYY-MM-DD` frontmatter field, which CI enforces (present, valid, not in the future, identical between EN and JP).

## Usage Examples

```
# Request meta tag optimization
"Optimize the meta tags for this page"

# Generate structured data
"Add Article structured data to this blog post"

# Run site audit
"Perform an SEO audit on this site"

# Improve Core Web Vitals
"How can I improve LCP?"

# Generate FAQ structured data
"Add JSON-LD to this FAQ page"
```

## Included Templates

### Structured Data
- Article / NewsArticle / BlogPosting
- FAQ (Frequently Asked Questions)*
- HowTo*
- Product
- LocalBusiness
- BreadcrumbList
- VideoObject
- Organization / WebSite
- Event

\* FAQ rich results were fully discontinued by Google on May 7, 2026, and HowTo rich results were discontinued in 2023. Templates are kept for semantic markup purposes.

### Technical SEO
- robots.txt template
- sitemap.xml template
- hreflang implementation patterns
- canonical URL configuration

### Core Web Vitals
- LCP optimization code
- INP optimization code
- CLS optimization code
- Measurement & monitoring scripts

## Supported Frameworks

- **Astro** — dedicated reference file ([astro-seo.md](.claude/skills/seo-mastery/astro-seo.md)); verified against Astro 6
- **Cloudflare Workers / Pages** — dedicated reference file ([edge-seo.md](.claude/skills/seo-mastery/edge-seo.md))
- Next.js — code examples in [core-web-vitals.md](.claude/skills/seo-mastery/core-web-vitals.md) and [technical-seo.md](.claude/skills/seo-mastery/technical-seo.md)
- Nuxt 3+ — same files
- Static HTML — every template is framework-agnostic

Everything else (WordPress, Rails, Django, …) is covered only by the framework-agnostic guidance;
there is no CMS-specific reference file.

## Versioning

This repository follows [Semantic Versioning](https://semver.org/), interpreted for a knowledge base rather than an API: a **MAJOR** bump means a breaking structural change (a reference file removed or renamed, a skill renamed, or guidance reversed such that earlier advice is invalidated); a **MINOR** bump means new knowledge (a new reference file, template, or section); a **PATCH** bump means corrections and freshness work (fixing an inaccuracy, documenting a retired feature, refreshing `last_verified` dates). The version in `SKILL.md`, both `marketplace.json` manifests, the CHANGELOG heading and the git tag are kept identical — the release workflow fails if they disagree.

## Resources

- [Google Search Central](https://developers.google.com/search)
- [SEO Starter Guide](https://developers.google.com/search/docs/fundamentals/seo-starter-guide)
- [Web.dev - Core Web Vitals](https://web.dev/vitals/)
- [Schema.org](https://schema.org/)

## Contributing

Pull requests and issue reports are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) — in particular, the English and Japanese versions must be kept in sync (English is the source of truth).

## License

MIT License
