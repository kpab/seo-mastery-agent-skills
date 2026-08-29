---
last_verified: 2026-08-30
---

# Astro SEO Reference

SEO patterns specific to Astro. Astro's defaults (zero JS by default, static HTML output) already
solve much of what other frameworks need plugins for — what remains are the decisions Astro makes
*you* responsible for: which islands hydrate, how absolute URLs are constructed at build time, and
how content metadata becomes structured data.

Verified against Astro 7 (released 2026-06-22). No API in this file changed in v7 — what changed is
the HTML Astro emits, covered in the migration section at the end. Where v5 and v6 differ, the v6
form is given first and the v5 form is noted.

## Islands Architecture and Core Web Vitals

Astro ships no client JavaScript unless you ask for it with a `client:*` directive. Every directive
you add is a deliberate INP and LCP cost, so directive choice *is* performance work.

### How client directives map to metrics

| Directive | Hydrates | Options | Metric impact |
|-----------|----------|---------|---------------|
| `client:load` | Immediately on page load, high priority | — | Worst case for INP and LCP: competes with the critical render path |
| `client:idle` | After load, when `requestIdleCallback` fires (falls back to the `load` event) | `timeout` (ms) | Keeps hydration out of the LCP window; still costs main-thread time later |
| `client:visible` | When the component enters the viewport (`IntersectionObserver`) | `rootMargin` | Best default for below-the-fold islands: zero cost until scrolled to |
| `client:media` | When a CSS media query matches | media query string | Useful for mobile-only or desktop-only UI |
| `client:only={"react"}` | Client only — no server render at all | framework name, `slot="fallback"` | **Content is invisible to crawlers before rendering.** Never use for indexable content |

`server:defer` is a different tool: it turns a component into a **server island**, rendered on demand
outside the main page render. Use it for personalized or slow fragments so the rest of the page can
be cached and served fast.

### Choosing a directive

Decide with two questions, in this order:

1. **Does a crawler need to see this content in the initial HTML?**
   If yes, it must be server-rendered — that means no `client:only`, and the island must render
   meaningful HTML on the server even before hydration.
2. **When does the user first interact with it?**
   Above the fold and immediately interactive → `client:load`. Above the fold but not urgent (a
   dropdown, a theme toggle) → `client:idle`. Below the fold → `client:visible`.

```astro
---
// src/pages/index.astro
import Hero from '../components/Hero.astro';           // no JS at all — the default
import SearchBox from '../components/SearchBox.jsx';
import CommentThread from '../components/CommentThread.jsx';
import ThemeToggle from '../components/ThemeToggle.jsx';
---
<Hero />                                  {/* static HTML, 0 KB JS */}
<SearchBox client:load />                 {/* above the fold, interacted with immediately */}
<ThemeToggle client:idle={{ timeout: 2000 }} />
<CommentThread client:visible={{ rootMargin: "200px" }} />
```

A common LCP regression: wrapping the hero in a framework component and adding `client:load` just to
animate it. The hero is the LCP element — keep it a plain `.astro` component and animate with CSS.

### Islands checklist

- [ ] No `client:only` on anything that must be indexed
- [ ] The LCP element is inside a static `.astro` component, not a hydrated island
- [ ] Below-the-fold islands use `client:visible`, not `client:load`
- [ ] Third-party widgets (chat, analytics) are islands with `client:idle`/`client:visible`, or loaded on first interaction
- [ ] `astro build` output was checked for unexpected client bundles

## Canonical URLs and Open Graph tags

Astro exposes two values you need for absolute URLs:

- `Astro.site` — the `site` value from `astro.config.mjs`. **Undefined if `site` is not set**, which
  silently produces relative or broken canonicals.
- `Astro.url` — the URL of the page being rendered.

Set `site` first; nothing else in this section works without it.

```js
// astro.config.mjs
import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://example.com',
  trailingSlash: 'always',   // pick one and keep links, canonicals and sitemap consistent
});
```

### The layout-level pattern

Generate canonical and OG tags once in a base layout so every page inherits them. Building the
canonical from `Astro.url.pathname` (not `Astro.url.href`) drops query strings and fragments, which
is almost always what you want.

```astro
---
// src/layouts/BaseLayout.astro
interface Props {
  title: string;
  description: string;
  image?: string;
  type?: 'website' | 'article';
  publishedTime?: Date;
  canonicalUrl?: string;
}

const { title, description, image, type = 'website', publishedTime, canonicalUrl } = Astro.props;

const canonical = canonicalUrl ?? new URL(Astro.url.pathname, Astro.site).href;
const ogImage = new URL(image ?? '/og-default.png', Astro.site).href;
---
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />

    <title>{title}</title>
    <meta name="description" content={description} />
    <link rel="canonical" href={canonical} />

    <meta property="og:type" content={type} />
    <meta property="og:title" content={title} />
    <meta property="og:description" content={description} />
    <meta property="og:url" content={canonical} />
    <meta property="og:image" content={ogImage} />
    {publishedTime && (
      <meta property="article:published_time" content={publishedTime.toISOString()} />
    )}

    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content={title} />
    <meta name="twitter:description" content={description} />
    <meta name="twitter:image" content={ogImage} />

    <slot name="head" />
  </head>
  <body><slot /></body>
</html>
```

OG images must be absolute URLs on an absolute host — `new URL(..., Astro.site)` guarantees that.
Relative OG image paths are the single most common broken-share-preview cause in Astro projects.

### getStaticPaths and Astro.site on Astro 6+

`getStaticPaths()` runs before a page has a request context. Since Astro 6, `Astro.site` inside
`getStaticPaths()` is **deprecated and logs a warning**; accessing any other `Astro` property there
throws. Use `import.meta.env.SITE`, which holds the same configured value.

```astro
---
// src/pages/blog/[...slug].astro
import { getCollection, render } from 'astro:content';
import BaseLayout from '../../layouts/BaseLayout.astro';

export async function getStaticPaths() {
  const posts = await getCollection('blog', ({ data }) => !data.draft);

  return posts.map((post) => ({
    params: { slug: post.id },
    props: {
      post,
      // Astro 6+: use import.meta.env.SITE here, NOT Astro.site
      shareUrl: new URL(`/blog/${post.id}/`, import.meta.env.SITE).href,
    },
  }));
}

const { post, shareUrl } = Astro.props;
const { Content } = await render(post);
---
<BaseLayout
  title={post.data.title}
  description={post.data.description}
  type="article"
  canonicalUrl={shareUrl}
>
  <Content />
</BaseLayout>
```

Pass the URL as a prop rather than emitting a second `og:url` through the `head` slot. The
slot renders *after* the layout's own tags, and every scraper takes the first `og:url` it
sees, so a slotted override is silently ignored while the page ships two conflicting tags.

### Trailing slashes

Astro's `trailingSlash` config, your internal links, your canonical tags and your sitemap must all
agree, or you publish two URLs for every page and let Google pick. Two Astro-specific traps:

- **Endpoints with a file extension.** Since Astro 6, routes such as `/sitemap.xml` or `/rss.xml`
  "can only be accessed without a trailing slash … regardless of your `build.trailingSlash`
  configuration." Link to them without a trailing slash.
- **The host also decides.** Static hosts often normalize trailing slashes themselves. Verify the
  deployed behaviour with `curl -I`, not the dev server.

## JSON-LD from Content Collections

Content Collections give you a Zod-validated schema for every entry. That schema is exactly the
contract structured data needs — generate JSON-LD from it and invalid structured data becomes a
build error instead of a Search Console error.

### Define the collection

Collections live in `src/content.config.ts` on Astro 6 and later (the legacy
`src/content/config.ts` location was removed) and require an explicit `loader`.

```ts
// src/content.config.ts
import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const blog = defineCollection({
  loader: glob({ base: './src/content/blog', pattern: '**/*.{md,mdx}' }),
  schema: ({ image }) =>
    z.object({
      title: z.string().max(110),           // editorial cap: Google sets no headline limit,
                                             // but "long titles may be truncated on some devices"
      description: z.string(),
      publishedAt: z.coerce.date(),
      updatedAt: z.coerce.date().optional(),
      cover: image(),                        // validated and optimizable
      author: z.object({
        name: z.string(),
        url: z.string().url().optional(),
      }),
      draft: z.boolean().default(false),
    }),
});

export const collections = { blog };
```

Putting your own editorial constraints in the schema (a headline cap, `.url()` on author links) means a
malformed post fails `astro build` rather than shipping broken markup.

### Generate the markup

Build the object in the frontmatter and serialize it with `set:html`. Astro does not escape inside a
`<script>` element, so escape the JSON yourself: a `</script>` sequence inside any string value would
otherwise terminate the script tag early. Replacing `<` with its unicode escape is enough and keeps
the JSON valid.

```astro
---
// src/components/ArticleJsonLd.astro
interface Props {
  post: import('astro:content').CollectionEntry<'blog'>;
}
const { post } = Astro.props;

const url = new URL(Astro.url.pathname, Astro.site).href;

const jsonLd = {
  '@context': 'https://schema.org',
  '@type': 'BlogPosting',
  headline: post.data.title,
  description: post.data.description,
  image: new URL(post.data.cover.src, Astro.site).href,
  datePublished: post.data.publishedAt.toISOString(),
  dateModified: (post.data.updatedAt ?? post.data.publishedAt).toISOString(),
  author: {
    '@type': 'Person',
    name: post.data.author.name,
    ...(post.data.author.url ? { url: post.data.author.url } : {}),
  },
  mainEntityOfPage: { '@type': 'WebPage', '@id': url },
};

// Escape `<` so a stray "</script>" in the content cannot break out of the tag.
const serialized = JSON.stringify(jsonLd).replace(/</g, '\\u003c');
---
<script type="application/ld+json" set:html={serialized} />
```

The rendered result is ordinary JSON-LD — the same markup documented in `structured-data.md`:

```json
{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "Optimizing Astro islands for INP",
  "description": "How client directive choice changes interaction latency.",
  "image": "https://example.com/_astro/cover.abc123.webp",
  "datePublished": "2026-08-01T09:00:00.000Z",
  "dateModified": "2026-08-20T11:30:00.000Z",
  "author": { "@type": "Person", "name": "Author Name", "url": "https://example.com/about/" },
  "mainEntityOfPage": { "@type": "WebPage", "@id": "https://example.com/blog/astro-inp/" }
}
```

### Site-wide graph

Organization, WebSite and BreadcrumbList belong in the base layout rather than per page. Combine
them with `@graph` and emit once, so pages carry only their own entity.

```astro
---
// src/components/SiteJsonLd.astro — rendered once in BaseLayout
// Fail loudly at build time rather than emitting "undefined" URLs. A non-null
// assertion (Astro.site!) would only silence TypeScript, not the real problem.
if (!Astro.site) throw new Error('astro.config.mjs is missing `site`; JSON-LD needs absolute URLs');
const site = Astro.site.href;

const graph = {
  '@context': 'https://schema.org',
  '@graph': [
    { '@type': 'Organization', '@id': `${site}#org`, name: 'Example Inc.', url: site,
      logo: new URL('/logo.png', site).href },
    { '@type': 'WebSite', '@id': `${site}#website`, url: site, name: 'Example',
      publisher: { '@id': `${site}#org` } },
  ],
};
---
<script type="application/ld+json" set:html={JSON.stringify(graph).replace(/</g, '\\u003c')} />
```

Do **not** add a `SearchAction` / Sitelinks Search Box to the `WebSite` node — that feature was
retired in November 2024. See `structured-data.md`.

## Sitemaps with @astrojs/sitemap

### Setup and options

`@astrojs/sitemap` requires `site`. It emits `sitemap-index.xml` plus numbered `sitemap-0.xml`
files, splitting at `entryLimit` (default 45,000 — below Google's hard limit of 50,000 URLs or 50 MB
uncompressed per file).

```js
// astro.config.mjs
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://example.com',
  integrations: [
    sitemap({
      filter: (page) =>
        !page.includes('/draft/') &&
        !page.includes('/thank-you/'),
      serialize(item) {
        if (item.url.endsWith('/blog/')) item.priority = 0.8;
        return item;
      },
      entryLimit: 10000,
    }),
  ],
});
```

Note that Google **ignores `<priority>` and `<changefreq>`** — setting them costs nothing but buys
nothing. `lastmod` is the field worth getting right, and only if it is genuinely accurate.

### Excluding pages properly

`filter` removes a URL from the sitemap; it does not stop the page being indexed. A page that should
not be in Search needs `noindex` as well, and a `noindex` page should not be in the sitemap —
listing it sends contradictory signals.

```astro
---
// src/pages/internal/preview.astro
import BaseLayout from '../../layouts/BaseLayout.astro';
---
<BaseLayout title="Internal preview" description="Not for search engines">
  <!-- Must land inside <head>: the BaseLayout above exposes a `head` slot for it -->
  <meta slot="head" name="robots" content="noindex, nofollow" />
  <p>…</p>
</BaseLayout>
```

### Multilingual sitemaps

The `i18n` option adds `<xhtml:link rel="alternate" hreflang="…">` entries for every translated page,
which is the sitemap-based hreflang implementation described in `technical-seo.md`.

```js
// astro.config.mjs
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://example.com',
  i18n: {
    defaultLocale: 'en',
    locales: ['en', 'ja', 'fr'],
  },
  integrations: [
    sitemap({
      i18n: {
        defaultLocale: 'en',
        locales: { en: 'en-US', ja: 'ja-JP', fr: 'fr-FR' },
      },
    }),
  ],
});
```

The keys in `sitemap.i18n.locales` must match the path segments Astro generates (`/ja/…`), and the
values are the hreflang codes emitted. Mismatched keys silently produce a sitemap with no alternates.

hreflang still requires **bidirectional** links: every language version must reference every other,
including itself. The integration handles this for pages it can see — pages added via `customPages`
are not translated automatically.

### robots.txt

Astro has no built-in robots.txt. Put a static file in `public/` and point it at the sitemap index:

```txt
User-agent: *
Allow: /

Sitemap: https://example.com/sitemap-index.xml
```

For AI crawler directives, see `ai-search.md`. If robots.txt must be generated (per-environment
rules, for example), an endpoint at `src/pages/robots.txt.ts` works — link to it without a trailing
slash on Astro 6 and later.

## View transitions and SEO

### Native transitions vs ClientRouter

Astro offers two mechanisms, and the SEO characteristics differ sharply:

1. **Native cross-document (MPA) view transitions** — CSS only. Every navigation is still a real
   document load. No JavaScript, no router, no SEO risk. Prefer this.
2. **`<ClientRouter />`** — converts the site into a client-routed app to enable `transition:persist`,
   shared state across navigations, and lifecycle hooks. Astro's own docs list the trade-off:
   "some drawbacks, such as needing to manually reinitialize scripts or state after navigation."

Crawlers see the server-rendered HTML either way, so ClientRouter does not hide content from Google.
The risk is on the client: analytics, structured data injected by scripts, and third-party widgets
that assume one page load per session.

```astro
---
// Add to the <head> of the BaseLayout above, if you want client routing.
// v6 name — on v5 this component was <ViewTransitions />, which is now removed.
import { ClientRouter } from 'astro:transitions';
---
<ClientRouter />
```

### Scripts and analytics after navigation

Astro documents that bundled module scripts "are only ever executed once. After initial execution
they will be ignored." A pageview call written as a top-level module script therefore fires once and
under-reports every subsequent navigation.

Two fixes, in order of preference:

```astro
<!-- Preferred: subscribe to the router's lifecycle event once -->
<script>
  document.addEventListener('astro:page-load', () => {
    window.gtag?.('event', 'page_view', {
      page_location: location.href,
      page_title: document.title,
    });
  });
</script>

<!-- Alternative: force an inline script to re-run on every navigation -->
<script is:inline data-astro-rerun>
  initThirdPartyWidget();
</script>
```

The lifecycle events fire in this order: `astro:before-preparation` → `astro:after-preparation` →
`astro:before-swap` → `astro:after-swap` → `astro:page-load`. Use `astro:page-load` for anything that
needs the new DOM in place.

### Accessibility, motion and persistence

- ClientRouter announces page title changes to assistive technology automatically — but only if each
  page actually sets a distinct `<title>`. Duplicate titles break both the announcement and your
  search snippets.
- `prefers-reduced-motion` is respected: animations are disabled for users who ask for it.
- Fallback behaviour in browsers without the View Transitions API is configurable as `animate`,
  `swap`, or `none`.
- `transition:persist` keeps an element (and its state) across navigations. Persisting an element
  that contains page-specific structured data or metadata will leave stale content in the DOM —
  persist players and sidebars, not content.

## Version migration notes that affect SEO

### Astro 7 (released 2026-06-22)

Astro 7 changes no API in this file. What it changes is the HTML those APIs emit, which matters more
to a crawler than a renamed import does.

| Change | SEO consequence |
|--------|-----------------|
| The Rust compiler is the default and only `.astro` compiler | "Unclosed tags now produce errors" and "semantically invalid HTML is no longer auto-corrected." The old compiler silently restructured invalid markup to match the HTML parsing specification; v7 passes your markup "through as-is", so a page that rendered cleanly on v6 can now ship the broken nesting you actually wrote. Most of it surfaces as a build error — re-check heading order and `<head>` contents on whatever still builds |
| `compressHTML` defaults to `'jsx'` instead of `true` | Whitespace between adjacent inline elements collapses: `<span>hello</span><em>world</em>` now renders as `helloworld`. Titles, headings and anchor text assembled from adjacent elements lose their word boundaries — and that is the text Google indexes. Insert an explicit `{" "}` wherever a space is meant |
| Markdown renders through Sätteri, not remark/rehype | `@astrojs/markdown-remark` is no longer installed by default, so a remark/rehype plugin doing SEO work — heading anchors, `rel` on external links, excerpt generation — stops running until you reinstall the package and configure `unified()` as the processor. Diff the generated heading IDs against your existing in-page anchors before shipping |
| `src/fetch.ts` is reserved for Advanced Routing | A standard fetch handler can now own the whole request pipeline. That is where redirects and response headers for SSR routes belong — the same gap `edge-seo.md` describes for Worker-generated responses |
| `astro:transitions` internals removed | The `TRANSITION_*` constants and helpers (`isTransitionBeforeSwapEvent()`, `createAnimationScope()`, …) are gone. The lifecycle *event names* are unaffected, so the `astro:page-load` analytics hook above still applies |

### Astro 6 (released 2026-03-10)

| Change | Action |
|--------|--------|
| `<ViewTransitions />` removed | Replace the import and component with `<ClientRouter />` from `astro:transitions` |
| `Astro.site` deprecated inside `getStaticPaths()` | Use `import.meta.env.SITE`; other `Astro` properties throw there |
| Endpoints with file extensions | Link to `/sitemap.xml`, `/rss.xml` etc. **without** a trailing slash |
| `src/content/config.ts` removed | Move to `src/content.config.ts` and give every collection a `loader` |
| Markdown heading IDs keep trailing hyphens | Re-check in-page anchors and any external links to `#fragment`s |
| Images never upscale; cropping is the default | Re-check hero art direction — a silently smaller LCP image changes the LCP candidate |

Astro 6 also adds a built-in **Fonts API** (self-hosting, caching, fallback metric generation and
preloading) and a **CSP API**. The Fonts API is directly useful for CLS: generated fallback metrics
reduce the layout shift when a web font swaps in.

## Astro SEO checklist

- [ ] `site` is set in `astro.config.mjs` (nothing below works without it)
- [ ] `trailingSlash`, internal links, canonicals and the sitemap all agree
- [ ] Canonical and OG tags are generated in one base layout from `Astro.url` + `Astro.site`
- [ ] OG image URLs are absolute
- [ ] No `client:only` on indexable content; LCP element is not inside a hydrated island
- [ ] Below-the-fold islands use `client:visible`
- [ ] JSON-LD is generated from the collection schema, with `<` unicode-escaped before `set:html`
- [ ] Organization/WebSite `@graph` is emitted once, without `SearchAction`
- [ ] `@astrojs/sitemap` is installed; drafts and utility pages are filtered out *and* `noindex`ed
- [ ] Multilingual sites configure `sitemap({ i18n })` with locale keys matching the route segments
- [ ] `robots.txt` in `public/` references `sitemap-index.xml`
- [ ] If ClientRouter is used: analytics hooks `astro:page-load`, and every page has a unique title
- [ ] On Astro 6+: no `Astro.site` inside `getStaticPaths()`, no `<ViewTransitions />`
- [ ] On Astro 7: the build clears the Rust compiler's HTML validation, and `compressHTML: 'jsx'` has not merged words in titles, headings or anchor text

## Official resources

- [Astro docs](https://docs.astro.build/)
- [Upgrade to Astro v7](https://docs.astro.build/en/guides/upgrade-to/v7/)
- [Upgrade to Astro v6](https://docs.astro.build/en/guides/upgrade-to/v6/)
- [Template directives reference](https://docs.astro.build/en/reference/directives-reference/)
- [View transitions](https://docs.astro.build/en/guides/view-transitions/)
- [Content collections](https://docs.astro.build/en/guides/content-collections/)
- [@astrojs/sitemap](https://docs.astro.build/en/guides/integrations-guide/sitemap/)
- [Astro 7.0 release notes](https://astro.build/blog/astro-7/)
- [Astro 6.0 release notes](https://astro.build/blog/astro-6/)
