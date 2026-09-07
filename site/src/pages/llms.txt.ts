import type { APIRoute } from 'astro';
import { site, installCmd, marketplaceCmd } from '../data/site';

/**
 * llms.txt は仕様として確立したものではない。サイトの要約を 1 か所に置くだけの、
 * 低コストな任意対応として出している。robots.txt や sitemap の代わりにはならない。
 */
const body = `# ${site.name}

> A Markdown-only Agent Skill that gives Claude Code and Codex reproducible SEO judgement:
> technical SEO, structured data (JSON-LD), Core Web Vitals, E-E-A-T, AI search,
> Astro and Cloudflare edge SEO, and site audits. English and Japanese.

- Version: ${site.version} (last_verified ${site.lastVerified})
- License: MIT
- Repository: ${site.repo}
- Author: ${site.author} (${site.authorUrl})

## Install

\`\`\`
${marketplaceCmd}
${installCmd}
\`\`\`

## Pages

- [English](${site.origin}/): overview, coverage, install, freshness policy, FAQ
- [日本語](${site.origin}/ja): 同じ内容の日本語版
- [Releases](${site.origin}/releases): what changed in each version, newest first
- [お知らせ](${site.origin}/ja/releases): 各バージョンの変更点（日本語）

## Reference files (per skill)

technical-seo.md, content-seo.md, structured-data.md, core-web-vitals.md,
ai-search.md, astro-seo.md, edge-seo.md, audit-workflow.md

## Notes

- The skill does not guarantee rankings or AI citations. GEO / LLMO / AEO are working
  terms; generative-visibility recommendations are labelled High / Medium / Experimental.
- Every reference file carries a \`last_verified\` date enforced by CI.
`;

export const GET: APIRoute = () =>
  new Response(body, { headers: { 'content-type': 'text/plain; charset=utf-8' } });
