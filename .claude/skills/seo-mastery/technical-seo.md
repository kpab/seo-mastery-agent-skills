# 技術SEO リファレンス

技術的なSEO設定の詳細ガイド。クローラビリティ、インデクサビリティ、レンダリングの最適化を網羅。

## robots.txt

### 基本構文

```txt
# すべてのクローラーに適用
User-agent: *
Disallow: /admin/
Disallow: /private/
Allow: /admin/public/

# Googlebotのみに適用
User-agent: Googlebot
Disallow: /temp/

# サイトマップの場所
Sitemap: https://example.com/sitemap.xml
```

### 重要ルール

1. **Disallow はインデックス制御ではない**
   - robots.txt はクロールのブロックのみ
   - インデックス除外には `noindex` メタタグを使用

2. **パス指定の注意点**
   ```txt
   Disallow: /admin   # /admin, /admin/, /admin123 すべてブロック
   Disallow: /admin/  # /admin/ 配下のみブロック
   ```

3. **ワイルドカード使用**
   ```txt
   Disallow: /*.pdf$   # すべてのPDFをブロック
   Disallow: /*/temp/  # 任意のパス下のtemp/をブロック
   ```

### よくある間違い

```txt
# ❌ 間違い: サイト全体をブロック
User-agent: *
Disallow: /

# ❌ 間違い: 重要なリソースをブロック
Disallow: /css/
Disallow: /js/
Disallow: /images/

# ✅ 正しい: 必要最小限のブロック
User-agent: *
Disallow: /admin/
Disallow: /api/internal/
```

---

## XML サイトマップ

### 基本構造

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

### サイトマップインデックス（大規模サイト用）

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

### ベストプラクティス

| 項目 | 推奨 |
|------|------|
| URL数上限 | 50,000 URL / ファイル |
| ファイルサイズ上限 | 50MB（非圧縮） |
| lastmod | 実際の更新日時を正確に記載 |
| priority | 相対的な重要度（0.0-1.0） |
| 送信先 | Google Search Console |

---

## Canonical URL

### 実装方法

```html
<!-- HTMLで指定 -->
<link rel="canonical" href="https://example.com/page/">

<!-- HTTPヘッダーで指定（PDF等に有効） -->
Link: <https://example.com/page/>; rel="canonical"
```

### 使用シナリオ

1. **パラメータ付きURL**
   ```html
   <!-- https://example.com/product?color=red&size=L -->
   <link rel="canonical" href="https://example.com/product">
   ```

2. **www / non-www の統一**
   ```html
   <!-- すべてのページで一貫して使用 -->
   <link rel="canonical" href="https://www.example.com/page/">
   ```

3. **ページネーション**
   ```html
   <!-- 各ページにそのページ自体のcanonicalを設定 -->
   <!-- ページ2の場合 -->
   <link rel="canonical" href="https://example.com/articles?page=2">
   ```

4. **モバイル/PC別URL**
   ```html
   <!-- PC版 -->
   <link rel="canonical" href="https://example.com/page">
   <link rel="alternate" media="only screen and (max-width: 640px)" href="https://m.example.com/page">
   
   <!-- モバイル版 -->
   <link rel="canonical" href="https://example.com/page">
   ```

### 注意点

- canonical は「ヒント」であり強制ではない
- 自己参照canonical を推奨
- 301リダイレクトとの併用が望ましい
- クロスドメインcanonicalは慎重に

---

## hreflang（多言語・多地域対応）

### 基本実装

```html
<link rel="alternate" hreflang="ja" href="https://example.com/ja/">
<link rel="alternate" hreflang="en" href="https://example.com/en/">
<link rel="alternate" hreflang="en-US" href="https://example.com/en-us/">
<link rel="alternate" hreflang="en-GB" href="https://example.com/en-gb/">
<link rel="alternate" hreflang="x-default" href="https://example.com/">
```

### 言語・地域コード

| コード | 意味 |
|--------|------|
| ja | 日本語 |
| en | 英語（地域指定なし） |
| en-US | アメリカ英語 |
| en-GB | イギリス英語 |
| zh-Hans | 簡体字中国語 |
| zh-Hant | 繁体字中国語 |
| x-default | デフォルト / 言語セレクター |

### サイトマップでの指定

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xhtml="http://www.w3.org/1999/xhtml">
  <url>
    <loc>https://example.com/ja/</loc>
    <xhtml:link rel="alternate" hreflang="ja" href="https://example.com/ja/"/>
    <xhtml:link rel="alternate" hreflang="en" href="https://example.com/en/"/>
    <xhtml:link rel="alternate" hreflang="x-default" href="https://example.com/"/>
  </url>
</urlset>
```

### 重要ルール

1. **双方向リンク必須**
   - 日本語ページ → 英語ページ
   - 英語ページ → 日本語ページ
   - 両方に設定がないとGoogleは無視する

2. **自己参照を含める**
   - 現在のページも hreflang に含める

3. **x-default の使用**
   - 該当する言語がない場合のフォールバック
   - 言語選択ページにも使用

---

## JavaScript SEO

### Google のレンダリングプロセス

```
1. クロール (HTML取得)
      ↓
2. レンダリングキュー待機 (数秒〜数日)
      ↓
3. レンダリング (JS実行)
      ↓
4. インデックス登録
```

### ベストプラクティス

**サーバーサイドレンダリング（SSR）推奨ケース:**
- コンテンツがSEO的に重要
- 頻繁に更新されるコンテンツ
- ソーシャルシェア用のメタタグが必要

**実装パターン:**

```javascript
// Next.js での SSR
export async function getServerSideProps() {
  const data = await fetchData();
  return { props: { data } };
}

// Nuxt.js での SSR
export default {
  async asyncData({ $axios }) {
    const data = await $axios.$get('/api/data');
    return { data };
  }
}
```

### リンクの実装

```html
<!-- ✅ クローラブル -->
<a href="/page">Link</a>
<a href="https://example.com/page">Link</a>

<!-- ❌ クローラブルでない可能性 -->
<a onclick="goto('/page')">Link</a>
<span onclick="navigate('/page')">Link</span>
<a href="javascript:void(0)">Link</a>
```

### 遅延読み込みコンテンツ

```html
<!-- ✅ ネイティブ lazy loading（Googlebot対応） -->
<img src="image.jpg" loading="lazy" alt="説明">

<!-- ❌ スクロールトリガーの動的読み込み -->
<div data-src="/content" class="load-on-scroll"></div>
```

---

## HTTPステータスコード

### SEO関連の主要コード

| コード | 意味 | SEOへの影響 |
|--------|------|-------------|
| 200 | 成功 | 正常にインデックス |
| 301 | 恒久的リダイレクト | リンク評価を転送 |
| 302 | 一時的リダイレクト | リンク評価は元URLに保持 |
| 304 | 未更新 | クロール効率向上 |
| 404 | ページなし | インデックスから削除 |
| 410 | 完全に削除済み | 404より早くインデックス削除 |
| 500 | サーバーエラー | 一時的なら問題なし、継続するとインデックス低下 |
| 503 | サービス利用不可 | メンテナンス時に使用 |

### リダイレクトの使い分け

```nginx
# 301: ドメイン変更、恒久的なURL変更
server {
    server_name old-domain.com;
    return 301 https://new-domain.com$request_uri;
}

# 302: A/Bテスト、一時的なメンテナンス
location /old-page {
    return 302 /new-page;
}
```

---

## クロールバジェット最適化

### クロールバジェットとは
Googlebotがサイトをクロールする「予算」（時間・リソース）

### 最適化のポイント

1. **不要なページをブロック**
   ```txt
   # robots.txt
   Disallow: /search?
   Disallow: /filter?
   Disallow: /tag/*
   ```

2. **重複コンテンツの整理**
   - canonical設定
   - パラメータハンドリング（Search Console）

3. **サーバーレスポンス高速化**
   - TTFB 200ms以下目標
   - キャッシュ活用

4. **内部リンク最適化**
   - 重要ページへのリンクを増やす
   - 深い階層を避ける（3クリック以内）

5. **サイトマップ更新**
   - 新規・更新ページを優先
   - 削除済みページを除外

---

## モバイルファーストインデックス

### チェックリスト

- [ ] レスポンシブデザイン または 動的配信 を採用
- [ ] モバイル版に同じコンテンツが存在
- [ ] 同じ構造化データがモバイル版に存在
- [ ] 同じメタタグ（title, description）がモバイル版に存在
- [ ] 画像・動画がモバイル版で適切に表示
- [ ] モバイル版でリソースがブロックされていない

### レスポンシブデザイン設定

```html
<!-- ビューポート設定 -->
<meta name="viewport" content="width=device-width, initial-scale=1">

<!-- レスポンシブ画像 -->
<picture>
  <source media="(max-width: 640px)" srcset="small.webp">
  <source media="(max-width: 1024px)" srcset="medium.webp">
  <img src="large.webp" alt="説明">
</picture>
```

---

## HTTPS / セキュリティ

### 必須設定

```nginx
# HTTPからHTTPSへリダイレクト
server {
    listen 80;
    server_name example.com;
    return 301 https://$server_name$request_uri;
}

# HSTS設定
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
```

### SEOへの影響

- HTTPS はランキングシグナル（軽微だが正の影響）
- Chrome で「保護されていない通信」警告を回避
- HTTP/2 利用可能（パフォーマンス向上）

---

## デバッグ用コマンド集

```bash
# robots.txt確認
curl -s https://example.com/robots.txt

# HTTPヘッダー確認
curl -I https://example.com/

# canonical / hreflang 抽出
curl -s https://example.com/ | grep -E 'rel="canonical"|hreflang'

# リダイレクトチェーン確認
curl -L -v https://example.com/ 2>&1 | grep -E 'Location:|< HTTP'

# レンダリング後のHTML取得（Puppeteer使用）
npx puppeteer screenshot https://example.com --fullPage
```
