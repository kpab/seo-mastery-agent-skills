# Changelog

All notable changes to the `seo-mastery` and `seo-mastery-jp` skills are documented here. Both skills share version numbers.

## v1.2.1 (2026-08) - FAQ rich results retirement

- Updated FAQ rich results guidance: Google retired FAQ rich results entirely on May 7, 2026 (documentation and Search Console reports removed); FAQPage markup is now documented as semantic-only, matching the HowTo treatment (#4)
- Added an audit checklist item to detect markup for deprecated rich results (FAQ, HowTo, Sitelinks Search Box) and propose removal or annotation
- Replaced the FAQ structured data example in the competitive gap analysis template with video structured data

## v1.2.0 (2026-07) - Content freshness, restructure, and tooling

- Updated stale Google Search guidance: replaced the retired Mobile-Friendly Test with Lighthouse-based checks; noted that FAQ rich results are restricted and HowTo rich results were discontinued (2023)
- Added explicit "use when" invocation triggers to both skill descriptions
- Restructured SKILL.md as a lightweight overview + navigation layer; templates and detailed procedures now live only in the reference files
- Added CONTRIBUTING.md with the EN/JP synchronization policy (English is the source of truth)
- Added CI (GitHub Actions) validating frontmatter, JSON-LD template syntax, manifests, and EN/JP structural sync
- Added official Claude Code plugin marketplace support (`claude plugin marketplace add kpab/seo-mastery-agent-skills`)

## v1.1.0 (2026-06) - Security hardening

- Added "Handling Untrusted External Content" guidance to mitigate indirect prompt injection from fetched pages
- Fetched content is now treated as untrusted data with explicit boundary markers

## v1.0.0 (2025-01) - Initial release

- Created based on Google's official SEO guides
- Comprehensive technical SEO, content SEO, structured data coverage
- Core Web Vitals (2024 INP-compliant version)
- E-E-A-T optimization checklist added
- Site audit workflow added
