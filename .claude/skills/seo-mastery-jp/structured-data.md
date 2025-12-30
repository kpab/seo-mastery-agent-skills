# 構造化データ リファレンス

Google検索のリッチリザルトに対応する構造化データの実装ガイド。JSON-LD形式を推奨。

## 実装の基本

### JSON-LD の配置

```html
<head>
  <!-- headまたはbody内に配置可能 -->
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "記事タイトル"
  }
  </script>
</head>
```

### 複数の構造化データ

```html
<!-- 方法1: 複数のscriptタグ -->
<script type="application/ld+json">
{ "@type": "Article", ... }
</script>
<script type="application/ld+json">
{ "@type": "BreadcrumbList", ... }
</script>

<!-- 方法2: @graphで統合（推奨） -->
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

## Article（記事）

### NewsArticle

```json
{
  "@context": "https://schema.org",
  "@type": "NewsArticle",
  "headline": "ニュース記事のタイトル（最大110文字）",
  "description": "記事の要約",
  "image": [
    "https://example.com/photos/1x1/photo.jpg",
    "https://example.com/photos/4x3/photo.jpg",
    "https://example.com/photos/16x9/photo.jpg"
  ],
  "datePublished": "2025-01-15T08:00:00+09:00",
  "dateModified": "2025-01-15T10:30:00+09:00",
  "author": [{
    "@type": "Person",
    "name": "著者名",
    "url": "https://example.com/author/profile",
    "sameAs": [
      "https://twitter.com/author",
      "https://www.linkedin.com/in/author"
    ]
  }],
  "publisher": {
    "@type": "Organization",
    "name": "メディア名",
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
  "headline": "ブログ記事のタイトル",
  "description": "記事の要約",
  "image": "https://example.com/blog-image.jpg",
  "datePublished": "2025-01-15T08:00:00+09:00",
  "dateModified": "2025-01-15T10:30:00+09:00",
  "author": {
    "@type": "Person",
    "name": "著者名"
  },
  "wordCount": 2500,
  "keywords": ["SEO", "コンテンツマーケティング", "Google"]
}
```

---

## FAQ（よくある質問）

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "SEOとは何ですか？",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "SEO（Search Engine Optimization）とは、検索エンジン最適化のことです。Webサイトを検索エンジンに適切に評価してもらい、検索結果の上位に表示させるための施策を指します。"
      }
    },
    {
      "@type": "Question",
      "name": "SEO対策にはどのくらい時間がかかりますか？",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "一般的に、SEO対策の効果が現れるまでには3〜6ヶ月程度かかります。競争の激しいキーワードでは1年以上かかることもあります。"
      }
    },
    {
      "@type": "Question",
      "name": "SEO対策は自分でできますか？",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "基本的なSEO対策は自分で行うことができます。メタタグの最適化、コンテンツの改善、内部リンクの整備などは専門知識がなくても取り組めます。ただし、技術的な問題や競争が激しい分野では専門家の支援が有効です。"
      }
    }
  ]
}
```

---

## HowTo（ハウツー）

```json
{
  "@context": "https://schema.org",
  "@type": "HowTo",
  "name": "robots.txtの設定方法",
  "description": "Webサイトのrobots.txtファイルを正しく設定する手順を解説します。",
  "image": "https://example.com/howto-image.jpg",
  "totalTime": "PT15M",
  "estimatedCost": {
    "@type": "MonetaryAmount",
    "currency": "JPY",
    "value": "0"
  },
  "tool": [
    {
      "@type": "HowToTool",
      "name": "テキストエディタ"
    },
    {
      "@type": "HowToTool",
      "name": "FTPクライアント"
    }
  ],
  "step": [
    {
      "@type": "HowToStep",
      "name": "robots.txtファイルを作成",
      "text": "テキストエディタを開き、新規ファイルを作成します。",
      "image": "https://example.com/step1.jpg",
      "url": "https://example.com/howto#step1"
    },
    {
      "@type": "HowToStep",
      "name": "ルールを記述",
      "text": "User-agent: *とDisallow: /admin/のようにクロール制御ルールを記述します。",
      "image": "https://example.com/step2.jpg",
      "url": "https://example.com/howto#step2"
    },
    {
      "@type": "HowToStep",
      "name": "サーバーにアップロード",
      "text": "FTPクライアントを使用して、ルートディレクトリにrobots.txtをアップロードします。",
      "image": "https://example.com/step3.jpg",
      "url": "https://example.com/howto#step3"
    }
  ]
}
```

---

## Product（商品）

```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "SEO分析ツール Pro",
  "image": [
    "https://example.com/product-1x1.jpg",
    "https://example.com/product-4x3.jpg",
    "https://example.com/product-16x9.jpg"
  ],
  "description": "包括的なSEO分析機能を備えたプロフェッショナル向けツール。キーワード調査、競合分析、サイト監査機能を搭載。",
  "sku": "SEO-PRO-001",
  "mpn": "925872",
  "brand": {
    "@type": "Brand",
    "name": "SEO Tools Inc."
  },
  "offers": {
    "@type": "Offer",
    "url": "https://example.com/product/seo-pro",
    "priceCurrency": "JPY",
    "price": "9800",
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
        "currency": "JPY"
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
        "name": "田中太郎"
      },
      "datePublished": "2025-01-10",
      "reviewBody": "非常に使いやすく、SEO分析が効率的に行えます。"
    }
  ]
}
```

---

## LocalBusiness（ローカルビジネス）

```json
{
  "@context": "https://schema.org",
  "@type": "Restaurant",
  "name": "寿司 太郎",
  "image": [
    "https://example.com/store-1x1.jpg",
    "https://example.com/store-4x3.jpg",
    "https://example.com/store-16x9.jpg"
  ],
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "中区本町1-2-3",
    "addressLocality": "横浜市",
    "addressRegion": "神奈川県",
    "postalCode": "231-0005",
    "addressCountry": "JP"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": 35.4437,
    "longitude": 139.6380
  },
  "url": "https://example.com/",
  "telephone": "+81-45-123-4567",
  "priceRange": "¥¥¥",
  "servesCuisine": "寿司",
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

## BreadcrumbList（パンくずリスト）

```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "ホーム",
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
      "name": "技術SEO",
      "item": "https://example.com/seo/technical/"
    },
    {
      "@type": "ListItem",
      "position": 4,
      "name": "robots.txtガイド"
    }
  ]
}
```

**注意:** 最後の項目（現在のページ）には `item` プロパティを省略可能。

---

## VideoObject（動画）

### 基本実装

```json
{
  "@context": "https://schema.org",
  "@type": "VideoObject",
  "name": "SEO入門講座 - 第1回",
  "description": "SEOの基礎知識を15分で解説します。クロール、インデックス、ランキングの仕組みを理解しましょう。",
  "thumbnailUrl": [
    "https://example.com/thumb-1x1.jpg",
    "https://example.com/thumb-4x3.jpg",
    "https://example.com/thumb-16x9.jpg"
  ],
  "uploadDate": "2025-01-15T08:00:00+09:00",
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

### ライブ配信（LIVE badge）

```json
{
  "@context": "https://schema.org",
  "@type": "VideoObject",
  "name": "SEOウェビナー LIVE",
  "description": "リアルタイムでSEOの最新トレンドを解説",
  "thumbnailUrl": "https://example.com/live-thumb.jpg",
  "uploadDate": "2025-01-20T19:00:00+09:00",
  "publication": {
    "@type": "BroadcastEvent",
    "isLiveBroadcast": true,
    "startDate": "2025-01-20T19:00:00+09:00",
    "endDate": "2025-01-20T20:30:00+09:00"
  }
}
```

### キーモーメント（Clip）

```json
{
  "@context": "https://schema.org",
  "@type": "VideoObject",
  "name": "SEO完全ガイド",
  "description": "60分でSEOを完全マスター",
  "thumbnailUrl": "https://example.com/thumb.jpg",
  "uploadDate": "2025-01-15T08:00:00+09:00",
  "duration": "PT60M",
  "hasPart": [
    {
      "@type": "Clip",
      "name": "イントロダクション",
      "startOffset": 0,
      "endOffset": 120,
      "url": "https://example.com/video?t=0"
    },
    {
      "@type": "Clip",
      "name": "技術SEOの基礎",
      "startOffset": 120,
      "endOffset": 900,
      "url": "https://example.com/video?t=120"
    },
    {
      "@type": "Clip",
      "name": "コンテンツ最適化",
      "startOffset": 900,
      "endOffset": 1800,
      "url": "https://example.com/video?t=900"
    },
    {
      "@type": "Clip",
      "name": "リンク戦略",
      "startOffset": 1800,
      "endOffset": 2700,
      "url": "https://example.com/video?t=1800"
    },
    {
      "@type": "Clip",
      "name": "まとめとQ&A",
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
  "name": "株式会社SEOマスター",
  "alternateName": "SEO Master Inc.",
  "url": "https://example.com/",
  "logo": "https://example.com/logo.png",
  "contactPoint": {
    "@type": "ContactPoint",
    "telephone": "+81-3-1234-5678",
    "contactType": "customer service",
    "areaServed": "JP",
    "availableLanguage": ["Japanese", "English"]
  },
  "sameAs": [
    "https://twitter.com/seomaster",
    "https://www.facebook.com/seomaster",
    "https://www.linkedin.com/company/seomaster"
  ]
}
```

### WebSite（サイト内検索）

```json
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "SEO Master",
  "url": "https://example.com/",
  "potentialAction": {
    "@type": "SearchAction",
    "target": {
      "@type": "EntryPoint",
      "urlTemplate": "https://example.com/search?q={search_term_string}"
    },
    "query-input": "required name=search_term_string"
  }
}
```

---

## Event（イベント）

```json
{
  "@context": "https://schema.org",
  "@type": "Event",
  "name": "SEOカンファレンス 2025",
  "description": "国内最大級のSEOカンファレンス。最新トレンドと実践テクニックを学べます。",
  "image": "https://example.com/event-image.jpg",
  "startDate": "2025-03-15T10:00:00+09:00",
  "endDate": "2025-03-15T18:00:00+09:00",
  "eventStatus": "https://schema.org/EventScheduled",
  "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
  "location": {
    "@type": "Place",
    "name": "東京国際フォーラム",
    "address": {
      "@type": "PostalAddress",
      "streetAddress": "丸の内3-5-1",
      "addressLocality": "千代田区",
      "addressRegion": "東京都",
      "postalCode": "100-0005",
      "addressCountry": "JP"
    }
  },
  "performer": {
    "@type": "Person",
    "name": "SEO専門家 山田太郎"
  },
  "organizer": {
    "@type": "Organization",
    "name": "SEO Master Inc.",
    "url": "https://example.com/"
  },
  "offers": {
    "@type": "Offer",
    "url": "https://example.com/event/register",
    "price": "15000",
    "priceCurrency": "JPY",
    "availability": "https://schema.org/InStock",
    "validFrom": "2025-01-01T00:00:00+09:00"
  }
}
```

---

## 検証ツール

### Rich Results Test
https://search.google.com/test/rich-results

```bash
# CLI での検証（Puppeteer使用）
npx puppeteer screenshot "https://search.google.com/test/rich-results?url=https://example.com"
```

### Schema Markup Validator
https://validator.schema.org/

### よくあるエラーと対処

| エラー | 原因 | 対処法 |
|--------|------|--------|
| Missing field | 必須フィールドの欠落 | 必須プロパティを追加 |
| Invalid URL | URLの形式が不正 | 完全なURLを指定 |
| Invalid date | 日付形式が不正 | ISO 8601形式を使用 |
| Image too small | 画像が小さすぎる | 最低1200pxを確保 |
| Unsupported type | 非対応のタイプ | 対応タイプを確認 |

---

## ベストプラクティス

1. **JSON-LD を使用**（Microdata/RDFaより推奨）
2. **テスト環境で検証**してから本番デプロイ
3. **ページ内容と一致**する情報のみマークアップ
4. **定期的な検証**（Search Consoleで監視）
5. **過度なマークアップを避ける**（スパム判定リスク）
