# SEO Mastery Agent Skills

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Agent%20Skill-7C3AED)](https://docs.claude.com/en/docs/claude-code/overview)
[![Languages: EN | JP](https://img.shields.io/badge/Languages-EN%20%7C%20JP-success)](docs/README.ja.md)

Comprehensive SEO optimization Agent Skills for Claude Code & Codex. Based on Google's official documentation, providing integrated support for technical SEO, content SEO, structured data, Core Web Vitals, E-E-A-T, and site audits.

[日本語版 README はこちら](docs/README.ja.md)

## Features

- **Technical SEO Checklist** - robots.txt, sitemap, canonical, hreflang, etc.
- **Content SEO Optimization** - Meta tags, heading structure, E-E-A-T strategies
- **Structured Data Templates** - Article, FAQ, Product, LocalBusiness, etc.
- **Core Web Vitals Support** - Detailed optimization techniques for LCP, INP, CLS
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
for f in SKILL.md technical-seo.md content-seo.md structured-data.md core-web-vitals.md ai-search.md audit-workflow.md; do
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
for f in SKILL.md technical-seo.md content-seo.md structured-data.md core-web-vitals.md ai-search.md audit-workflow.md; do
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
│   └── audit-workflow.md     # Audit workflow details
└── seo-mastery-jp/           # Japanese version
    ├── SKILL.md              # Main skill file
    ├── technical-seo.md      # Technical SEO details
    ├── content-seo.md        # Content SEO details
    ├── structured-data.md    # Structured data details
    ├── core-web-vitals.md    # Core Web Vitals details
    ├── ai-search.md          # AI search details
    └── audit-workflow.md     # Audit workflow details
```

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

- Next.js
- Nuxt.js
- Static HTML
- WordPress (reference)

## Resources

- [Google Search Central](https://developers.google.com/search)
- [SEO Starter Guide](https://developers.google.com/search/docs/fundamentals/seo-starter-guide)
- [Web.dev - Core Web Vitals](https://web.dev/vitals/)
- [Schema.org](https://schema.org/)

## Contributing

Pull requests and issue reports are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) — in particular, the English and Japanese versions must be kept in sync (English is the source of truth).

## License

MIT License
