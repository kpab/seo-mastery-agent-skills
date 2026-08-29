---
last_verified: 2026-08-29
---

# Edge SEO Reference (Cloudflare Workers / Pages)

SEO work that happens at the edge rather than in the application: redirects, response headers,
dynamically generated sitemaps, crawler handling, and last-mile HTML rewriting. Written for
Cloudflare Workers and Cloudflare Pages, but the reasoning transfers to any edge runtime.

Verified against Cloudflare's documentation on 2026-08-29. The `_redirects` and `_headers` files
behave identically on Workers with static assets and on Pages; where behaviour diverges it is called
out.

## The platform model

Two request paths exist, and almost every edge SEO bug comes from confusing them:

| Path | Serves | `_redirects` applies | `_headers` applies |
|------|--------|----------------------|--------------------|
| **Static assets** | Files uploaded from your build output directory | Yes | Yes |
| **Worker code / Pages Functions** | Responses your code returns (SSR, API routes) | **No** | **No** |

Cloudflare states this plainly: redirects "are not applied to requests served by your Worker code,
even if the request URL matches a rule," and custom headers "are not applied to responses generated
by your Worker code." A hybrid site — static marketing pages plus an SSR blog — therefore needs its
redirect and header logic implemented **twice**, or implemented once in Worker code.

Configuration lives under `assets` in `wrangler.jsonc`:

```jsonc
{
  "name": "example-site",
  "main": "src/index.ts",
  "compatibility_date": "2026-08-01",
  "assets": {
    "directory": "./dist/",
    "binding": "ASSETS",
    "not_found_handling": "404-page",
    "run_worker_first": ["/api/*", "!/api/public/*"]
  }
}
```

`run_worker_first` accepts a boolean or an array of route patterns (`*` matches deeply, a leading `!`
negates). `.assetsignore` keeps `_worker.js`, `_redirects` and `_headers` from being uploaded as
public assets.

**This key decides whether your Worker sees the request at all.** By default Cloudflare serves a
matching static asset and only invokes the Worker when none matches. A Worker that rewrites or
inspects HTML — the HTMLRewriter and query-canonicalization patterns later in this file — is
therefore dead code under the config above, because `/blog/post/` matches an asset and never reaches
it. Middleware-style Workers need the HTML paths listed in `run_worker_first`:

```jsonc
{
  "assets": {
    "directory": "./dist/",
    "binding": "ASSETS",
    // Worker first for everything except fingerprinted assets, which should be
    // served straight from the edge.
    "run_worker_first": ["/*", "!/_astro/*", "!/assets/*"]
  }
}
```

The cost is the trade documented above: those paths no longer get `_headers` or `_redirects`, so the
Worker has to set headers and issue redirects itself. Pick per project — asset-first for a purely
static site, Worker-first when you genuinely need to transform HTML.

Two of these keys decide your canonical URL shape before any of your own redirects run:

| Key | Values | SEO effect |
|-----|--------|------------|
| `html_handling` | `auto-trailing-slash` (default), `force-trailing-slash`, `drop-trailing-slash`, `none` | Determines whether `/about` or `/about/` is the served URL and which one gets a 307. Pick the form your `<link rel="canonical">` and sitemap use — a mismatch means every page redirects on its way to being indexed |
| `not_found_handling` | `none` (default), `404-page`, `single-page-application` | `404-page` serves the nearest `404.html` with a real 404 status. `single-page-application` returns **200 with `index.html` for every unmatched path**, which turns typos and dead links into indexable soft 404s — acceptable for an app shell, harmful for content sites |

## Redirects

### The _redirects file

A plain text file in the static asset directory, one rule per line: `[source] [destination] [code?]`.
The status code **defaults to 302**, which is the single most common accidental SEO regression in
Cloudflare projects — a permanent move published as a temporary redirect. Always write the code.

```txt
# Permanent moves — always state 301 explicitly
/old-blog/*            /blog/:splat            301
/products/legacy-sku   /products/new-sku       301

# Locale consolidation with a placeholder (matches one path segment)
/en-us/:slug           /en/:slug               301

# Temporary: campaign page that will come back
/summer-sale           /promotions/            302

# Proxy (rewrite, URL unchanged) — relative destination, status 200
/docs/*                /documentation/:splat   200
```

Rules to keep in mind:

- **Placeholders** (`:name`) match everything except the delimiter, and the delimiter depends on
  position: in the **host** it is `.` or `/`, in the **path** it is only `/`. A path placeholder
  therefore **does match dots** — `/:slug` also matches `report.pdf`, so a rule intended for clean
  slugs will happily rewrite file URLs too.
- **Splats** (`*`) are greedy and only **one splat per URL** is allowed. Reference placeholders and
  splats as `:name` and `:splat` in the destination.
- Supported status codes: **301, 302, 303, 307, 308**. A `200` destination proxies instead of
  redirecting.
- **Not supported:** matching on query parameters, domain-level redirects, or conditional redirects
  by country, language or cookie. Those require Worker code (or Cloudflare Rules).

### Limits

| Limit | Value |
|-------|-------|
| Static redirects | 2,000 |
| Dynamic redirects (with `*` or `:name`) | 100 |
| Combined total | 2,100 |
| Characters per line | 1,000 |

Sites migrating a large legacy URL space hit the 100-dynamic-rule limit quickly. The fix is not more
rules — it is a Worker backed by KV, below.

### Redirects in Worker code

For anything the file format cannot express — query parameters, thousands of one-off legacy URLs,
conditional logic — do it in the Worker. Store the map in KV so redirects can be updated without a
deploy.

```js
// src/index.ts
export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    // 1. Exact legacy URL lookup (KV holds "/old/path" -> "/new/path")
    const target = await env.REDIRECTS.get(url.pathname);
    if (target) {
      return Response.redirect(new URL(target, url.origin).toString(), 301);
    }

    // 2. Query-parameter canonicalization: strip tracking params, 301 to the clean URL
    const TRACKING = ['utm_source', 'utm_medium', 'utm_campaign', 'fbclid', 'gclid'];
    if (TRACKING.some((p) => url.searchParams.has(p))) {
      TRACKING.forEach((p) => url.searchParams.delete(p));
      return Response.redirect(url.toString(), 301);
    }

    return env.ASSETS.fetch(request);
  },
};
```

Redirecting away tracking parameters is worth care: it breaks referral attribution for analytics that
read them client-side. Prefer `rel=canonical` for parameter duplication and reserve edge redirects
for parameters that genuinely produce distinct, low-value URLs (session IDs, sort orders).

### Redirect design rules

- **301 for permanent, 302 for temporary.** Google treats a long-lived 302 as a signal to keep the
  old URL indexed, which is rarely what you want.
- **One hop.** Chains dilute crawl efficiency and lose a little signal at every step. When you add a
  new redirect, check whether an existing rule already points at the old target and flatten it.
- **Redirect to the equivalent page, not the homepage.** Mass redirects to `/` are treated as soft
  404s.
- **Order matters.** Rules are evaluated top to bottom; the first match wins. Put specific rules
  above wildcards.
- **Keep the protocol and host canonical.** HTTP→HTTPS and www→apex (or the reverse) belong in
  Cloudflare Redirect Rules at the zone level, not in `_redirects`, which cannot do domain-level
  redirects.

## SEO headers with _headers

A rule block is a URL pattern followed by indented `Name: value` lines. Limits: **100 rules** and
**2,000 characters per line**. A leading `! ` removes a header.

One behaviour governs the whole file: **matching rules accumulate, they do not override.** Cloudflare
states that "if a header is applied twice in the `_headers` file, the values are joined with a comma
separator." A broad `/*` rule and a narrow `/_astro/*` rule that both set `Cache-Control` therefore
ship one nonsensical joined value, not the specific one. Keep each header name to a single matching
rule, or detach the inherited value with `! Header-Name` before setting your own.

```txt
# Keep staging and internal previews out of the index
/preview/*
  X-Robots-Tag: noindex, nofollow

# Non-HTML resources can only carry robots directives as a header
/reports/*.pdf
  X-Robots-Tag: noindex, nofollow

# Long-lived immutable build output. Cache-Control is set here and nowhere
# else that matches these paths.
/_astro/*
  Cache-Control: public, max-age=31536000, immutable

/*
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
```

Note what is deliberately absent: a `Cache-Control` rule for HTML. Under the default
`auto-trailing-slash`, pages are served at extensionless URLs, so a `/*.html` pattern matches
nothing useful — and a `/*` rule would collide with the asset rule above. Set HTML caching with
Cloudflare Cache Rules at the zone level, or in Worker code for SSR routes.

### X-Robots-Tag

`X-Robots-Tag` is the only way to apply robots directives to non-HTML resources — PDFs, images,
JSON feeds — because they cannot carry a `<meta name="robots">` tag. It supports the same directives
as the meta tag (`noindex`, `nofollow`, `none`, `nosnippet`, `max-snippet:[n]`,
`max-image-preview:[setting]`, `max-video-preview:[n]`, `notranslate`, `noimageindex`,
`unavailable_after:[date]`, `indexifembedded`) and can target a specific crawler by prefixing the
user agent:

```txt
X-Robots-Tag: googlebot: nofollow
X-Robots-Tag: otherbot: noindex, nofollow
```

Directives without a user agent apply to all crawlers, and where rules conflict the **more
restrictive** one wins.

**Per-crawler rules do not survive `_headers`.** Google's per-user-agent form relies on *separate*
`X-Robots-Tag` header lines, but Cloudflare states that "if a header is applied twice in the
`_headers` file, the values are joined with a comma separator" — two lines ship as one combined
header, and Google does not document how it parses a combined value carrying user-agent prefixes.
If you need per-crawler directives, set the headers in Worker code, where you control each line.

Two further traps:

- A `noindex` header on a URL that is **also disallowed in robots.txt** never takes effect — the
  crawler cannot fetch the response to read the header. Choose one: block crawling, or allow
  crawling and send `noindex`.
- Applying `X-Robots-Tag: noindex` to `/*` on a preview deployment is correct; leaving it on when
  that deployment is promoted to production is catastrophic and silent. Gate it on the environment.

### Cache-Control

Cache headers are an SEO concern because they set the cost of crawling your site:

| Resource | Recommended | Why |
|----------|-------------|-----|
| Fingerprinted assets (`/_astro/*`, `/assets/*.[hash].js`) | `public, max-age=31536000, immutable` | Never revalidated; frees crawl and render budget |
| HTML | `public, max-age=0, must-revalidate` + a CDN cache with explicit purge | Content must be fresh, but the origin should not be hit per request |
| `sitemap.xml`, `robots.txt` | `public, max-age=3600` | Frequently fetched by crawlers; hourly is fresh enough |

Use `stale-while-revalidate` on HTML when the origin is slow: crawlers get a fast response (helping
the crawl rate Google is willing to spend) while the edge refreshes in the background.

### The Worker code gap

Because `_headers` does not apply to Worker-generated responses, SSR pages need headers set in code:

```js
const response = await renderPage(request);
const headers = new Headers(response.headers);
headers.set('X-Robots-Tag', env.ENVIRONMENT === 'production' ? 'all' : 'noindex, nofollow');
headers.set('Cache-Control', 'public, max-age=0, must-revalidate');
return new Response(response.body, { status: response.status, headers });
```

Auditing for this is straightforward: `curl -I` a static URL and an SSR URL and compare. If the
headers differ, you have found the gap.

## Dynamic sitemaps from D1 and KV

A sitemap generated at the edge is always current, which matters when content changes faster than the
build. Two constraints from Google apply regardless of how you generate it: **50,000 URLs and 50 MB
uncompressed per sitemap file**, and `lastmod` is only used if it is verifiably accurate.

### Generating from D1

```js
// src/sitemap.ts
export const PAGE_SIZE = 25000;   // well under the 50,000 URL limit

export async function sitemapForPage(env, page) {
  const { results } = await env.DB.prepare(
    `SELECT slug, updated_at FROM posts
      WHERE published = 1
      ORDER BY updated_at DESC
      LIMIT ?1 OFFSET ?2`
  ).bind(PAGE_SIZE, page * PAGE_SIZE).all();

  const urls = results
    .map((row) => {
      // A NULL or unparseable timestamp would make toISOString() throw and take
      // the whole sitemap down with it. Omit lastmod instead — it is optional,
      // and Google only trusts it when it is consistently accurate anyway.
      const lastmod = isoOrNull(row.updated_at);
      return (
        `  <url>\n` +
        `    <loc>${escapeXml(locFor(row.slug))}</loc>\n` +
        (lastmod ? `    <lastmod>${lastmod}</lastmod>\n` : '') +
        `  </url>`
      );
    })
    .join('\n');

  return `<?xml version="1.0" encoding="UTF-8"?>\n` +
    `<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${urls}\n</urlset>`;
}

export async function pageCount(env) {
  const { results } = await env.DB.prepare(
    'SELECT COUNT(*) AS n FROM posts WHERE published = 1'
  ).all();
  return Math.ceil(results[0].n / PAGE_SIZE);
}

function locFor(slug) {
  // The spec wants the URL percent-encoded first and entity-escaped second.
  // encodeURIComponent leaves path-safe characters alone and handles the two
  // things that actually break <loc>: spaces and non-ASCII.
  return `https://example.com/blog/${encodeURIComponent(slug)}/`;
}

function isoOrNull(value) {
  if (value == null) return null;
  // SQLite commonly stores "2026-08-01 12:00:00"; the space form is not ISO 8601
  // and its parsing is engine-dependent, so normalise it first.
  const normalised = typeof value === 'string' ? value.trim().replace(' ', 'T') : value;
  const date = new Date(normalised);
  return Number.isNaN(date.getTime()) ? null : date.toISOString();
}

function escapeXml(value) {
  const ENTITIES = { '<': '&lt;', '>': '&gt;', '&': '&amp;', "'": '&apos;', '"': '&quot;' };
  let out = '';
  for (const ch of String(value)) {
    const code = ch.codePointAt(0);
    // Control characters are illegal in XML and cannot be escaped, only dropped.
    // Tab (0x09), LF (0x0a) and CR (0x0d) are the exceptions.
    if (code < 0x20 && code !== 0x09 && code !== 0x0a && code !== 0x0d) continue;
    out += ENTITIES[ch] ?? ch;
  }
  return out;
}
```

Escaping is not optional. A slug containing `&` produces malformed XML, and Search Console reports
the whole sitemap as unreadable — one bad row costs you the entire file. Note the order for `<loc>`:
the sitemap spec wants the URL percent-encoded *first* and entity-escaped second, which is why
`locFor()` runs `encodeURIComponent()` on the slug and hands the finished URL to `escapeXml()`.

### Sitemap index and caching

Serve an index that points at the paginated files, and cache both at the edge so a crawler fetching
50 sitemap files does not run 50 database queries.

```js
// src/index.js
import { sitemapForPage, pageCount } from './sitemap.js';

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const cache = caches.default;

    const cached = await cache.match(request);
    if (cached) return cached;

    let body;
    if (url.pathname === '/sitemap-index.xml') {
      const pages = await pageCount(env);
      // Zero pages means zero URLs, and there is no valid empty sitemap:
      // <sitemapindex> needs a child and <urlset> needs a <url>. Padding the
      // count to 1 only moves the invalid document one level down, so serve
      // nothing. List your static routes here too and the case cannot arise.
      if (pages === 0) return new Response('Not found', { status: 404 });
      body =
        `<?xml version="1.0" encoding="UTF-8"?>\n` +
        `<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n` +
        Array.from({ length: pages }, (_, i) =>
          `  <sitemap><loc>https://example.com/sitemap-${i}.xml</loc></sitemap>`
        ).join('\n') +
        `\n</sitemapindex>`;
    } else {
      const match = url.pathname.match(/^\/sitemap-(\d+)\.xml$/);
      if (!match) return env.ASSETS.fetch(request);
      const page = Number(match[1]);
      // Bound the page against the real count. Unbounded, /sitemap-999999.xml
      // answers 200 with an empty <urlset>: an infinite space of indexable
      // URLs — the crawler trap this file warns about below — backed by an
      // unbounded D1 OFFSET scan on every request.
      if (page >= (await pageCount(env))) {
        return new Response('Not found', { status: 404 });
      }
      body = await sitemapForPage(env, page);
    }

    const response = new Response(body, {
      headers: {
        'Content-Type': 'application/xml; charset=utf-8',
        'Cache-Control': 'public, max-age=3600',
      },
    });
    ctx.waitUntil(cache.put(request, response.clone()));
    return response;
  },
};
```

Reference the index from `robots.txt` (`Sitemap: https://example.com/sitemap-index.xml`). Sitemaps
listed in an index must sit in the same directory as the index or lower, so keep them at the root.

For a KV-backed variant, store the rendered XML under a key and rebuild it from a Cron Trigger
instead of per request — cheaper and more predictable than querying on the crawler's schedule.

## Bot handling at the edge

The edge is the right place to shape crawler traffic and the easiest place to accidentally
de-index yourself. The governing rule: **never block a crawler on user agent alone.** The user agent
string is trivially forged, so a UA-based allow-list blocks impostors and a UA-based block list
blocks nothing.

### Verifying Google crawlers

Google publishes two verification methods. At the edge, IP range matching is the practical one.

```js
// Fetch and cache Google's published ranges, then match the connecting IP.
// New location as of 2026-03-31; googlebot.json was renamed to common-crawlers.json.
const RANGE_FILES = [
  'https://developers.google.com/static/crawling/ipranges/common-crawlers.json',
  'https://developers.google.com/static/crawling/ipranges/special-crawlers.json',
  'https://developers.google.com/static/crawling/ipranges/user-triggered-fetchers.json',
];

async function googleRanges(env) {
  const cached = await env.BOT_KV.get('google-ranges', 'json');
  // An empty array is truthy: without the length check, one failed refresh
  // would poison the cache for 24 hours and reject every real crawler.
  if (Array.isArray(cached) && cached.length) return cached;

  // Negative cache. Without it, every request during an outage re-issues three
  // fetches, so a flood of spoofed-UA requests becomes an outbound fetch storm
  // against Google and burns the Worker's subrequest budget.
  if (await env.BOT_KV.get('google-ranges-failed')) {
    throw new Error('range lookup failed recently; backing off');
  }

  try {
    const files = await Promise.all(
      RANGE_FILES.map(async (u) => {
        const res = await fetch(u, { cf: { cacheTtl: 3600 } });
        if (!res.ok) throw new Error(`${u} -> ${res.status}`);
        return res.json();
      })
    );
    const prefixes = files.flatMap((f) => f.prefixes ?? []);
    if (!prefixes.length) throw new Error('no prefixes in Google range files');
    await env.BOT_KV.put('google-ranges', JSON.stringify(prefixes), { expirationTtl: 86400 });
    return prefixes;
  } catch (err) {
    await env.BOT_KV.put('google-ranges-failed', '1', { expirationTtl: 300 });
    throw err;
  }
}

async function isVerifiedGoogle(request, env) {
  const ua = request.headers.get('user-agent') ?? '';
  if (!/Googlebot|Google-InspectionTool|Storebot-Google/i.test(ua)) return false;

  const ip = request.headers.get('cf-connecting-ip');
  if (!ip) return false;

  let prefixes;
  try {
    prefixes = await googleRanges(env);
  } catch (err) {
    // Fail OPEN *only because this function gates rate limits*. During an
    // outage every spoofed Googlebot UA is treated as verified, which is the
    // UA-only trust this file forbids — acceptable when the cost is a skipped
    // rate limit, never when the check gates content or access. Fail closed
    // there, and let the negative cache above bound the retry rate.
    console.error('crawler range lookup failed', err);
    return true;
  }

  const wantV6 = ip.includes(':');
  return prefixes.some((p) => {
    const cidr = wantV6 ? p.ipv6Prefix : p.ipv4Prefix;
    return cidr ? ipInCidr(ip, cidr) : false;
  });
}
```

`ipInCidr` is yours to provide. IPv4 fits in a few lines; IPv6 needs BigInt because the address does
not fit in a 32-bit integer:

```js
// Returns null for anything unparseable. Never throws: this runs inside
// isVerifiedGoogle's prefix loop, which sits OUTSIDE its try/catch, so an
// exception here would 5xx the one client the check exists to identify.
function ipToBigInt(ip) {
  if (ip.includes(':')) {
    const parts = ip.split('::');
    if (parts.length > 2) return null;            // "::" may appear once
    const [head, tail = ''] = parts;
    const left = head ? head.split(':') : [];
    const right = tail ? tail.split(':') : [];

    // An IPv4-mapped address ends in a dotted quad ("::ffff:192.0.2.1").
    // parseInt('192.0.2.1', 16) silently returns 402, so expand the quad into
    // two 16-bit groups rather than letting that value through.
    const tailGroups = right.length ? right : left;
    const last = tailGroups[tailGroups.length - 1];
    if (last && last.includes('.')) {
      const octets = last.split('.').map(Number);
      if (octets.length !== 4) return null;
      if (octets.some((n) => !Number.isInteger(n) || n < 0 || n > 255)) return null;
      tailGroups.splice(-1, 1,
        ((octets[0] << 8) | octets[1]).toString(16),
        ((octets[2] << 8) | octets[3]).toString(16));
    }

    const fill = 8 - left.length - right.length;
    if (fill < 0 || (fill > 0 && parts.length !== 2)) return null;
    const groups = [...left, ...Array(fill).fill('0'), ...right];

    let acc = 0n;
    for (const g of groups) {
      // BigInt(NaN) throws a RangeError, so reject the group instead.
      if (!/^[0-9a-f]{1,4}$/i.test(g || '0')) return null;
      acc = (acc << 16n) | BigInt(parseInt(g || '0', 16));
    }
    return acc;
  }

  const octets = ip.split('.');
  if (octets.length !== 4) return null;
  let acc = 0n;
  for (const o of octets) {
    if (!/^\d{1,3}$/.test(o) || Number(o) > 255) return null;
    acc = (acc << 8n) | BigInt(Number(o));
  }
  return acc;
}

function ipInCidr(ip, cidr) {
  const [network, bitsRaw] = cidr.split('/');
  if (!network || !/^\d{1,3}$/.test(bitsRaw ?? '')) return false;
  if (ip.includes(':') !== network.includes(':')) return false;   // family mismatch

  const width = network.includes(':') ? 128n : 32n;
  const bits = BigInt(bitsRaw);
  if (bits > width) return false;

  const addr = ipToBigInt(ip);
  const net = ipToBigInt(network);
  if (addr === null || net === null) return false;

  const mask = bits === 0n ? 0n : (~0n << (width - bits)) & ((1n << width) - 1n);
  return (addr & mask) === (net & mask);
}
```

Cloudflare's own bot detection already does this work, so on paid plans prefer the Verified Bots
signal over rolling your own. The code above is for cases where you need the check in Worker logic.

The published files are `common-crawlers.json` (Googlebot and friends), `special-crawlers.json`
(AdsBot etc.), `user-triggered-fetchers.json`, `user-triggered-fetchers-google.json` and
`user-triggered-agents.json`; addresses are CIDR. Google IPs outside these categories are listed at
`https://www.gstatic.com/ipranges/goog.json`. The alternative method is reverse DNS — the PTR record
must resolve to `googlebot.com`, `google.com` or `googleusercontent.com`, and a forward lookup of
that name must return the original IP.

Cloudflare also maintains a **Verified Bots** program and supports **Web Bot Auth**, where an agent
signs its requests (`Signature`, `Signature-Input`, `Signature-Agent` headers, Ed25519 keys). Where
available, a cryptographic signature is a stronger check than any IP list.

### AI crawlers

AI crawler policy is a business decision made in robots.txt (see `ai-search.md`); the edge is where
it is *enforced*, since robots.txt is voluntary. Cloudflare's **AI Crawl Control** (formerly AI
Audit) reports which AI services fetch a site and provides per-crawler allow/block rules, robots.txt
compliance tracking, and a pay-per-crawl model in private beta; it is available on all plans.

Before blocking, separate the two questions from `ai-search.md` — "may my content train models?"
versus "may AI search cite and link to me?" — because blocking the second at the edge removes
referral traffic that robots.txt alone would not have cost you.

### Avoiding false blocks

Over-aggressive edge protection de-indexes sites quietly. Guard against it:

- **Never challenge or rate-limit verified search crawlers.** A CAPTCHA served to Googlebot is an
  unindexable page.
- **Return 503, not 403, for temporary blocks.** A 503 with `Retry-After` tells a crawler to come
  back; a 403 or 404 tells it the page is gone and eventually drops it from the index.
- **Do not serve different HTML to crawlers.** Adjusting rate limits by verified identity is fine;
  changing content by user agent is cloaking.
- **Watch for geo-blocking.** Googlebot crawls predominantly from US IP addresses. A country block
  that excludes the US blocks Google.
- **Test after every WAF change.** Fetch a page with `curl -A "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"`
  and confirm a 200 with full HTML, then confirm in Search Console's URL Inspection that Google
  agrees.

## Rewriting metadata with HTMLRewriter

`HTMLRewriter` transforms HTML as it streams through the Worker, without buffering the document. It
is the right tool for last-mile metadata fixes on HTML you do not control — a legacy origin, a CMS
you cannot modify, an A/B tested title.

### Rewriting titles and meta tags

```js
class MetaRewriter {
  constructor(meta) {
    this.meta = meta;
  }

  element(element) {
    // A throwing handler aborts parsing and errors the response body, turning a
    // metadata tweak into a 5xx. Never let one escape.
    try {
      if (element.tagName === 'title') {
        if (this.meta.title) element.setInnerContent(this.meta.title);
        return;
      }
      const name = element.getAttribute('name') ?? element.getAttribute('property');
      if (name === 'description' && this.meta.description) {
        element.setAttribute('content', this.meta.description);
      }
      if (name === 'og:title' && this.meta.title) {
        element.setAttribute('content', this.meta.title);
      }
    } catch (err) {
      console.error('meta rewrite failed', err);
    }
  }
}

export default {
  async fetch(request, env) {
    const response = await env.ASSETS.fetch(request);
    if (!response.headers.get('content-type')?.includes('text/html')) return response;

    const meta = await env.META.get(new URL(request.url).pathname, 'json');
    if (!meta) return response;

    const rewriter = new MetaRewriter(meta);
    return new HTMLRewriter()
      // `head > title`, not `title`: a bare selector also matches <title>
      // inside inline SVG, which would rewrite an icon's tooltip.
      .on('head > title', rewriter)
      .on('head > meta', rewriter)
      .transform(response);
  },
};
```

Two things this does **not** do. It only edits tags that already exist — HTMLRewriter streams, so
adding a missing `<meta name="description">` means appending to `head` instead (next section). And it
requires the Worker to see the request at all, which means the HTML paths must be in
`run_worker_first`.

### Injecting structured data

Appending to `<head>` is the safe way to add JSON-LD — it never disturbs existing markup:

```js
class JsonLdInjector {
  constructor(data) {
    this.payload = JSON.stringify(data).replace(/</g, '\\u003c');
  }
  element(head) {
    head.append(
      `<script type="application/ld+json">${this.payload}</script>`,
      { html: true }
    );
  }
}

// new HTMLRewriter().on('head', new JsonLdInjector(graph)).transform(response)
```

Unicode-escaping `<` prevents a value containing `</script>` from terminating the tag early —
the same precaution as in server-side templates.

### Caveats

- **Text arrives in chunks.** Cloudflare warns that "text chunks are not the same thing as text
  nodes": a single text node may be delivered across several `text()` calls. Accumulate until
  `lastInTextNode` is true before inspecting the whole string.
- **A throwing handler kills the response.** An exception halts parsing and errors the response body,
  turning a metadata tweak into a 5xx. Wrap handler bodies in `try/catch`.
- **Only rewrite HTML.** Check `content-type` first; running the rewriter over JSON or XML wastes CPU
  and can corrupt output.
- **Rewriting is not a fix.** Metadata patched at the edge is invisible to everyone reading the
  repository. Treat HTMLRewriter as a bridge while the origin is corrected, and record why it exists.

## Edge cache and crawl budget

Crawl budget is a function of how much a crawler *wants* to fetch and how much your site *lets* it
fetch without straining. Google reduces crawl rate when responses slow down or error; a healthy edge
cache raises the ceiling.

What actually helps:

- **Serve crawlers from cache.** A high edge hit ratio keeps TTFB low and steady, which is what
  Google's crawl rate heuristics respond to.
- **Fix 5xx immediately.** Sustained server errors cause Google to back off crawling site-wide, not
  just on the failing URLs.
- **Stop crawlers wandering into infinite URL spaces.** Faceted navigation, calendars and sort
  parameters generate unbounded URLs. Block the patterns in robots.txt (crawl-level) rather than
  handling them at the edge (which still costs a fetch).
- **Return 304 where you can.** Honouring `If-Modified-Since` / `If-None-Match` lets a crawler
  revalidate cheaply.
- **Use 410 for permanently removed content.** It states the intent precisely. Google does not
  document a processing-speed advantage over 404, so choose it for correctness, not for speed.
- **Keep `lastmod` honest in the sitemap.** Google uses it only when it is consistently accurate;
  stamping every URL with today's date trains it to ignore the field.

Crawl budget is only a real constraint for large sites (roughly: more URLs than a crawler can fetch
in a few days). For a site of a few thousand pages, spend the effort on content and internal linking
instead.

## Edge SEO checklist

- [ ] Every `_redirects` rule states its status code explicitly (the default is 302)
- [ ] No redirect chains; rules are ordered specific → wildcard
- [ ] Redirect count is within 2,000 static / 100 dynamic, or moved into a KV-backed Worker
- [ ] HTTP→HTTPS and host canonicalization are handled at the zone level, not in `_redirects`
- [ ] SSR routes set `X-Robots-Tag` and `Cache-Control` in code — `_headers` does not reach them
- [ ] `X-Robots-Tag: noindex` is never applied to a URL that is also disallowed in robots.txt
- [ ] Preview/staging `noindex` is gated on an environment variable, not hardcoded
- [ ] Fingerprinted assets are `immutable`; HTML revalidates; sitemap/robots cache for ~1 hour
- [ ] Dynamic sitemaps XML-escape every field and stay under 50,000 URLs / 50 MB per file
- [ ] Sitemap responses are edge-cached so a crawl does not become a database load test
- [ ] Crawler identity is verified by IP range (or Web Bot Auth), never by user agent alone
- [ ] Temporary blocks return 503 + `Retry-After`, never 403/404
- [ ] Verified search crawlers are exempt from WAF challenges and rate limits
- [ ] HTMLRewriter handlers check `content-type`, catch exceptions, and escape injected JSON-LD

## Official resources

- [Cloudflare Workers static assets](https://developers.cloudflare.com/workers/static-assets/)
- [Redirects (Workers)](https://developers.cloudflare.com/workers/static-assets/redirects/) / [Redirects (Pages)](https://developers.cloudflare.com/pages/configuration/redirects/)
- [Headers (Workers)](https://developers.cloudflare.com/workers/static-assets/headers/) / [Headers (Pages)](https://developers.cloudflare.com/pages/configuration/headers/)
- [HTMLRewriter](https://developers.cloudflare.com/workers/runtime-apis/html-rewriter/)
- [Verified bots](https://developers.cloudflare.com/bots/concepts/bot/verified-bots/) and [Web Bot Auth](https://developers.cloudflare.com/bots/reference/bot-verification/web-bot-auth/)
- [AI Crawl Control](https://developers.cloudflare.com/ai-crawl-control/)
- [Verifying Googlebot and other Google crawlers](https://developers.google.com/search/docs/crawling-indexing/verifying-googlebot)
- [X-Robots-Tag directives](https://developers.google.com/search/docs/crawling-indexing/robots-meta-tag)
- [Large sitemaps](https://developers.google.com/search/docs/crawling-indexing/sitemaps/large-sitemaps)
