---
last_verified: 2026-08-29
---

# Structured Data Reference

Implementation guide for structured data supporting Google Search rich results. JSON-LD format recommended.

## Implementation Basics

### JSON-LD Placement

```html
<head>
  <!-- Can be placed in head or body -->
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "Article Title"
  }
  </script>
</head>
```

### Multiple Structured Data

```html
<!-- Method 1: Multiple script tags -->
<script type="application/ld+json">
{ "@type": "Article", ... }
</script>
<script type="application/ld+json">
{ "@type": "BreadcrumbList", ... }
</script>

<!-- Method 2: Combine with @graph (recommended) -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    { "@type": "Article", ... },
    { "@type": "BreadcrumbList", ... }
  ]
}
</script>
```

---

## Article

### NewsArticle

```json
{
  "@context": "https://schema.org",
  "@type": "NewsArticle",
  "headline": "News article headline (no character limit, but keep it concise)",
  "description": "Article summary",
  "image": [
    "https://example.com/photos/1x1/photo.jpg",
    "https://example.com/photos/4x3/photo.jpg",
    "https://example.com/photos/16x9/photo.jpg"
  ],
  "datePublished": "2025-01-15T08:00:00+00:00",
  "dateModified": "2025-01-15T10:30:00+00:00",
  "author": [{
    "@type": "Person",
    "name": "Author Name",
    "url": "https://example.com/author/profile",
    "sameAs": [
      "https://twitter.com/author",
      "https://www.linkedin.com/in/author"
    ]
  }],
  "publisher": {
    "@type": "Organization",
    "name": "Publication Name",
    "logo": {
      "@type": "ImageObject",
      "url": "https://example.com/logo.png",
      "width": 600,
      "height": 60
    }
  },
  "mainEntityOfPage": {
    "@type": "WebPage",
    "@id": "https://example.com/article"
  }
}
```

### BlogPosting

```json
{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "Blog post title",
  "description": "Post summary",
  "image": "https://example.com/blog-image.jpg",
  "datePublished": "2025-01-15T08:00:00+00:00",
  "dateModified": "2025-01-15T10:30:00+00:00",
  "author": {
    "@type": "Person",
    "name": "Author Name"
  },
  "wordCount": 2500,
  "keywords": ["SEO", "content marketing", "Google"]
}
```

---

## FAQ (Frequently Asked Questions)

> **Note:** Google discontinued FAQ rich results entirely on May 7, 2026 (after limiting them to well-known government and health websites since August 2023) — this markup no longer produces rich results in Google Search, and the feature's documentation and Search Console reports have been removed. FAQPage remains valid schema.org: keeping it incurs no penalty and it is kept here for semantic markup and other consumers.

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "What is SEO?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "SEO (Search Engine Optimization) is the practice of optimizing websites to rank higher in search engine results. It involves technical optimizations, content creation, and link building to improve visibility and drive organic traffic."
      }
    },
    {
      "@type": "Question",
      "name": "How long does SEO take to work?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Generally, SEO results take 3-6 months to appear. For highly competitive keywords, it may take a year or more. Results depend on factors like competition, content quality, and technical implementation."
      }
    },
    {
      "@type": "Question",
      "name": "Can I do SEO myself?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Yes, basic SEO can be done yourself. Meta tag optimization, content improvement, and internal link structure are accessible without expert knowledge. However, for technical issues or competitive niches, professional support is beneficial."
      }
    }
  ]
}
```

---

## HowTo

> **Note:** Google discontinued HowTo rich results in September 2023 — this markup no longer produces rich results in Google Search. It remains valid schema.org and is kept here for semantic markup and other consumers.

```json
{
  "@context": "https://schema.org",
  "@type": "HowTo",
  "name": "How to Configure robots.txt",
  "description": "Step-by-step guide to properly configure your website's robots.txt file.",
  "image": "https://example.com/howto-image.jpg",
  "totalTime": "PT15M",
  "estimatedCost": {
    "@type": "MonetaryAmount",
    "currency": "USD",
    "value": "0"
  },
  "tool": [
    {
      "@type": "HowToTool",
      "name": "Text editor"
    },
    {
      "@type": "HowToTool",
      "name": "FTP client"
    }
  ],
  "step": [
    {
      "@type": "HowToStep",
      "name": "Create robots.txt file",
      "text": "Open your text editor and create a new file.",
      "image": "https://example.com/step1.jpg",
      "url": "https://example.com/howto#step1"
    },
    {
      "@type": "HowToStep",
      "name": "Write the rules",
      "text": "Write crawl control rules like User-agent: * and Disallow: /admin/.",
      "image": "https://example.com/step2.jpg",
      "url": "https://example.com/howto#step2"
    },
    {
      "@type": "HowToStep",
      "name": "Upload to server",
      "text": "Use FTP client to upload robots.txt to your root directory.",
      "image": "https://example.com/step3.jpg",
      "url": "https://example.com/howto#step3"
    }
  ]
}
```

---

## Product

```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "SEO Analytics Tool Pro",
  "image": [
    "https://example.com/product-1x1.jpg",
    "https://example.com/product-4x3.jpg",
    "https://example.com/product-16x9.jpg"
  ],
  "description": "Professional SEO analysis tool with comprehensive features. Includes keyword research, competitor analysis, and site audit capabilities.",
  "sku": "SEO-PRO-001",
  "mpn": "925872",
  "brand": {
    "@type": "Brand",
    "name": "SEO Tools Inc."
  },
  "offers": {
    "@type": "Offer",
    "url": "https://example.com/product/seo-pro",
    "priceCurrency": "USD",
    "price": "99.00",
    "priceValidUntil": "2025-12-31",
    "availability": "https://schema.org/InStock",
    "itemCondition": "https://schema.org/NewCondition",
    "seller": {
      "@type": "Organization",
      "name": "SEO Tools Inc."
    },
    "shippingDetails": {
      "@type": "OfferShippingDetails",
      "shippingRate": {
        "@type": "MonetaryAmount",
        "value": "0",
        "currency": "USD"
      },
      "deliveryTime": {
        "@type": "ShippingDeliveryTime",
        "handlingTime": {
          "@type": "QuantitativeValue",
          "minValue": 0,
          "maxValue": 1,
          "unitCode": "DAY"
        },
        "transitTime": {
          "@type": "QuantitativeValue",
          "minValue": 1,
          "maxValue": 3,
          "unitCode": "DAY"
        }
      }
    }
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.8",
    "bestRating": "5",
    "worstRating": "1",
    "ratingCount": "256"
  },
  "review": [
    {
      "@type": "Review",
      "reviewRating": {
        "@type": "Rating",
        "ratingValue": "5",
        "bestRating": "5"
      },
      "author": {
        "@type": "Person",
        "name": "John Smith"
      },
      "datePublished": "2025-01-10",
      "reviewBody": "Very easy to use and makes SEO analysis efficient."
    }
  ]
}
```

---

## LocalBusiness

```json
{
  "@context": "https://schema.org",
  "@type": "Restaurant",
  "name": "The Italian Kitchen",
  "image": [
    "https://example.com/store-1x1.jpg",
    "https://example.com/store-4x3.jpg",
    "https://example.com/store-16x9.jpg"
  ],
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "123 Main Street",
    "addressLocality": "New York",
    "addressRegion": "NY",
    "postalCode": "10001",
    "addressCountry": "US"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": 40.7128,
    "longitude": -74.0060
  },
  "url": "https://example.com/",
  "telephone": "+1-212-555-1234",
  "priceRange": "$$$",
  "servesCuisine": "Italian",
  "openingHoursSpecification": [
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
      "opens": "11:30",
      "closes": "14:00"
    },
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
      "opens": "17:00",
      "closes": "22:00"
    },
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Saturday", "Sunday"],
      "opens": "11:30",
      "closes": "22:00"
    }
  ],
  "menu": "https://example.com/menu",
  "acceptsReservations": "True",
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.5",
    "reviewCount": "89"
  }
}
```

---

## BreadcrumbList

```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "Home",
      "item": "https://example.com/"
    },
    {
      "@type": "ListItem",
      "position": 2,
      "name": "SEO",
      "item": "https://example.com/seo/"
    },
    {
      "@type": "ListItem",
      "position": 3,
      "name": "Technical SEO",
      "item": "https://example.com/seo/technical/"
    },
    {
      "@type": "ListItem",
      "position": 4,
      "name": "robots.txt Guide"
    }
  ]
}
```

**Note:** The `item` property can be omitted for the last item (current page).

---

## VideoObject

### Basic Implementation

```json
{
  "@context": "https://schema.org",
  "@type": "VideoObject",
  "name": "SEO Beginner Course - Part 1",
  "description": "Learn SEO basics in 15 minutes. Understand how crawling, indexing, and ranking work.",
  "thumbnailUrl": [
    "https://example.com/thumb-1x1.jpg",
    "https://example.com/thumb-4x3.jpg",
    "https://example.com/thumb-16x9.jpg"
  ],
  "uploadDate": "2025-01-15T08:00:00+00:00",
  "duration": "PT15M30S",
  "contentUrl": "https://example.com/videos/seo-intro.mp4",
  "embedUrl": "https://example.com/embed/seo-intro",
  "interactionStatistic": {
    "@type": "InteractionCounter",
    "interactionType": { "@type": "WatchAction" },
    "userInteractionCount": 12500
  }
}
```

### Live Streaming (LIVE badge)

```json
{
  "@context": "https://schema.org",
  "@type": "VideoObject",
  "name": "SEO Webinar LIVE",
  "description": "Real-time coverage of the latest SEO trends",
  "thumbnailUrl": "https://example.com/live-thumb.jpg",
  "uploadDate": "2025-01-20T19:00:00+00:00",
  "publication": {
    "@type": "BroadcastEvent",
    "isLiveBroadcast": true,
    "startDate": "2025-01-20T19:00:00+00:00",
    "endDate": "2025-01-20T20:30:00+00:00"
  }
}
```

### Key Moments (Clip)

```json
{
  "@context": "https://schema.org",
  "@type": "VideoObject",
  "name": "Complete SEO Guide",
  "description": "Master SEO in 60 minutes",
  "thumbnailUrl": "https://example.com/thumb.jpg",
  "uploadDate": "2025-01-15T08:00:00+00:00",
  "duration": "PT60M",
  "hasPart": [
    {
      "@type": "Clip",
      "name": "Introduction",
      "startOffset": 0,
      "endOffset": 120,
      "url": "https://example.com/video?t=0"
    },
    {
      "@type": "Clip",
      "name": "Technical SEO Basics",
      "startOffset": 120,
      "endOffset": 900,
      "url": "https://example.com/video?t=120"
    },
    {
      "@type": "Clip",
      "name": "Content Optimization",
      "startOffset": 900,
      "endOffset": 1800,
      "url": "https://example.com/video?t=900"
    },
    {
      "@type": "Clip",
      "name": "Link Strategy",
      "startOffset": 1800,
      "endOffset": 2700,
      "url": "https://example.com/video?t=1800"
    },
    {
      "@type": "Clip",
      "name": "Summary and Q&A",
      "startOffset": 2700,
      "endOffset": 3600,
      "url": "https://example.com/video?t=2700"
    }
  ]
}
```

---

## Organization / WebSite

### Organization

```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "SEO Master Inc.",
  "alternateName": "SEO Master",
  "url": "https://example.com/",
  "logo": "https://example.com/logo.png",
  "contactPoint": {
    "@type": "ContactPoint",
    "telephone": "+1-800-555-1234",
    "contactType": "customer service",
    "areaServed": "US",
    "availableLanguage": ["English", "Spanish"]
  },
  "sameAs": [
    "https://twitter.com/seomaster",
    "https://www.facebook.com/seomaster",
    "https://www.linkedin.com/company/seomaster"
  ]
}
```

### WebSite

> **Note:** The Sitelinks Search Box (`potentialAction` / `SearchAction`) was retired in November 2024 and no longer appears in Google Search — do not add it. WebSite markup itself is still current: Google uses it to determine the site name shown in search results, so provide `name` (and `alternateName` for a shorter variant).

```json
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "SEO Master Inc.",
  "alternateName": "SEO Master",
  "url": "https://example.com/"
}
```

---

## Event

```json
{
  "@context": "https://schema.org",
  "@type": "Event",
  "name": "SEO Conference 2025",
  "description": "The largest SEO conference. Learn the latest trends and practical techniques.",
  "image": "https://example.com/event-image.jpg",
  "startDate": "2025-03-15T10:00:00-05:00",
  "endDate": "2025-03-15T18:00:00-05:00",
  "eventStatus": "https://schema.org/EventScheduled",
  "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
  "location": {
    "@type": "Place",
    "name": "Convention Center",
    "address": {
      "@type": "PostalAddress",
      "streetAddress": "100 Convention Blvd",
      "addressLocality": "New York",
      "addressRegion": "NY",
      "postalCode": "10001",
      "addressCountry": "US"
    }
  },
  "performer": {
    "@type": "Person",
    "name": "SEO Expert John Doe"
  },
  "organizer": {
    "@type": "Organization",
    "name": "SEO Master Inc.",
    "url": "https://example.com/"
  },
  "offers": {
    "@type": "Offer",
    "url": "https://example.com/event/register",
    "price": "150.00",
    "priceCurrency": "USD",
    "availability": "https://schema.org/InStock",
    "validFrom": "2025-01-01T00:00:00-05:00"
  }
}
```

---

## Validation Tools

### Rich Results Test
https://search.google.com/test/rich-results

```bash
# CLI validation (using Puppeteer)
npx puppeteer screenshot "https://search.google.com/test/rich-results?url=https://example.com"
```

### Schema Markup Validator
https://validator.schema.org/

### Common Errors and Fixes

| Error | Cause | Solution |
|-------|-------|----------|
| Missing field | Required field missing | Add required property |
| Invalid URL | URL format is wrong | Specify complete URL |
| Invalid date | Date format is wrong | Use ISO 8601 format |
| Image too small | Image is too small | Ensure minimum 1200px |
| Unsupported type | Type not supported | Check supported types |

---

## Best Practices

1. **Use JSON-LD** (Preferred over Microdata/RDFa)
2. **Validate in test environment** before production deployment
3. **Only markup information matching page content**
4. **Regular validation** (Monitor in Search Console)
5. **Avoid excessive markup** (Risk of spam classification)
