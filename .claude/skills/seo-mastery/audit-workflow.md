# SEO Audit Workflow

Systematic process for conducting comprehensive site-wide SEO audits.

## Audit Overview

```
Phase 1: Crawl Diagnosis
    |
Phase 2: Technical SEO Diagnosis
    |
Phase 3: Content Diagnosis
    |
Phase 4: Performance Diagnosis
    |
Phase 5: Competitive Analysis
    |
Phase 6: Improvement Plan
```

---

## Phase 1: Crawl Diagnosis

### 1.1 robots.txt Check

```bash
# Get robots.txt
curl -s https://example.com/robots.txt

# Check points:
# - Are important pages Disallowed?
# - Is there a sitemap reference?
# - Is Crawl-delay set too high?
```

**Checklist:**
- [ ] robots.txt exists
- [ ] Important pages (/, /products/, /services/) are not blocked
- [ ] CSS/JS/images are not blocked
- [ ] Sitemap reference exists

### 1.2 Sitemap Check

```bash
# Get sitemap
curl -s https://example.com/sitemap.xml | head -100

# Count URLs
curl -s https://example.com/sitemap.xml | grep -c "<loc>"

# Check lastmod
curl -s https://example.com/sitemap.xml | grep "<lastmod>" | sort | uniq -c
```

**Checklist:**
- [ ] Sitemap exists
- [ ] All main pages are included
- [ ] No 404 pages are included
- [ ] lastmod is accurately updated
- [ ] Submitted to Search Console

### 1.3 Index Status

```bash
# Check index count with site: search
# Search "site:example.com" on Google

# Check specific directory index
# site:example.com/blog/
```

**Checklist:**
- [ ] Index count matches expectations
- [ ] Important pages are indexed
- [ ] Unnecessary pages (admin, etc.) are not indexed

---

## Phase 2: Technical SEO Diagnosis

### 2.1 HTTPS/Security

```bash
# Check SSL certificate
curl -vI https://example.com 2>&1 | grep -E 'SSL|certificate|expire'

# Check redirect from HTTP
curl -I http://example.com

# Detect Mixed Content
curl -s https://example.com | grep -E 'http://'
```

**Checklist:**
- [ ] HTTPS enabled
- [ ] HTTP redirects to HTTPS with 301
- [ ] No Mixed Content
- [ ] SSL certificate is valid

### 2.2 Redirect Diagnosis

```bash
# Check redirect chain
curl -L -I https://example.com 2>&1 | grep -E 'HTTP/|Location:'

# Check www unification
curl -I https://www.example.com
curl -I https://example.com
```

**Checklist:**
- [ ] Redirect chain is 2 hops or less
- [ ] Using 301, not 302
- [ ] www/non-www is unified

### 2.3 Meta Tag Diagnosis

```bash
# Extract meta information
curl -s https://example.com | grep -E '<title>|<meta name="description"|<meta name="robots"|<link rel="canonical"'

# Batch check multiple pages (example)
for url in "/" "/about" "/products"; do
  echo "=== $url ==="
  curl -s "https://example.com$url" | grep -E '<title>'
done
```

**Checklist:**
- [ ] Each page has unique title
- [ ] Title is under 60 characters
- [ ] Meta description is under 160 characters
- [ ] Canonical URL is correctly set
- [ ] No unnecessary noindex/nofollow

### 2.4 Structured Data Diagnosis

```bash
# Extract JSON-LD
curl -s https://example.com | grep -oP '<script type="application/ld\+json">.*?</script>'

# Rich Results Test (check in browser)
# https://search.google.com/test/rich-results?url=https://example.com
```

**Checklist:**
- [ ] Appropriate structured data is implemented
- [ ] No errors (Rich Results Test)
- [ ] Matches page content

### 2.5 Mobile Compatibility

```bash
# Check viewport
curl -s https://example.com | grep 'viewport'

# Mobile-Friendly Test (check in browser)
# https://search.google.com/test/mobile-friendly?url=https://example.com
```

**Checklist:**
- [ ] Responsive design or dynamic serving
- [ ] viewport meta tag is set
- [ ] Tap targets are appropriate size
- [ ] Text is readable size

---

## Phase 3: Content Diagnosis

### 3.1 Heading Structure

```bash
# Extract heading tags
curl -s https://example.com | grep -oP '<h[1-6][^>]*>.*?</h[1-6]>'

# Count H1 tags
curl -s https://example.com | grep -c '<h1'
```

**Checklist:**
- [ ] Only one H1 tag
- [ ] Heading hierarchy is logical (H1→H2→H3)
- [ ] Headings contain keywords

### 3.2 Link Diagnosis

```bash
# Extract internal links
curl -s https://example.com | grep -oP 'href="[^"]*"' | grep -v 'http' | head -20

# Extract external links
curl -s https://example.com | grep -oP 'href="https?://[^"]*"' | grep -v 'example.com'

# Check broken links (simple version)
curl -s https://example.com | grep -oP 'href="[^"]*"' | while read href; do
  url=$(echo $href | sed 's/href="\(.*\)"/\1/')
  status=$(curl -o /dev/null -s -w "%{http_code}" "$url")
  echo "$status $url"
done
```

**Checklist:**
- [ ] Internal links are properly set
- [ ] Anchor text is descriptive
- [ ] No broken links
- [ ] External links have appropriate rel attributes

### 3.3 Image Diagnosis

```bash
# Check alt attributes
curl -s https://example.com | grep -oP '<img[^>]*>' | grep -v 'alt='

# Check image dimensions
curl -s https://example.com | grep -oP '<img[^>]*>' | grep -v 'width\|height'
```

**Checklist:**
- [ ] All images have alt attributes
- [ ] Alt attributes are descriptive (not empty)
- [ ] Image dimensions (width/height) are specified
- [ ] Using appropriate formats (WebP, etc.)

### 3.4 Content Quality

**Manual Checks:**
- [ ] Content is original
- [ ] Matches user search intent
- [ ] Sufficient information volume
- [ ] Regularly updated
- [ ] Author information is stated

---

## Phase 4: Performance Diagnosis

### 4.1 Core Web Vitals

```bash
# Lighthouse CLI
npx lighthouse https://example.com --output=json --output-path=./report.json --preset=mobile

# Extract results
cat report.json | jq '.audits["largest-contentful-paint"].numericValue'
cat report.json | jq '.audits["cumulative-layout-shift"].numericValue'
```

**Checklist:**
- [ ] LCP ≤ 2.5 seconds
- [ ] INP ≤ 200ms
- [ ] CLS ≤ 0.1
- [ ] Performance score ≥ 80

### 4.2 Resource Optimization

```bash
# Check page size
curl -s -o /dev/null -w "%{size_download}\n" https://example.com

# Check compression
curl -H "Accept-Encoding: gzip, deflate, br" -sI https://example.com | grep -i 'content-encoding'
```

**Checklist:**
- [ ] Gzip/Brotli compression enabled
- [ ] Images are optimized
- [ ] CSS/JS are minified
- [ ] No unnecessary resources

---

## Phase 5: Competitive Analysis

### 5.1 Identify Competitors

**Steps:**
1. Search for main keywords
2. List top 5-10 sites
3. Classify direct vs indirect competitors

### 5.2 Comparison Items

| Item | Our Site | Competitor A | Competitor B |
|------|----------|--------------|--------------|
| Domain age | | | |
| Index count | | | |
| Content volume | | | |
| Update frequency | | | |
| Structured data | | | |
| Core Web Vitals | | | |
| Backlink count | | | |

### 5.3 Gap Analysis

```markdown
## Keyword Gap
Keywords competitors rank for but we don't:
1. Keyword A (Search volume: X)
2. Keyword B (Search volume: Y)

## Content Gap
Content types competitors have but we don't:
1. How-to guides
2. Comparison articles
3. Case studies

## Technical Gap
Features competitors have but we don't:
1. FAQ structured data
2. Site search
3. Multilingual support
```

---

## Phase 6: Improvement Plan

### 6.1 Priority Matrix

| Priority | Impact | Effort | Example Actions |
|----------|--------|--------|-----------------|
| Critical | High | Low | Fix noindex, fix 404s, resolve title duplicates |
| High | High | Medium | Add structured data, optimize meta tags |
| Medium | Medium | Medium | Improve Core Web Vitals, add content |
| Low | Low | High | Site structure changes, domain migration |

### 6.2 Improvement Report Template

```markdown
# SEO Audit Report

## Executive Summary
- Audit date: YYYY-MM-DD
- Target site: https://example.com
- Overall assessment: B (Room for improvement)

## Critical Issues
1. **[Critical] noindex set on multiple pages**
   - Impact: Important pages not indexed
   - Action: Remove noindex from affected pages
   - Effort: 1 hour

2. **[High] LCP is 4.2 seconds (Target: under 2.5s)**
   - Impact: Negative effect on UX and ranking
   - Action: Image optimization, Critical CSS implementation
   - Effort: 8 hours

## Improvement Roadmap

### Week 1-2 (Critical Response)
- [ ] Fix noindex issues
- [ ] Fix 404 pages
- [ ] Resolve redirect chains

### Week 3-4 (Technical SEO Improvements)
- [ ] Add structured data
- [ ] Optimize meta tags
- [ ] Update sitemap

### Month 2 (Performance Improvements)
- [ ] LCP optimization
- [ ] CLS optimization
- [ ] Convert image formats

### Month 3 (Content Improvements)
- [ ] Update existing content
- [ ] Add new content
- [ ] Optimize internal links

## Expected Results
- Organic traffic: +30% (after 3 months)
- Core Web Vitals: All "Good" ratings
- Index count: +50 pages
```

---

## Audit Tools List

### Free Tools
- Google Search Console
- Google PageSpeed Insights
- Google Rich Results Test
- Lighthouse
- Chrome DevTools
- Screaming Frog (up to 500 URLs)

### Paid Tools
- Screaming Frog (paid version)
- Ahrefs / SEMrush
- Moz Pro
- DeepCrawl

### CLI Tools

```bash
# Lighthouse CLI
npm install -g lighthouse

# Batch audit script
for url in "https://example.com/" "https://example.com/about" "https://example.com/products"; do
  npx lighthouse "$url" --output=html --output-path="./reports/$(echo $url | md5sum | cut -c1-8).html"
done
```

---

## Regular Audit Schedule

| Frequency | Audit Content |
|-----------|---------------|
| Weekly | Search Console error check, index status |
| Monthly | Core Web Vitals, ranking changes, competitor trends |
| Quarterly | Full technical audit, content audit |
| Yearly | Site structure review, SEO strategy review |
