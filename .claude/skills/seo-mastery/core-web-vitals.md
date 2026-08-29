---
last_verified: 2026-08-29
---

# Core Web Vitals Reference

Detailed optimization guide for Core Web Vitals, Google's ranking factors.

## Overview

Core Web Vitals are three key metrics measuring user experience.

| Metric | Measures | Good | Needs Improvement | Poor |
|--------|----------|------|-------------------|------|
| LCP | Loading speed | ≤ 2.5s | 2.5-4s | > 4s |
| INP | Interactivity | ≤ 200ms | 200-500ms | > 500ms |
| CLS | Visual stability | ≤ 0.1 | 0.1-0.25 | > 0.25 |

---

## LCP (Largest Contentful Paint)

### What is LCP?
Time until the largest content element within the viewport is displayed.

**LCP Element Candidates:**
- `<img>` elements
- `<image>` elements within `<svg>`
- `<video>` elements (poster image)
- Elements with `background-image`
- Block-level elements containing text

### Main Causes and Solutions

#### 1. Slow Server Response

**Diagnosis:**
```bash
# Measure TTFB (Time to First Byte)
curl -o /dev/null -s -w "TTFB: %{time_starttransfer}s\n" https://example.com/
```

**Solutions:**
```nginx
# Nginx cache configuration
proxy_cache_path /tmp/nginx levels=1:2 keys_zone=my_cache:10m max_size=1g;

location / {
    proxy_cache my_cache;
    proxy_cache_valid 200 60m;
    proxy_cache_use_stale error timeout http_500 http_502 http_503 http_504;
}
```

```javascript
// CDN (Cloudflare) configuration example
// Cache-Control header
res.setHeader('Cache-Control', 'public, max-age=31536000, immutable');
```

#### 2. Render-Blocking Resources

**Diagnosis:**
```html
<!-- Blocking resource examples -->
<link rel="stylesheet" href="styles.css"> <!-- Blocking -->
<script src="app.js"></script> <!-- Blocking -->
```

**Solutions:**

```html
<!-- Inline Critical CSS -->
<style>
  /* Minimum CSS needed for first view */
  .hero { ... }
  .nav { ... }
</style>

<!-- Defer non-critical CSS -->
<link rel="preload" href="styles.css" as="style" onload="this.onload=null;this.rel='stylesheet'">
<noscript><link rel="stylesheet" href="styles.css"></noscript>

<!-- Defer JavaScript execution -->
<script src="app.js" defer></script>
<!-- or -->
<script src="analytics.js" async></script>
```

#### 3. Slow Image Loading

**Solutions:**

```html
<!-- Preload LCP image -->
<link rel="preload" as="image" href="hero.webp" fetchpriority="high">

<!-- Optimal image formats -->
<picture>
  <source srcset="hero.avif" type="image/avif">
  <source srcset="hero.webp" type="image/webp">
  <img src="hero.jpg" alt="Hero image"
       width="1200" height="600"
       fetchpriority="high"
       decoding="async">
</picture>

<!-- Responsive images -->
<img srcset="hero-400.webp 400w,
             hero-800.webp 800w,
             hero-1200.webp 1200w"
     sizes="(max-width: 600px) 400px,
            (max-width: 1000px) 800px,
            1200px"
     src="hero-1200.webp"
     alt="Description">
```

#### 4. Client-Side Rendering

**Solutions:**

```javascript
// Next.js: SSR implementation
export async function getServerSideProps() {
  const data = await fetchData();
  return { props: { data } };
}

// Next.js: SSG implementation
export async function getStaticProps() {
  const data = await fetchData();
  return {
    props: { data },
    revalidate: 3600 // Regenerate every hour
  };
}
```

### LCP Optimization Checklist

- [ ] TTFB under 200ms
- [ ] LCP image is preloaded
- [ ] Images are WebP/AVIF format
- [ ] Critical CSS is inlined
- [ ] Unnecessary JavaScript is deferred
- [ ] Using CDN
- [ ] Server caching is properly configured

---

## INP (Interaction to Next Paint)

### What is INP?
Delay time from user interaction (click, tap, key input) to the next paint.

**Difference from FID:**
- FID: Measures only first interaction
- INP: Measures all interactions during page session

### Main Causes and Solutions

#### 1. Heavy JavaScript Execution

**Diagnosis:**
```javascript
// Detect long tasks
const observer = new PerformanceObserver((list) => {
  for (const entry of list.getEntries()) {
    console.log('Long Task:', entry.duration, 'ms');
  }
});
observer.observe({ entryTypes: ['longtask'] });
```

**Solution: Task Splitting**

```javascript
// Bad: Blocks main thread
function processItems(items) {
  items.forEach(item => heavyProcess(item));
}

// Good: Yield to main thread
async function processItemsAsync(items) {
  for (const item of items) {
    heavyProcess(item);
    // Yield control to main thread
    await new Promise(resolve => setTimeout(resolve, 0));
  }
}

// Good: Using scheduler.yield() — Chromium and Firefox only.
// Not supported in Safari and not Baseline, so the feature check is required.
async function processItemsWithYield(items) {
  for (const item of items) {
    heavyProcess(item);
    if ('scheduler' in window && 'yield' in scheduler) {
      await scheduler.yield();
    }
  }
}
```

**Solution: Web Workers**

```javascript
// Main thread
const worker = new Worker('worker.js');

worker.postMessage({ items: largeDataset });

worker.onmessage = (e) => {
  const result = e.data;
  updateUI(result);
};

// worker.js
self.onmessage = (e) => {
  const result = heavyComputation(e.data.items);
  self.postMessage(result);
};
```

#### 2. Large DOM Size

**Diagnosis:**
```javascript
// Check DOM element count
console.log('DOM Elements:', document.querySelectorAll('*').length);
```

**Solutions:**

```javascript
// Virtual scrolling implementation (React example)
import { FixedSizeList as List } from 'react-window';

function VirtualizedList({ items }) {
  return (
    <List
      height={600}
      itemCount={items.length}
      itemSize={50}
      width="100%"
    >
      {({ index, style }) => (
        <div style={style}>{items[index].name}</div>
      )}
    </List>
  );
}
```

```css
/* Lazy rendering with content-visibility */
.below-fold-content {
  content-visibility: auto;
  contain-intrinsic-size: 0 500px;
}
```

#### 3. Third-Party Scripts

**Solutions:**

```html
<!-- Lazy loading -->
<script>
  // Load after user interaction
  let loaded = false;
  function loadAnalytics() {
    if (loaded) return;
    loaded = true;
    const script = document.createElement('script');
    script.src = 'https://analytics.example.com/script.js';
    document.body.appendChild(script);
  }

  document.addEventListener('scroll', loadAnalytics, { once: true });
  document.addEventListener('click', loadAnalytics, { once: true });
</script>

<!-- Execute in worker with Partytown -->
<script type="text/partytown" src="https://analytics.example.com/script.js"></script>
```

### INP Optimization Checklist

- [ ] No long tasks (50ms+)
- [ ] Event handlers are lightweight
- [ ] DOM element count under 1500
- [ ] Third-party scripts are lazy loaded
- [ ] Heavy processing runs in Web Workers
- [ ] Using requestIdleCallback

---

## CLS (Cumulative Layout Shift)

### What is CLS?
Cumulative score of unexpected layout shifts during page load.

**Formula:**
```
CLS = Impact Fraction × Distance Fraction
Impact Fraction = Area affected by shift / Viewport area
Distance Fraction = Distance moved / Viewport height
```

### Main Causes and Solutions

#### 1. Images/Videos Without Dimensions

**Solutions:**

```html
<!-- Specify width/height attributes -->
<img src="image.jpg" width="800" height="600" alt="Description">

<!-- Maintain aspect ratio with CSS -->
<style>
  img {
    width: 100%;
    height: auto;
    aspect-ratio: 4 / 3;
  }
</style>

<!-- For video -->
<video width="1280" height="720" poster="poster.jpg">
  <source src="video.mp4" type="video/mp4">
</video>

<!-- For iframe -->
<div style="position: relative; padding-bottom: 56.25%; height: 0;">
  <iframe
    src="https://www.youtube.com/embed/xxxxx"
    style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"
    frameborder="0"
    allowfullscreen>
  </iframe>
</div>
```

#### 2. Dynamically Inserted Content

**Solutions:**

```html
<!-- Bad: Suddenly inserted banner -->
<div id="banner-container"></div>
<script>
  fetch('/api/banner').then(...)
</script>

<!-- Good: Reserve space in advance -->
<div id="banner-container" style="min-height: 250px;">
  <!-- Skeleton UI -->
  <div class="skeleton" style="height: 250px; background: #eee;"></div>
</div>

<!-- Good: Reserve space with CSS -->
<style>
  .ad-slot {
    min-height: 250px;
    contain: layout;
  }
</style>
```

#### 3. Web Fonts (FOUT/FOIT)

**Solutions:**

```css
/* Use font-display: swap */
@font-face {
  font-family: 'CustomFont';
  src: url('custom-font.woff2') format('woff2');
  font-display: swap;
}

/* Adjust fallback with size-adjust */
@font-face {
  font-family: 'CustomFont-Fallback';
  src: local('Arial');
  size-adjust: 105%;
  ascent-override: 90%;
  descent-override: 20%;
  line-gap-override: 0%;
}
```

```html
<!-- Preload fonts -->
<link rel="preload" href="custom-font.woff2" as="font" type="font/woff2" crossorigin>
```

#### 4. Ads/Embedded Content

**Solutions:**

```html
<!-- Fixed-size container -->
<div class="ad-container" style="width: 300px; height: 250px; contain: strict;">
  <!-- Ad script -->
</div>

<!-- Set minimum height -->
<style>
  .ad-container {
    min-height: 250px;
    background: #f0f0f0;
  }

  /* After ad loads */
  .ad-container.loaded {
    min-height: auto;
  }
</style>
```

### CLS Optimization Checklist

- [ ] All images have width/height specified
- [ ] Videos/iframes have aspect ratio set
- [ ] Ad space is reserved in advance
- [ ] Web fonts have font-display: swap set
- [ ] Dynamic content has min-height set
- [ ] Animations use transform

---

## Measurement Tools

### Lighthouse

```bash
# CLI measurement
npx lighthouse https://example.com --output=json --output-path=./report.json --preset=mobile

# Specific categories only
npx lighthouse https://example.com --only-categories=performance

# Mobile/Desktop switch
npx lighthouse https://example.com --preset=desktop
```

### Web Vitals JavaScript

```javascript
import { onLCP, onINP, onCLS } from 'web-vitals';

function sendToAnalytics(metric) {
  const body = JSON.stringify({
    name: metric.name,
    value: metric.value,
    delta: metric.delta,
    id: metric.id,
    navigationType: metric.navigationType,
  });

  // Send to analytics with Navigator.sendBeacon
  navigator.sendBeacon('/analytics', body);
}

onLCP(sendToAnalytics);
onINP(sendToAnalytics);
onCLS(sendToAnalytics);
```

### Chrome DevTools

```
1. Open DevTools (F12)
2. Go to Performance tab
3. Click Record button to record page load
4. Enable Web Vitals checkbox
5. Each metric appears on timeline
```

### PageSpeed Insights API

```bash
# API measurement
curl "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=https://example.com&key=YOUR_API_KEY&strategy=mobile"
```

---

## Framework-Specific Optimization

### Next.js

```javascript
// next.config.js
module.exports = {
  images: {
    formats: ['image/avif', 'image/webp'],
    deviceSizes: [640, 750, 828, 1080, 1200],
  },
  experimental: {
    optimizeCss: true,
  },
};

// Image component
import Image from 'next/image';

function Hero() {
  return (
    <Image
      src="/hero.jpg"
      alt="Hero"
      width={1200}
      height={600}
      priority // Set for LCP image
      placeholder="blur"
      blurDataURL="data:image/jpeg;base64,..."
    />
  );
}
```

### Nuxt 3+

```javascript
// nuxt.config.ts (Nuxt 3+)
export default defineNuxtConfig({
  modules: ['@nuxt/image'],
  image: {
    format: ['avif', 'webp'],
    screens: { xs: 320, sm: 640, md: 768, lg: 1024, xl: 1280 },
  },
  app: {
    head: {
      link: [
        // Preload the LCP image explicitly; do not rely on HTTP/2 Server Push
        // (removed from Chrome — the `render.http2.push` option of Nuxt 2 no longer exists)
        { rel: 'preload', as: 'image', href: '/hero.webp', fetchpriority: 'high' },
      ],
    },
  },
});
```

```vue
<!-- Mark the LCP image as high priority -->
<template>
  <NuxtImg src="/hero.jpg" width="1200" height="600" preload
           fetchpriority="high" format="avif,webp" alt="Hero" />
</template>
```

---

## Monitoring and Continuous Improvement

### Search Console Monitoring

1. Access Search Console
2. Check "Core Web Vitals" report
3. Identify "Poor" and "Needs Improvement" URLs
4. Analyze individual URLs with PageSpeed Insights

### Alert Setup

```javascript
// Automated monitoring script example
const threshold = {
  LCP: 2500,
  INP: 200,
  CLS: 0.1
};

async function checkWebVitals(url) {
  const response = await fetch(
    `https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=${url}&key=API_KEY`
  );
  const data = await response.json();

  const metrics = data.lighthouseResult.audits;

  if (metrics['largest-contentful-paint'].numericValue > threshold.LCP) {
    sendAlert('LCP exceeds threshold');
  }
  // ... check other metrics similarly
}
```
