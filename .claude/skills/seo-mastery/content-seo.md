# コンテンツSEO リファレンス

検索エンジンとユーザー双方に最適化されたコンテンツ作成ガイド。

## メタタグ最適化

### title タグ

```html
<title>主要キーワード - サブキーワード | サイト名</title>
```

**ベストプラクティス:**

| 項目 | 推奨 |
|------|------|
| 文字数 | 30〜60文字（日本語） |
| キーワード位置 | 先頭に配置 |
| ユニーク性 | 各ページで固有のタイトル |
| ブランド名 | 末尾に「| サイト名」 |
| 区切り文字 | `-` `|` `–` を使用 |

**パターン別テンプレート:**

```html
<!-- 記事ページ -->
<title>【2025年版】SEO対策の完全ガイド - 初心者でもわかる基礎から実践まで | サイト名</title>

<!-- 商品ページ -->
<title>商品名 - カテゴリ | ショップ名 【公式】</title>

<!-- カテゴリページ -->
<title>カテゴリ名の商品一覧 | ショップ名</title>

<!-- トップページ -->
<title>サイト名 | キャッチコピー（サービスの要約）</title>
```

**避けるべきパターン:**

```html
<!-- ❌ キーワード詰め込み -->
<title>SEO SEO対策 SEO最適化 SEOツール SEO会社</title>

<!-- ❌ 同じタイトルの重複使用 -->
<title>サイト名</title> <!-- 全ページ同じ -->

<!-- ❌ 長すぎるタイトル -->
<title>2025年最新版SEO対策完全ガイド初心者から上級者まで使える実践テクニック集Google検索エンジン最適化の極意</title>
```

---

### meta description

```html
<meta name="description" content="ページの説明文。120文字程度で要約。">
```

**ベストプラクティス:**

| 項目 | 推奨 |
|------|------|
| 文字数 | 80〜120文字（日本語） |
| 内容 | ページ内容の正確な要約 |
| CTA | 「詳しくはこちら」等のアクション誘導 |
| キーワード | 自然に含める（太字表示される） |

**良い例:**

```html
<meta name="description" content="SEO対策の基礎から実践までを解説。クロール最適化、構造化データ、Core Web Vitalsの改善方法を具体例付きで紹介します。">
```

**悪い例:**

```html
<!-- ❌ キーワードの羅列 -->
<meta name="description" content="SEO、SEO対策、Google、検索エンジン、最適化、ランキング、上位表示">

<!-- ❌ 内容と無関係 -->
<meta name="description" content="当社は1990年創業の老舗企業です。お客様満足度No.1を目指しています。">
```

---

### OGP / Twitter Card

```html
<!-- Open Graph Protocol -->
<meta property="og:title" content="ページタイトル">
<meta property="og:description" content="ページの説明">
<meta property="og:type" content="article">
<meta property="og:url" content="https://example.com/page/">
<meta property="og:image" content="https://example.com/ogp-image.jpg">
<meta property="og:site_name" content="サイト名">
<meta property="og:locale" content="ja_JP">

<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@username">
<meta name="twitter:title" content="ページタイトル">
<meta name="twitter:description" content="ページの説明">
<meta name="twitter:image" content="https://example.com/twitter-image.jpg">
```

**OGP画像サイズ:**

| プラットフォーム | 推奨サイズ |
|------------------|------------|
| Facebook | 1200 x 630px |
| Twitter | 1200 x 628px |
| LinkedIn | 1200 x 627px |
| LINE | 1200 x 630px |

---

## 見出し構造（H1-H6）

### 正しい階層構造

```html
<h1>メインタイトル（1ページに1つ）</h1>

<h2>大見出し1</h2>
<p>本文...</p>

<h3>中見出し1-1</h3>
<p>本文...</p>

<h3>中見出し1-2</h3>
<p>本文...</p>

<h2>大見出し2</h2>
<p>本文...</p>

<h3>中見出し2-1</h3>
<p>本文...</p>

<h4>小見出し2-1-1</h4>
<p>本文...</p>
```

**ルール:**

1. **H1 は1ページに1つ**
2. **階層をスキップしない**（H1 → H3 は ❌）
3. **論理的な構造を維持**
4. **キーワードを自然に含める**

**悪い例:**

```html
<!-- ❌ 階層スキップ -->
<h1>タイトル</h1>
<h3>いきなりH3</h3>

<!-- ❌ H1が複数 -->
<h1>タイトル1</h1>
<h1>タイトル2</h1>

<!-- ❌ デザイン目的での使用 -->
<h2 style="font-size: 14px;">小さいテキストをH2で...</h2>
```

---

## コンテンツ品質

### E-E-A-T を意識した構成

**Experience（経験）:**
```html
<!-- 実体験を示す表現 -->
<p>実際に3ヶ月間このツールを使用して検証した結果、
以下のような効果が得られました。</p>

<!-- 写真・スクリーンショット -->
<figure>
  <img src="実際の使用画面.jpg" alt="ツールの管理画面">
  <figcaption>実際の管理画面（2025年1月時点）</figcaption>
</figure>
```

**Expertise（専門性）:**
```html
<!-- 著者情報 -->
<div class="author-bio">
  <img src="author.jpg" alt="著者名">
  <p><strong>著者名</strong> - SEOコンサルタント</p>
  <p>10年以上のSEO経験。Google認定パートナー。
  これまで200社以上の企業のSEO支援を実施。</p>
  <a href="/author/profile">著者プロフィール</a>
</div>
```

**Authoritativeness（権威性）:**
```html
<!-- 引用・出典の明記 -->
<blockquote cite="https://developers.google.com/search">
  <p>「高品質なコンテンツを作成することが、検索結果で上位表示される
  最も重要な要因の一つです。」</p>
  <footer>— Google Search Central</footer>
</blockquote>
```

**Trustworthiness（信頼性）:**
```html
<!-- 更新日の明記 -->
<time datetime="2025-01-15">最終更新: 2025年1月15日</time>

<!-- ファクトチェック -->
<p>この記事は<a href="/author/expert">専門家名</a>が監修しています。</p>

<!-- 情報源の開示 -->
<section class="sources">
  <h2>参考文献</h2>
  <ul>
    <li><a href="...">Google Search Central Documentation</a></li>
    <li><a href="...">Web.dev - Core Web Vitals</a></li>
  </ul>
</section>
```

---

## 内部リンク戦略

### アンカーテキストのベストプラクティス

```html
<!-- ✅ 良い例：説明的なアンカーテキスト -->
<p>詳しくは<a href="/seo-guide">SEO対策の基礎ガイド</a>をご覧ください。</p>

<!-- ✅ 良い例：コンテキストが明確 -->
<p>Core Web Vitalsの改善については、
<a href="/core-web-vitals">LCP・INP・CLSの最適化方法</a>で解説しています。</p>

<!-- ❌ 悪い例：汎用的すぎる -->
<p>詳しくは<a href="/seo-guide">こちら</a>をご覧ください。</p>
<p><a href="/core-web-vitals">クリックしてください</a></p>

<!-- ❌ 悪い例：過度なキーワード -->
<p><a href="/seo-guide">SEO SEO対策 Google SEO 検索エンジン最適化</a></p>
```

### リンク構造の設計

```
トップページ
├── カテゴリA
│   ├── 記事A-1 ← サイロ構造内でリンク
│   ├── 記事A-2
│   └── 記事A-3
├── カテゴリB
│   ├── 記事B-1
│   └── 記事B-2
└── 重要ページ（複数カテゴリからリンク）
```

**実装のポイント:**

1. **重要ページへのリンク増加**
   - サイドバー、フッターからリンク
   - 関連記事セクションで紹介

2. **サイロ構造の活用**
   - 同カテゴリ内でのリンクを優先
   - カテゴリをまたぐリンクは戦略的に

3. **孤立ページの防止**
   - すべてのページに最低1つの内部リンク
   - パンくずリストで階層を明示

---

## 画像最適化

### alt属性

```html
<!-- ✅ 良い例：具体的で説明的 -->
<img src="chart.png" alt="2024年のSEOトレンドを示す棒グラフ。AIコンテンツが40%で1位">

<!-- ✅ 良い例：商品画像 -->
<img src="product.jpg" alt="Apple MacBook Pro 14インチ M3チップ シルバー">

<!-- ❌ 悪い例：キーワード詰め込み -->
<img src="chart.png" alt="SEO SEO対策 Google 検索エンジン 最適化 グラフ 統計">

<!-- ❌ 悪い例：説明不足 -->
<img src="chart.png" alt="グラフ">
<img src="product.jpg" alt="商品画像">

<!-- 装飾画像はalt空欄 -->
<img src="decorative-line.png" alt="">
```

### ファイル名

```
✅ 良い例:
seo-trends-2024-chart.webp
macbook-pro-14-m3-silver.jpg

❌ 悪い例:
IMG_1234.jpg
screenshot-2025-01-15.png
image1.webp
```

### 画像形式の選択

| 形式 | 用途 | 圧縮 |
|------|------|------|
| WebP | 写真、イラスト全般 | 非可逆/可逆 |
| AVIF | 次世代（高圧縮） | 非可逆/可逆 |
| PNG | 透過が必要な画像 | 可逆 |
| SVG | ロゴ、アイコン | ベクター |
| JPEG | レガシーサポート | 非可逆 |

### レスポンシブ画像

```html
<picture>
  <source media="(min-width: 1024px)" srcset="large.webp" type="image/webp">
  <source media="(min-width: 640px)" srcset="medium.webp" type="image/webp">
  <source srcset="small.webp" type="image/webp">
  <img src="fallback.jpg" alt="説明" width="800" height="600" loading="lazy">
</picture>
```

---

## URL設計

### ベストプラクティス

```
✅ 良い例:
https://example.com/seo/technical-guide
https://example.com/products/laptop/macbook-pro
https://example.com/blog/2025/01/seo-trends

❌ 悪い例:
https://example.com/p?id=12345
https://example.com/category1/subcategory2/page
https://example.com/seo-seo-optimization-guide-tips-tricks
```

**ルール:**

| 項目 | 推奨 |
|------|------|
| 長さ | 50〜60文字以内 |
| 区切り文字 | ハイフン `-` を使用 |
| 文字 | 小文字英数字のみ |
| 階層 | 3階層以内 |
| キーワード | 主要キーワードを含む |

### 避けるべきパターン

```
# アンダースコア
example.com/seo_guide ❌
example.com/seo-guide ✅

# 大文字混在
example.com/SEO-Guide ❌
example.com/seo-guide ✅

# 不要なパラメータ
example.com/page?session=abc123 ❌

# 日本語URL
example.com/SEO対策 △（エンコードで長くなる）
```

---

## コンテンツ更新戦略

### 更新すべきコンテンツの特定

1. **トラフィック減少ページ**
   - 過去3〜6ヶ月で20%以上減少
   
2. **古い情報を含むページ**
   - 日付、統計データ、ツールのバージョン

3. **検索順位が下降したページ**
   - 上位10位 → 20位以下に下降

4. **CTR が低いページ**
   - 表示回数に対してクリック率が低い

### 更新のベストプラクティス

```html
<!-- 更新日を明記 -->
<meta property="article:modified_time" content="2025-01-15T10:30:00+09:00">

<!-- 本文にも表示 -->
<p class="last-updated">
  <time datetime="2025-01-15">最終更新: 2025年1月15日</time>
  （初回公開: 2024年6月1日）
</p>

<!-- 更新履歴を記載 -->
<details>
  <summary>更新履歴</summary>
  <ul>
    <li>2025-01-15: 2025年のトレンドを追加</li>
    <li>2024-10-01: Core Web Vitals情報を更新</li>
    <li>2024-06-01: 初回公開</li>
  </ul>
</details>
```

---

## 検索意図（Search Intent）

### 4つの検索意図タイプ

| タイプ | 意図 | 例 | 最適コンテンツ |
|--------|------|-----|----------------|
| Informational | 情報を知りたい | 「SEOとは」 | 解説記事、ガイド |
| Navigational | 特定サイトに行きたい | 「Gmail ログイン」 | ブランドページ |
| Commercial | 購入前に比較検討 | 「SEOツール おすすめ」 | 比較記事、レビュー |
| Transactional | 購入・申込したい | 「SEOツール 申込」 | 商品・サービスページ |

### 検索意図に合わせたコンテンツ設計

**Informational の例:**
```markdown
# SEOとは？初心者でもわかる基礎知識

## SEOの定義
SEO（Search Engine Optimization）とは...

## なぜSEOが重要なのか
1. 継続的なトラフィック獲得
2. 広告費の削減
3. ブランド認知度向上

## SEOの基本要素
### 技術SEO
...
### コンテンツSEO
...
```

**Commercial の例:**
```markdown
# 【2025年版】SEOツール比較10選

| ツール名 | 価格 | 機能 | おすすめ度 |
|----------|------|------|------------|
| ツールA | ¥10,000/月 | ... | ★★★★★ |
| ツールB | ¥5,000/月 | ... | ★★★★☆ |

## 各ツールの詳細レビュー
### ツールA
実際に使ってみた感想...
```
