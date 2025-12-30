# SEO監査ワークフロー

サイト全体のSEO監査を実施するための体系的なプロセス。

## 監査の全体像

```
Phase 1: クロール診断（30分）
    ↓
Phase 2: 技術SEO診断（1-2時間）
    ↓
Phase 3: コンテンツ診断（1-2時間）
    ↓
Phase 4: パフォーマンス診断（30分）
    ↓
Phase 5: 競合分析（1時間）
    ↓
Phase 6: 改善計画策定（1時間）
```

---

## Phase 1: クロール診断

### 1.1 robots.txt 確認

```bash
# robots.txt の取得
curl -s https://example.com/robots.txt

# 確認ポイント:
# - 重要ページがDisallowされていないか
# - サイトマップへの参照があるか
# - Crawl-delay が過度に設定されていないか
```

**チェックリスト:**
- [ ] robots.txt が存在する
- [ ] 重要ページ（/, /products/, /services/）がブロックされていない
- [ ] CSS/JS/画像がブロックされていない
- [ ] サイトマップへの参照がある

### 1.2 サイトマップ確認

```bash
# サイトマップの取得
curl -s https://example.com/sitemap.xml | head -100

# URL数の確認
curl -s https://example.com/sitemap.xml | grep -c "<loc>"

# lastmod の確認
curl -s https://example.com/sitemap.xml | grep "<lastmod>" | sort | uniq -c
```

**チェックリスト:**
- [ ] サイトマップが存在する
- [ ] 主要ページがすべて含まれている
- [ ] 404ページが含まれていない
- [ ] lastmod が正確に更新されている
- [ ] Search Console に送信済み

### 1.3 インデックス状況

```bash
# site: 検索でインデックス数を確認
# Google で「site:example.com」を検索

# 特定ディレクトリのインデックス
# site:example.com/blog/
```

**チェックリスト:**
- [ ] インデックス数が想定と一致
- [ ] 重要ページがインデックスされている
- [ ] 不要なページ（管理画面等）がインデックスされていない

---

## Phase 2: 技術SEO診断

### 2.1 HTTPS/セキュリティ

```bash
# SSL証明書の確認
curl -vI https://example.com 2>&1 | grep -E 'SSL|certificate|expire'

# HTTPからのリダイレクト確認
curl -I http://example.com

# Mixed Content の検出
curl -s https://example.com | grep -E 'http://'
```

**チェックリスト:**
- [ ] HTTPS化されている
- [ ] HTTPからHTTPSへ301リダイレクト
- [ ] Mixed Content がない
- [ ] SSL証明書が有効期限内

### 2.2 リダイレクト診断

```bash
# リダイレクトチェーンの確認
curl -L -I https://example.com 2>&1 | grep -E 'HTTP/|Location:'

# wwwの統一確認
curl -I https://www.example.com
curl -I https://example.com
```

**チェックリスト:**
- [ ] リダイレクトチェーンが2ホップ以内
- [ ] 302ではなく301を使用
- [ ] www/non-wwwが統一されている

### 2.3 メタタグ診断

```bash
# メタ情報の抽出
curl -s https://example.com | grep -E '<title>|<meta name="description"|<meta name="robots"|<link rel="canonical"'

# 複数ページを一括チェック（例）
for url in "/" "/about" "/products"; do
  echo "=== $url ==="
  curl -s "https://example.com$url" | grep -E '<title>'
done
```

**チェックリスト:**
- [ ] 各ページにユニークなtitleがある
- [ ] titleが60文字以内
- [ ] meta descriptionが120文字以内
- [ ] canonical URLが正しく設定
- [ ] 不要なnoindex/nofollowがない

### 2.4 構造化データ診断

```bash
# JSON-LD の抽出
curl -s https://example.com | grep -oP '<script type="application/ld\+json">.*?</script>'

# Rich Results Test（ブラウザで確認）
# https://search.google.com/test/rich-results?url=https://example.com
```

**チェックリスト:**
- [ ] 適切な構造化データが実装されている
- [ ] エラーがない（Rich Results Test）
- [ ] ページ内容と一致している

### 2.5 モバイル対応

```bash
# viewport の確認
curl -s https://example.com | grep 'viewport'

# Mobile-Friendly Test（ブラウザで確認）
# https://search.google.com/test/mobile-friendly?url=https://example.com
```

**チェックリスト:**
- [ ] レスポンシブデザインまたは動的配信
- [ ] viewport meta tagが設定
- [ ] タップターゲットが適切なサイズ
- [ ] テキストが読みやすいサイズ

---

## Phase 3: コンテンツ診断

### 3.1 見出し構造

```bash
# 見出しタグの抽出
curl -s https://example.com | grep -oP '<h[1-6][^>]*>.*?</h[1-6]>'

# H1タグの数
curl -s https://example.com | grep -c '<h1'
```

**チェックリスト:**
- [ ] H1タグが1つのみ
- [ ] 見出し階層が論理的（H1→H2→H3）
- [ ] 見出しにキーワードが含まれる

### 3.2 リンク診断

```bash
# 内部リンクの抽出
curl -s https://example.com | grep -oP 'href="[^"]*"' | grep -v 'http' | head -20

# 外部リンクの抽出
curl -s https://example.com | grep -oP 'href="https?://[^"]*"' | grep -v 'example.com'

# リンク切れチェック（簡易版）
curl -s https://example.com | grep -oP 'href="[^"]*"' | while read href; do
  url=$(echo $href | sed 's/href="\(.*\)"/\1/')
  status=$(curl -o /dev/null -s -w "%{http_code}" "$url")
  echo "$status $url"
done
```

**チェックリスト:**
- [ ] 内部リンクが適切に設定
- [ ] アンカーテキストが説明的
- [ ] リンク切れがない
- [ ] 外部リンクに適切なrel属性

### 3.3 画像診断

```bash
# alt属性のチェック
curl -s https://example.com | grep -oP '<img[^>]*>' | grep -v 'alt='

# 画像サイズの確認
curl -s https://example.com | grep -oP '<img[^>]*>' | grep -v 'width\|height'
```

**チェックリスト:**
- [ ] すべての画像にalt属性がある
- [ ] alt属性が説明的（空でない）
- [ ] 画像サイズ（width/height）が指定
- [ ] 適切なフォーマット（WebP等）

### 3.4 コンテンツ品質

**手動チェック:**
- [ ] コンテンツがオリジナル
- [ ] ユーザーの検索意図に合致
- [ ] 十分な情報量がある
- [ ] 定期的に更新されている
- [ ] 著者情報が明記されている

---

## Phase 4: パフォーマンス診断

### 4.1 Core Web Vitals

```bash
# Lighthouse CLI
npx lighthouse https://example.com --output=json --output-path=./report.json --preset=mobile

# 結果の抽出
cat report.json | jq '.audits["largest-contentful-paint"].numericValue'
cat report.json | jq '.audits["cumulative-layout-shift"].numericValue'
```

**チェックリスト:**
- [ ] LCP ≤ 2.5秒
- [ ] INP ≤ 200ms
- [ ] CLS ≤ 0.1
- [ ] パフォーマンススコア ≥ 80

### 4.2 リソース最適化

```bash
# ページサイズの確認
curl -s -o /dev/null -w "%{size_download}\n" https://example.com

# 圧縮の確認
curl -H "Accept-Encoding: gzip, deflate, br" -sI https://example.com | grep -i 'content-encoding'
```

**チェックリスト:**
- [ ] Gzip/Brotli圧縮が有効
- [ ] 画像が最適化されている
- [ ] CSS/JSがミニファイされている
- [ ] 不要なリソースがない

---

## Phase 5: 競合分析

### 5.1 競合特定

**手順:**
1. 主要キーワードで検索
2. 上位5〜10サイトをリストアップ
3. 直接競合と間接競合を分類

### 5.2 比較項目

| 項目 | 自社 | 競合A | 競合B |
|------|------|-------|-------|
| ドメイン年齢 | | | |
| インデックス数 | | | |
| コンテンツ量 | | | |
| 更新頻度 | | | |
| 構造化データ | | | |
| Core Web Vitals | | | |
| 被リンク数 | | | |

### 5.3 ギャップ分析

```markdown
## キーワードギャップ
競合がランキングしているが自社がしていないキーワード:
1. キーワードA（検索ボリューム: X）
2. キーワードB（検索ボリューム: Y）

## コンテンツギャップ
競合にあって自社にないコンテンツタイプ:
1. ハウツーガイド
2. 比較記事
3. ケーススタディ

## 技術ギャップ
競合が実装しているが自社にない機能:
1. FAQ構造化データ
2. サイト内検索
3. 多言語対応
```

---

## Phase 6: 改善計画策定

### 6.1 優先度マトリクス

| 優先度 | 影響度 | 工数 | 施策例 |
|--------|--------|------|--------|
| 🔴 最高 | 高 | 低 | noindex修正、404修正、title重複解消 |
| 🟠 高 | 高 | 中 | 構造化データ追加、メタタグ最適化 |
| 🟡 中 | 中 | 中 | Core Web Vitals改善、コンテンツ追加 |
| 🟢 低 | 低 | 高 | サイト構造変更、ドメイン移行 |

### 6.2 改善レポートテンプレート

```markdown
# SEO監査レポート

## エグゼクティブサマリー
- 監査日: YYYY-MM-DD
- 対象サイト: https://example.com
- 総合評価: B（改善の余地あり）

## 重要な問題点
1. **[緊急] 複数ページでnoindexが設定されている**
   - 影響: 重要ページがインデックスされていない
   - 対策: 該当ページのnoindex削除
   - 工数: 1時間

2. **[高] LCPが4.2秒（目標: 2.5秒以下）**
   - 影響: ユーザー体験とランキングに悪影響
   - 対策: 画像最適化、Critical CSS実装
   - 工数: 8時間

## 改善ロードマップ

### Week 1-2（緊急対応）
- [ ] noindex問題の修正
- [ ] 404ページの修正
- [ ] リダイレクトチェーンの解消

### Week 3-4（技術SEO改善）
- [ ] 構造化データの追加
- [ ] メタタグの最適化
- [ ] サイトマップの更新

### Month 2（パフォーマンス改善）
- [ ] LCP最適化
- [ ] CLS最適化
- [ ] 画像形式の変換

### Month 3（コンテンツ改善）
- [ ] 既存コンテンツの更新
- [ ] 新規コンテンツの追加
- [ ] 内部リンクの最適化

## 期待される効果
- オーガニックトラフィック: +30%（3ヶ月後）
- Core Web Vitals: すべて「良好」判定
- インデックス数: +50ページ
```

---

## 監査ツールリスト

### 無料ツール
- Google Search Console
- Google PageSpeed Insights
- Google Rich Results Test
- Lighthouse
- Chrome DevTools
- Screaming Frog（500 URL まで）

### 有料ツール
- Screaming Frog（有料版）
- Ahrefs / SEMrush
- Moz Pro
- DeepCrawl

### CLI ツール

```bash
# Lighthouse CLI
npm install -g lighthouse

# 一括監査スクリプト
for url in "https://example.com/" "https://example.com/about" "https://example.com/products"; do
  npx lighthouse "$url" --output=html --output-path="./reports/$(echo $url | md5sum | cut -c1-8).html"
done
```

---

## 定期監査スケジュール

| 頻度 | 監査内容 |
|------|----------|
| 週次 | Search Console エラーチェック、インデックス状況 |
| 月次 | Core Web Vitals、ランキング変動、競合動向 |
| 四半期 | フル技術監査、コンテンツ監査 |
| 年次 | サイト構造見直し、SEO戦略レビュー |
