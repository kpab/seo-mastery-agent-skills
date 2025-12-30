# Content SEO Reference

Guide for creating content optimized for both search engines and users.

## Meta Tag Optimization

### Title Tag

```html
<title>Primary Keyword - Secondary Keyword | Site Name</title>
```

**Best Practices:**

| Item | Recommendation |
|------|----------------|
| Length | 50-60 characters |
| Keyword position | Place at the beginning |
| Uniqueness | Unique title for each page |
| Brand name | "| Site Name" at the end |
| Separators | Use `-` `|` `–` |

**Pattern Templates:**

```html
<!-- Article page -->
<title>Complete Guide to SEO in 2025 - From Basics to Advanced | Site Name</title>

<!-- Product page -->
<title>Product Name - Category | Shop Name [Official]</title>

<!-- Category page -->
<title>Category Name Products | Shop Name</title>

<!-- Home page -->
<title>Site Name | Tagline (Service Summary)</title>
```

**Patterns to Avoid:**

```html
<!-- Keyword stuffing -->
<title>SEO SEO Guide SEO Tips SEO Tools SEO Company</title>

<!-- Duplicate titles -->
<title>Site Name</title> <!-- Same on all pages -->

<!-- Too long -->
<title>2025 Ultimate Complete Comprehensive SEO Guide For Beginners And Experts Tips Tricks And Strategies For Google Search Engine Optimization</title>
```

---

### Meta Description

```html
<meta name="description" content="Page description. Summarize in about 160 characters.">
```

**Best Practices:**

| Item | Recommendation |
|------|----------------|
| Length | 150-160 characters |
| Content | Accurate summary of page content |
| CTA | Action prompts like "Learn more" |
| Keywords | Include naturally (shown in bold) |

**Good Example:**

```html
<meta name="description" content="Learn SEO from basics to advanced techniques. This guide covers crawl optimization, structured data, and Core Web Vitals improvement with practical examples.">
```

**Bad Examples:**

```html
<!-- Keyword list -->
<meta name="description" content="SEO, SEO guide, Google, search engine, optimization, ranking, top results">

<!-- Unrelated to content -->
<meta name="description" content="We are a company founded in 1990. We strive for customer satisfaction.">
```

---

### OGP / Twitter Card

```html
<!-- Open Graph Protocol -->
<meta property="og:title" content="Page Title">
<meta property="og:description" content="Page description">
<meta property="og:type" content="article">
<meta property="og:url" content="https://example.com/page/">
<meta property="og:image" content="https://example.com/ogp-image.jpg">
<meta property="og:site_name" content="Site Name">
<meta property="og:locale" content="en_US">

<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@username">
<meta name="twitter:title" content="Page Title">
<meta name="twitter:description" content="Page description">
<meta name="twitter:image" content="https://example.com/twitter-image.jpg">
```

**OGP Image Sizes:**

| Platform | Recommended Size |
|----------|------------------|
| Facebook | 1200 x 630px |
| Twitter | 1200 x 628px |
| LinkedIn | 1200 x 627px |
| Pinterest | 1000 x 1500px |

---

## Heading Structure (H1-H6)

### Correct Hierarchy

```html
<h1>Main Title (One per page)</h1>

<h2>Section Heading 1</h2>
<p>Body text...</p>

<h3>Subsection 1-1</h3>
<p>Body text...</p>

<h3>Subsection 1-2</h3>
<p>Body text...</p>

<h2>Section Heading 2</h2>
<p>Body text...</p>

<h3>Subsection 2-1</h3>
<p>Body text...</p>

<h4>Sub-subsection 2-1-1</h4>
<p>Body text...</p>
```

**Rules:**

1. **One H1 per page**
2. **Don't skip levels** (H1 -> H3 is wrong)
3. **Maintain logical structure**
4. **Include keywords naturally**

**Bad Examples:**

```html
<!-- Skipping levels -->
<h1>Title</h1>
<h3>Jumping to H3</h3>

<!-- Multiple H1s -->
<h1>Title 1</h1>
<h1>Title 2</h1>

<!-- Using headings for styling -->
<h2 style="font-size: 14px;">Small text as H2...</h2>
```

---

## Content Quality

### E-E-A-T Focused Structure

**Experience:**
```html
<!-- Show first-hand experience -->
<p>After using this tool for 3 months, I verified the following results.</p>

<!-- Photos/screenshots -->
<figure>
  <img src="actual-screenshot.jpg" alt="Tool dashboard">
  <figcaption>Actual dashboard (January 2025)</figcaption>
</figure>
```

**Expertise:**
```html
<!-- Author information -->
<div class="author-bio">
  <img src="author.jpg" alt="Author Name">
  <p><strong>Author Name</strong> - SEO Consultant</p>
  <p>10+ years of SEO experience. Google certified partner.
  Has supported 200+ companies with SEO.</p>
  <a href="/author/profile">Author Profile</a>
</div>
```

**Authoritativeness:**
```html
<!-- Citations/sources -->
<blockquote cite="https://developers.google.com/search">
  <p>"Creating high-quality content is one of the most important factors
  for ranking well in search results."</p>
  <footer>— Google Search Central</footer>
</blockquote>
```

**Trustworthiness:**
```html
<!-- Update date -->
<time datetime="2025-01-15">Last updated: January 15, 2025</time>

<!-- Fact check -->
<p>This article was reviewed by <a href="/author/expert">Expert Name</a>.</p>

<!-- Source disclosure -->
<section class="sources">
  <h2>References</h2>
  <ul>
    <li><a href="...">Google Search Central Documentation</a></li>
    <li><a href="...">Web.dev - Core Web Vitals</a></li>
  </ul>
</section>
```

---

## Internal Linking Strategy

### Anchor Text Best Practices

```html
<!-- Good: Descriptive anchor text -->
<p>For details, see our <a href="/seo-guide">SEO basics guide</a>.</p>

<!-- Good: Clear context -->
<p>For Core Web Vitals improvements,
check our <a href="/core-web-vitals">LCP, INP, and CLS optimization guide</a>.</p>

<!-- Bad: Too generic -->
<p>For details, click <a href="/seo-guide">here</a>.</p>
<p><a href="/core-web-vitals">Click here</a></p>

<!-- Bad: Over-optimized -->
<p><a href="/seo-guide">SEO SEO Guide Google SEO Search Engine Optimization</a></p>
```

### Link Structure Design

```
Homepage
├── Category A
│   ├── Article A-1 ← Link within silo structure
│   ├── Article A-2
│   └── Article A-3
├── Category B
│   ├── Article B-1
│   └── Article B-2
└── Important Page (linked from multiple categories)
```

**Implementation Points:**

1. **Increase links to important pages**
   - Link from sidebar, footer
   - Feature in related articles section

2. **Use silo structure**
   - Prioritize links within same category
   - Cross-category links should be strategic

3. **Prevent orphan pages**
   - Every page should have at least one internal link
   - Use breadcrumbs to show hierarchy

---

## Image Optimization

### Alt Attribute

```html
<!-- Good: Specific and descriptive -->
<img src="chart.png" alt="Bar chart showing 2024 SEO trends. AI content at 40% ranks first">

<!-- Good: Product image -->
<img src="product.jpg" alt="Apple MacBook Pro 14-inch M3 chip Silver">

<!-- Bad: Keyword stuffing -->
<img src="chart.png" alt="SEO SEO guide Google search engine optimization chart statistics">

<!-- Bad: Not descriptive -->
<img src="chart.png" alt="Chart">
<img src="product.jpg" alt="Product image">

<!-- Decorative images: empty alt -->
<img src="decorative-line.png" alt="">
```

### File Names

```
Good:
seo-trends-2024-chart.webp
macbook-pro-14-m3-silver.jpg

Bad:
IMG_1234.jpg
screenshot-2025-01-15.png
image1.webp
```

### Image Format Selection

| Format | Use Case | Compression |
|--------|----------|-------------|
| WebP | Photos, illustrations general | Lossy/Lossless |
| AVIF | Next-gen (high compression) | Lossy/Lossless |
| PNG | Images requiring transparency | Lossless |
| SVG | Logos, icons | Vector |
| JPEG | Legacy support | Lossy |

### Responsive Images

```html
<picture>
  <source media="(min-width: 1024px)" srcset="large.webp" type="image/webp">
  <source media="(min-width: 640px)" srcset="medium.webp" type="image/webp">
  <source srcset="small.webp" type="image/webp">
  <img src="fallback.jpg" alt="Description" width="800" height="600" loading="lazy">
</picture>
```

---

## URL Design

### Best Practices

```
Good:
https://example.com/seo/technical-guide
https://example.com/products/laptop/macbook-pro
https://example.com/blog/2025/01/seo-trends

Bad:
https://example.com/p?id=12345
https://example.com/category1/subcategory2/page
https://example.com/seo-seo-optimization-guide-tips-tricks
```

**Rules:**

| Item | Recommendation |
|------|----------------|
| Length | Under 50-60 characters |
| Separator | Use hyphens `-` |
| Characters | Lowercase alphanumeric only |
| Depth | Within 3 levels |
| Keywords | Include main keyword |

### Patterns to Avoid

```
# Underscores
example.com/seo_guide    Bad
example.com/seo-guide    Good

# Mixed case
example.com/SEO-Guide    Bad
example.com/seo-guide    Good

# Unnecessary parameters
example.com/page?session=abc123    Bad

# Non-ASCII URLs
example.com/seo-guide    Good (encodes to long string)
```

---

## Content Update Strategy

### Identifying Content to Update

1. **Traffic declining pages**
   - 20%+ decrease over past 3-6 months

2. **Pages with outdated information**
   - Dates, statistics, tool versions

3. **Ranking dropped pages**
   - Dropped from top 10 to 20+ position

4. **Low CTR pages**
   - Low click rate relative to impressions

### Update Best Practices

```html
<!-- Mark update date -->
<meta property="article:modified_time" content="2025-01-15T10:30:00+00:00">

<!-- Display in content -->
<p class="last-updated">
  <time datetime="2025-01-15">Last updated: January 15, 2025</time>
  (Originally published: June 1, 2024)
</p>

<!-- Include update history -->
<details>
  <summary>Update History</summary>
  <ul>
    <li>2025-01-15: Added 2025 trends</li>
    <li>2024-10-01: Updated Core Web Vitals info</li>
    <li>2024-06-01: Initial publication</li>
  </ul>
</details>
```

---

## Search Intent

### Four Types of Search Intent

| Type | Intent | Example | Best Content |
|------|--------|---------|--------------|
| Informational | Want information | "What is SEO" | Guides, tutorials |
| Navigational | Go to specific site | "Gmail login" | Brand pages |
| Commercial | Research before purchase | "Best SEO tools" | Comparisons, reviews |
| Transactional | Want to buy/sign up | "SEO tool signup" | Product/service pages |

### Content Design by Intent

**Informational Example:**
```markdown
# What is SEO? Basics for Beginners

## Definition of SEO
SEO (Search Engine Optimization) is...

## Why SEO Matters
1. Continuous traffic acquisition
2. Reduced advertising costs
3. Brand awareness improvement

## Core SEO Elements
### Technical SEO
...
### Content SEO
...
```

**Commercial Example:**
```markdown
# Top 10 SEO Tools Compared [2025]

| Tool | Price | Features | Rating |
|------|-------|----------|--------|
| Tool A | $100/mo | ... | 5 stars |
| Tool B | $50/mo | ... | 4 stars |

## Detailed Reviews
### Tool A
My experience after using it...
```
