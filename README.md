# SEO Mastery Agent Skills

Comprehensive SEO optimization Agent Skills for Claude/Codex. Based on Google's official documentation, providing integrated support for technical SEO, content SEO, structured data, Core Web Vitals, and site audits.

[日本語版 README はこちら](docs/README.ja.md)

## Features

- **Technical SEO Checklist** - robots.txt, sitemap, canonical, hreflang, etc.
- **Content SEO Optimization** - Meta tags, heading structure, E-E-A-T strategies
- **Structured Data Templates** - Article, FAQ, Product, LocalBusiness, etc.
- **Core Web Vitals Support** - Detailed optimization techniques for LCP, INP, CLS
- **Site Audit Workflow** - Systematic audit process and report formats
- **Practical Code Examples** - Ready-to-use templates

## Installation

### Claude Code / Claude.ai

```bash
# Install English version
mkdir -p .claude/skills/seo-mastery
curl -o .claude/skills/seo-mastery/SKILL.md https://raw.githubusercontent.com/kpab/seo-mastery-agent-skills/main/.claude/skills/seo-mastery/SKILL.md

# Install Japanese version
mkdir -p .claude/skills/seo-mastery-jp
curl -o .claude/skills/seo-mastery-jp/SKILL.md https://raw.githubusercontent.com/kpab/seo-mastery-agent-skills/main/.claude/skills/seo-mastery-jp/SKILL.md
```

### Codex

```bash
# Project local (English)
mkdir -p .codex/skills/seo-mastery
curl -o .codex/skills/seo-mastery/SKILL.md https://raw.githubusercontent.com/kpab/seo-mastery-agent-skills/main/.claude/skills/seo-mastery/SKILL.md

# Project local (Japanese)
mkdir -p .codex/skills/seo-mastery-jp
curl -o .codex/skills/seo-mastery-jp/SKILL.md https://raw.githubusercontent.com/kpab/seo-mastery-agent-skills/main/.claude/skills/seo-mastery-jp/SKILL.md

# User global
mkdir -p ~/.codex/skills/seo-mastery
curl -o ~/.codex/skills/seo-mastery/SKILL.md https://raw.githubusercontent.com/kpab/seo-mastery-agent-skills/main/.claude/skills/seo-mastery/SKILL.md
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
│   └── audit-workflow.md     # Audit workflow details
└── seo-mastery-jp/           # Japanese version
    ├── SKILL.md              # Main skill file
    ├── technical-seo.md      # Technical SEO details
    ├── content-seo.md        # Content SEO details
    ├── structured-data.md    # Structured data details
    ├── core-web-vitals.md    # Core Web Vitals details
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
- FAQ (Frequently Asked Questions)
- HowTo
- Product
- LocalBusiness
- BreadcrumbList
- VideoObject
- Organization / WebSite
- Event

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

Pull requests and issue reports are welcome!

## License

MIT License
