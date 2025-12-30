# Technical SEO Reference

Detailed guide for technical SEO configuration. Covers crawlability, indexability, and rendering optimization.

## robots.txt

### Basic Syntax

```txt
# Apply to all crawlers
User-agent: *
Disallow: /admin/
Disallow: /private/
Allow: /admin/public/

# Apply only to Googlebot
User-agent: Googlebot
Disallow: /temp/

# Sitemap location
Sitemap: https://example.com/sitemap.xml
```

### Important Rules

1. **Disallow is NOT Index Control**
   - robots.txt only blocks crawling
   - Use `noindex` meta tag to exclude from index

2. **Path Specification Notes**
   ```txt
   Disallow: /admin   # Blocks /admin, /admin/, /admin123
   Disallow: /admin/  # Blocks only under /admin/
   ```

3. **Wildcard Usage**
   ```txt
   Disallow: /*.pdf$   # Block all PDFs
   Disallow: /*/temp/  # Block temp/ under any path
   ```

### Common Mistakes

```txt
# Mistake: Blocking entire site
User-agent: *
Disallow: /

# Mistake: Blocking important resources
Disallow: /css/
Disallow: /js/
Disallow: /images/

# Correct: Minimal blocking
User-agent: *
Disallow: /admin/
Disallow: /api/internal/
```

---

## XML Sitemap

### Basic Structure

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://example.com/</loc>
    <lastmod>2025-01-15</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://example.com/about/</loc>
    <lastmod>2025-01-10</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
</urlset>
```

### Sitemap Index (For Large Sites)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap>
    <loc>https://example.com/sitemap-posts.xml</loc>
    <lastmod>2025-01-15</lastmod>
  </sitemap>
  <sitemap>
    <loc>https://example.com/sitemap-products.xml</loc>
    <lastmod>2025-01-14</lastmod>
  </sitemap>
</sitemapindex>
```

### Best Practices

| Item | Recommendation |
|------|----------------|
| URL limit | 50,000 URLs per file |
| File size limit | 50MB (uncompressed) |
| lastmod | Accurate update datetime |
| priority | Relative importance (0.0-1.0) |
| Submission | Google Search Console |

---

## Canonical URL

### Implementation Methods

```html
<!-- Specify in HTML -->
<link rel="canonical" href="https://example.com/page/">

<!-- Specify in HTTP header (useful for PDFs) -->
Link: <https://example.com/page/>; rel="canonical"
```

### Use Cases

1. **URLs with Parameters**
   ```html
   <!-- https://example.com/product?color=red&size=L -->
   <link rel="canonical" href="https://example.com/product">
   ```

2. **www / non-www Unification**
   ```html
   <!-- Use consistently across all pages -->
   <link rel="canonical" href="https://www.example.com/page/">
   ```

3. **Pagination**
   ```html
   <!-- Each page has its own canonical -->
   <!-- For page 2 -->
   <link rel="canonical" href="https://example.com/articles?page=2">
   ```

4. **Separate Mobile/Desktop URLs**
   ```html
   <!-- Desktop version -->
   <link rel="canonical" href="https://example.com/page">
   <link rel="alternate" media="only screen and (max-width: 640px)" href="https://m.example.com/page">

   <!-- Mobile version -->
   <link rel="canonical" href="https://example.com/page">
   ```

### Notes

- Canonical is a "hint," not a directive
- Self-referencing canonical recommended
- Best combined with 301 redirects
- Use cross-domain canonicals carefully

---

## hreflang (Multilingual/Multi-regional)

### Basic Implementation

```html
<link rel="alternate" hreflang="en" href="https://example.com/en/">
<link rel="alternate" hreflang="en-US" href="https://example.com/en-us/">
<link rel="alternate" hreflang="en-GB" href="https://example.com/en-gb/">
<link rel="alternate" hreflang="es" href="https://example.com/es/">
<link rel="alternate" hreflang="x-default" href="https://example.com/">
```

### Language/Region Codes

| Code | Meaning |
|------|---------|
| en | English (no region) |
| en-US | American English |
| en-GB | British English |
| es | Spanish |
| zh-Hans | Simplified Chinese |
| zh-Hant | Traditional Chinese |
| x-default | Default / language selector |

### Sitemap Specification

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xhtml="http://www.w3.org/1999/xhtml">
  <url>
    <loc>https://example.com/en/</loc>
    <xhtml:link rel="alternate" hreflang="en" href="https://example.com/en/"/>
    <xhtml:link rel="alternate" hreflang="es" href="https://example.com/es/"/>
    <xhtml:link rel="alternate" hreflang="x-default" href="https://example.com/"/>
  </url>
</urlset>
```

### Important Rules

1. **Bidirectional Links Required**
   - English page -> Spanish page
   - Spanish page -> English page
   - Google ignores incomplete hreflang

2. **Include Self-Reference**
   - Include current page in hreflang list

3. **x-default Usage**
   - Fallback when no language matches
   - Also used for language selector pages

---

## JavaScript SEO

### Google's Rendering Process

```
1. Crawl (Fetch HTML)
      |
2. Render Queue Wait (seconds to days)
      |
3. Rendering (Execute JS)
      |
4. Index
```

### Best Practices

**Recommended SSR Cases:**
- SEO-critical content
- Frequently updated content
- Social share meta tags needed

**Implementation Patterns:**

```javascript
// Next.js SSR
export async function getServerSideProps() {
  const data = await fetchData();
  return { props: { data } };
}

// Nuxt.js SSR
export default {
  async asyncData({ $axios }) {
    const data = await $axios.$get('/api/data');
    return { data };
  }
}
```

### Link Implementation

```html
<!-- Crawlable -->
<a href="/page">Link</a>
<a href="https://example.com/page">Link</a>

<!-- May not be crawlable -->
<a onclick="goto('/page')">Link</a>
<span onclick="navigate('/page')">Link</span>
<a href="javascript:void(0)">Link</a>
```

### Lazy-Loaded Content

```html
<!-- Native lazy loading (Googlebot compatible) -->
<img src="image.jpg" loading="lazy" alt="Description">

<!-- Scroll-triggered dynamic loading (problematic) -->
<div data-src="/content" class="load-on-scroll"></div>
```

---

## HTTP Status Codes

### SEO-Related Codes

| Code | Meaning | SEO Impact |
|------|---------|------------|
| 200 | Success | Indexed normally |
| 301 | Permanent redirect | Link equity transferred |
| 302 | Temporary redirect | Link equity stays with original |
| 304 | Not modified | Improved crawl efficiency |
| 404 | Not found | Removed from index |
| 410 | Gone | Removed from index faster than 404 |
| 500 | Server error | Temporary is OK, persistent causes index decline |
| 503 | Service unavailable | Use during maintenance |

### Redirect Usage

```nginx
# 301: Domain change, permanent URL change
server {
    server_name old-domain.com;
    return 301 https://new-domain.com$request_uri;
}

# 302: A/B testing, temporary maintenance
location /old-page {
    return 302 /new-page;
}
```

---

## Crawl Budget Optimization

### What is Crawl Budget?
The "budget" (time/resources) Googlebot allocates to crawl your site.

### Optimization Points

1. **Block Unnecessary Pages**
   ```txt
   # robots.txt
   Disallow: /search?
   Disallow: /filter?
   Disallow: /tag/*
   ```

2. **Handle Duplicate Content**
   - Canonical settings
   - Parameter handling (Search Console)

3. **Improve Server Response**
   - Target TTFB under 200ms
   - Use caching

4. **Optimize Internal Links**
   - Increase links to important pages
   - Avoid deep hierarchies (within 3 clicks)

5. **Update Sitemap**
   - Prioritize new/updated pages
   - Exclude deleted pages

---

## Mobile-First Indexing

### Checklist

- [ ] Using responsive design or dynamic serving
- [ ] Mobile version has the same content
- [ ] Same structured data on mobile version
- [ ] Same meta tags (title, description) on mobile
- [ ] Images/videos display properly on mobile
- [ ] Resources not blocked on mobile version

### Responsive Design Setup

```html
<!-- Viewport setting -->
<meta name="viewport" content="width=device-width, initial-scale=1">

<!-- Responsive images -->
<picture>
  <source media="(max-width: 640px)" srcset="small.webp">
  <source media="(max-width: 1024px)" srcset="medium.webp">
  <img src="large.webp" alt="Description">
</picture>
```

---

## HTTPS / Security

### Required Configuration

```nginx
# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name example.com;
    return 301 https://$server_name$request_uri;
}

# HSTS setting
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
```

### SEO Impact

- HTTPS is a ranking signal (minor but positive)
- Avoids "Not Secure" warning in Chrome
- Enables HTTP/2 (performance boost)

---

## Debug Commands

```bash
# Check robots.txt
curl -s https://example.com/robots.txt

# Check HTTP headers
curl -I https://example.com/

# Extract canonical / hreflang
curl -s https://example.com/ | grep -E 'rel="canonical"|hreflang'

# Check redirect chain
curl -L -v https://example.com/ 2>&1 | grep -E 'Location:|< HTTP'

# Get rendered HTML (using Puppeteer)
npx puppeteer screenshot https://example.com --fullPage
```
