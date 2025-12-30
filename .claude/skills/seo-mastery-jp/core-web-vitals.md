# Core Web Vitals リファレンス

Googleのランキング要因となるCore Web Vitalsの詳細な最適化ガイド。

## 概要

Core Web Vitalsは、ユーザー体験を測定する3つの主要指標です。

| 指標 | 測定内容 | 良好 | 改善が必要 | 不良 |
|------|----------|------|------------|------|
| LCP | 読み込み速度 | ≤ 2.5秒 | 2.5-4秒 | > 4秒 |
| INP | インタラクティブ性 | ≤ 200ms | 200-500ms | > 500ms |
| CLS | 視覚的安定性 | ≤ 0.1 | 0.1-0.25 | > 0.25 |

---

## LCP（Largest Contentful Paint）

### LCPとは
ビューポート内で最も大きなコンテンツ要素が表示されるまでの時間。

**LCP要素の候補:**
- `<img>`要素
- `<svg>`内の`<image>`要素
- `<video>`要素（ポスター画像）
- `background-image`を持つ要素
- テキストを含むブロックレベル要素

### 主な原因と対策

#### 1. 遅いサーバーレスポンス

**診断:**
```bash
# TTFB (Time to First Byte) の測定
curl -o /dev/null -s -w "TTFB: %{time_starttransfer}s\n" https://example.com/
```

**対策:**
```nginx
# Nginxでのキャッシュ設定
proxy_cache_path /tmp/nginx levels=1:2 keys_zone=my_cache:10m max_size=1g;

location / {
    proxy_cache my_cache;
    proxy_cache_valid 200 60m;
    proxy_cache_use_stale error timeout http_500 http_502 http_503 http_504;
}
```

```javascript
// CDN (Cloudflare) の設定例
// Cache-Control ヘッダー
res.setHeader('Cache-Control', 'public, max-age=31536000, immutable');
```

#### 2. レンダーブロッキングリソース

**診断:**
```html
<!-- ブロッキングリソースの例 -->
<link rel="stylesheet" href="styles.css"> <!-- ブロッキング -->
<script src="app.js"></script> <!-- ブロッキング -->
```

**対策:**

```html
<!-- Critical CSSのインライン化 -->
<style>
  /* ファーストビューに必要な最小限のCSS */
  .hero { ... }
  .nav { ... }
</style>

<!-- 非クリティカルCSSの遅延読み込み -->
<link rel="preload" href="styles.css" as="style" onload="this.onload=null;this.rel='stylesheet'">
<noscript><link rel="stylesheet" href="styles.css"></noscript>

<!-- JavaScriptの遅延実行 -->
<script src="app.js" defer></script>
<!-- または -->
<script src="analytics.js" async></script>
```

#### 3. 遅い画像読み込み

**対策:**

```html
<!-- LCP画像のプリロード -->
<link rel="preload" as="image" href="hero.webp" fetchpriority="high">

<!-- 最適な画像形式 -->
<picture>
  <source srcset="hero.avif" type="image/avif">
  <source srcset="hero.webp" type="image/webp">
  <img src="hero.jpg" alt="ヒーロー画像" 
       width="1200" height="600"
       fetchpriority="high"
       decoding="async">
</picture>

<!-- レスポンシブ画像 -->
<img srcset="hero-400.webp 400w,
             hero-800.webp 800w,
             hero-1200.webp 1200w"
     sizes="(max-width: 600px) 400px,
            (max-width: 1000px) 800px,
            1200px"
     src="hero-1200.webp"
     alt="説明">
```

#### 4. クライアントサイドレンダリング

**対策:**

```javascript
// Next.js: SSRの実装
export async function getServerSideProps() {
  const data = await fetchData();
  return { props: { data } };
}

// Next.js: SSGの実装
export async function getStaticProps() {
  const data = await fetchData();
  return { 
    props: { data },
    revalidate: 3600 // 1時間ごとに再生成
  };
}
```

### LCP最適化チェックリスト

- [ ] TTFBが200ms以下
- [ ] LCP画像がプリロードされている
- [ ] 画像がWebP/AVIF形式
- [ ] クリティカルCSSがインライン化
- [ ] 不要なJavaScriptが遅延読み込み
- [ ] CDNを使用している
- [ ] サーバーキャッシュが適切に設定

---

## INP（Interaction to Next Paint）

### INPとは
ユーザーのインタラクション（クリック、タップ、キー入力）から次のペイントまでの遅延時間。

**FIDとの違い:**
- FID: 最初のインタラクションのみ測定
- INP: ページ滞在中のすべてのインタラクションを測定

### 主な原因と対策

#### 1. 重いJavaScript実行

**診断:**
```javascript
// 長いタスクの検出
const observer = new PerformanceObserver((list) => {
  for (const entry of list.getEntries()) {
    console.log('Long Task:', entry.duration, 'ms');
  }
});
observer.observe({ entryTypes: ['longtask'] });
```

**対策: タスクの分割**

```javascript
// ❌ メインスレッドをブロック
function processItems(items) {
  items.forEach(item => heavyProcess(item));
}

// ✅ yieldを使用してメインスレッドに制御を返す
async function processItemsAsync(items) {
  for (const item of items) {
    heavyProcess(item);
    // メインスレッドに制御を返す
    await new Promise(resolve => setTimeout(resolve, 0));
  }
}

// ✅ scheduler.yield() を使用（Chrome 129+）
async function processItemsWithYield(items) {
  for (const item of items) {
    heavyProcess(item);
    if ('scheduler' in window && 'yield' in scheduler) {
      await scheduler.yield();
    }
  }
}
```

**対策: Web Workerの活用**

```javascript
// メインスレッド
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

#### 2. 大きなDOMサイズ

**診断:**
```javascript
// DOM要素数の確認
console.log('DOM Elements:', document.querySelectorAll('*').length);
```

**対策:**

```javascript
// 仮想スクロールの実装（React例）
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
/* content-visibility による遅延レンダリング */
.below-fold-content {
  content-visibility: auto;
  contain-intrinsic-size: 0 500px;
}
```

#### 3. サードパーティスクリプト

**対策:**

```html
<!-- 遅延読み込み -->
<script>
  // ユーザーインタラクション後に読み込み
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

<!-- Partytown によるワーカー実行 -->
<script type="text/partytown" src="https://analytics.example.com/script.js"></script>
```

### INP最適化チェックリスト

- [ ] 長いタスク（50ms以上）がない
- [ ] イベントハンドラが軽量
- [ ] DOM要素数が1500以下
- [ ] サードパーティスクリプトが遅延読み込み
- [ ] 重い処理はWeb Workerで実行
- [ ] requestIdleCallbackを活用

---

## CLS（Cumulative Layout Shift）

### CLSとは
ページ読み込み中に発生する予期しないレイアウトシフトの累積スコア。

**計算式:**
```
CLS = 影響率 × 距離率
影響率 = シフトした要素の影響面積 / ビューポート面積
距離率 = 移動距離 / ビューポート高さ
```

### 主な原因と対策

#### 1. サイズ未指定の画像・動画

**対策:**

```html
<!-- ✅ width/height属性を指定 -->
<img src="image.jpg" width="800" height="600" alt="説明">

<!-- ✅ CSSでアスペクト比を維持 -->
<style>
  img {
    width: 100%;
    height: auto;
    aspect-ratio: 4 / 3;
  }
</style>

<!-- ✅ 動画の場合 -->
<video width="1280" height="720" poster="poster.jpg">
  <source src="video.mp4" type="video/mp4">
</video>

<!-- ✅ iframeの場合 -->
<div style="position: relative; padding-bottom: 56.25%; height: 0;">
  <iframe 
    src="https://www.youtube.com/embed/xxxxx"
    style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"
    frameborder="0"
    allowfullscreen>
  </iframe>
</div>
```

#### 2. 動的に挿入されるコンテンツ

**対策:**

```html
<!-- ❌ 突然挿入されるバナー -->
<div id="banner-container"></div>
<script>
  fetch('/api/banner').then(...)
</script>

<!-- ✅ 事前にスペースを確保 -->
<div id="banner-container" style="min-height: 250px;">
  <!-- スケルトンUI -->
  <div class="skeleton" style="height: 250px; background: #eee;"></div>
</div>

<!-- ✅ CSSでスペース確保 -->
<style>
  .ad-slot {
    min-height: 250px;
    contain: layout;
  }
</style>
```

#### 3. Webフォント（FOUT/FOIT）

**対策:**

```css
/* font-display: swap を使用 */
@font-face {
  font-family: 'CustomFont';
  src: url('custom-font.woff2') format('woff2');
  font-display: swap;
}

/* size-adjust でフォールバックを調整 */
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
<!-- フォントのプリロード -->
<link rel="preload" href="custom-font.woff2" as="font" type="font/woff2" crossorigin>
```

#### 4. 広告・埋め込みコンテンツ

**対策:**

```html
<!-- 固定サイズのコンテナ -->
<div class="ad-container" style="width: 300px; height: 250px; contain: strict;">
  <!-- 広告スクリプト -->
</div>

<!-- 最小高さの設定 -->
<style>
  .ad-container {
    min-height: 250px;
    background: #f0f0f0;
  }
  
  /* 広告読み込み後 */
  .ad-container.loaded {
    min-height: auto;
  }
</style>
```

### CLS最適化チェックリスト

- [ ] すべての画像にwidth/heightが指定されている
- [ ] 動画・iframeにアスペクト比が設定されている
- [ ] 広告スペースが事前に確保されている
- [ ] Webフォントにfont-display: swapが設定
- [ ] 動的コンテンツにmin-heightが設定
- [ ] アニメーションがtransformを使用

---

## 測定ツール

### Lighthouse

```bash
# CLI での測定
npx lighthouse https://example.com --output=json --output-path=./report.json

# 特定のカテゴリのみ
npx lighthouse https://example.com --only-categories=performance

# モバイル/デスクトップ切り替え
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
  
  // Navigator.sendBeacon でアナリティクスに送信
  navigator.sendBeacon('/analytics', body);
}

onLCP(sendToAnalytics);
onINP(sendToAnalytics);
onCLS(sendToAnalytics);
```

### Chrome DevTools

```
1. DevTools を開く (F12)
2. Performance タブ
3. Record ボタンでページ読み込みを記録
4. Web Vitals チェックボックスを有効化
5. 各指標がタイムラインに表示される
```

### PageSpeed Insights API

```bash
# API での測定
curl "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=https://example.com&key=YOUR_API_KEY&strategy=mobile"
```

---

## フレームワーク別最適化

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

// 画像コンポーネント
import Image from 'next/image';

function Hero() {
  return (
    <Image
      src="/hero.jpg"
      alt="ヒーロー"
      width={1200}
      height={600}
      priority // LCP画像に設定
      placeholder="blur"
      blurDataURL="data:image/jpeg;base64,..."
    />
  );
}
```

### Nuxt.js

```javascript
// nuxt.config.js
export default {
  image: {
    provider: 'ipx',
    screens: {
      xs: 320,
      sm: 640,
      md: 768,
      lg: 1024,
      xl: 1280,
    },
  },
  render: {
    http2: {
      push: true,
      pushAssets: (req, res, publicPath, preloadFiles) =>
        preloadFiles
          .filter(f => f.asType === 'script' || f.asType === 'style')
          .map(f => `<${publicPath}${f.file}>; rel=preload; as=${f.asType}`),
    },
  },
};
```

---

## 監視と継続的改善

### Search Console での監視

1. Search Console にアクセス
2. 「ウェブに関する主な指標」レポートを確認
3. 「不良」「改善が必要」なURLを特定
4. 個別URLをPageSpeed Insightsで詳細分析

### アラート設定

```javascript
// 自動監視スクリプト例
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
  // ... 他の指標も同様にチェック
}
```
