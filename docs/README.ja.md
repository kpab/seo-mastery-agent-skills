# SEO Mastery Agent Skills

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](../LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Agent%20Skill-7C3AED)](https://docs.claude.com/en/docs/claude-code/overview)
[![Languages: EN | JP](https://img.shields.io/badge/Languages-EN%20%7C%20JP-success)](../README.md)

[English README here](../README.md)

Claude Code / Codex 向けの包括的なSEO最適化Agent Skills。Google公式ドキュメントに基づく技術SEO、コンテンツSEO、構造化データ、Core Web Vitals、E-E-A-T、AI検索、エッジ・静的サイトのSEO、サイト監査を統合的にサポートします。

## このスキルの位置づけ

- **軽量・ゼロ依存。** Markdownのみで完結します。APIキーもMCPサーバーもインストールするスクリプトも不要で、実行するものは何もありません。フォルダをコピーすればオフラインで動きます。
- **エッジ・静的サイトに強い。** **Astro** と **Cloudflare Workers/Pages** に専用のリファレンス層を用意しています。アイランドのハイドレーションとINP/LCPの関係、`_redirects` / `_headers` とWorkerコードに適用されない盲点、D1/KVからの動的サイトマップ、エッジでのクローラー検証まで扱います。
- **鮮度を「たぶん最新」で済ませない。** 全リファレンスファイルに `last_verified` の日付を付与してCIで検証し、検証パスで追加・修正した記述は [docs/research-notes.md](research-notes.md) から一次情報に辿れるようにし、変更は semver に沿って [CHANGELOG.md](../CHANGELOG.md) に記録し、毎月1日に再検証用のIssueを自動作成しています。保証しているのは運用と日付スタンプであって、全行が現時点で正しいことではありません。

## 特徴

- **技術SEOチェックリスト** - robots.txt、sitemap、canonical、hreflang等
- **コンテンツSEO最適化** - メタタグ、見出し構造、E-E-A-T対策
- **構造化データテンプレート** - Article、FAQ、Product、LocalBusiness等
- **Core Web Vitals対応** - LCP、INP、CLSの詳細な最適化手法
- **AI検索対応** - AI Overviews / AIモードの表示要件と制御、AIクローラー管理
- **Astro・エッジSEO** - Astro固有のパターンとCloudflare Workers/PagesのエッジSEO
- **サイト監査ワークフロー** - 体系的な監査プロセスとレポート形式
- **実践的なコード例** - コピペで使えるテンプレート多数

## インストール

各スキルは `SKILL.md` と複数の参照ファイル（`technical-seo.md`、`content-seo.md` 等）で構成されています。`SKILL.md` だけを取得するとスキルが不完全になるため、スキルフォルダ内の**すべてのファイル**をインストールしてください。

### 推奨: Claude Code プラグイン

```bash
claude plugin marketplace add kpab/seo-mastery-agent-skills
claude plugin install seo-mastery@seo-mastery-agent-skills
```

英語版・日本語版の両スキルがインストールされ、プラグインマネージャー経由で更新できます。

### 代替: リポジトリをクローン

```bash
git clone https://github.com/kpab/seo-mastery-agent-skills.git
# 使いたいスキルフォルダをコピー:
cp -r seo-mastery-agent-skills/.claude/skills/seo-mastery     .claude/skills/      # 英語版
cp -r seo-mastery-agent-skills/.claude/skills/seo-mastery-jp  .claude/skills/      # 日本語版
```

### Claude Code / Claude.ai（全ファイルをダウンロード）

```bash
SKILL=seo-mastery   # または seo-mastery-jp
BASE=https://raw.githubusercontent.com/kpab/seo-mastery-agent-skills/main/.claude/skills/$SKILL
mkdir -p .claude/skills/$SKILL
for f in SKILL.md technical-seo.md content-seo.md structured-data.md core-web-vitals.md ai-search.md astro-seo.md edge-seo.md audit-workflow.md; do
  curl -fsSL -o .claude/skills/$SKILL/$f "$BASE/$f"
done
```

### Codex

```bash
# 上記と同様。ターゲットを Codex のスキルディレクトリに変更:
# プロジェクトローカル: .codex/skills/$SKILL  |  ユーザーグローバル: ~/.codex/skills/$SKILL
SKILL=seo-mastery   # または seo-mastery-jp
BASE=https://raw.githubusercontent.com/kpab/seo-mastery-agent-skills/main/.claude/skills/$SKILL
mkdir -p .codex/skills/$SKILL
for f in SKILL.md technical-seo.md content-seo.md structured-data.md core-web-vitals.md ai-search.md astro-seo.md edge-seo.md audit-workflow.md; do
  curl -fsSL -o .codex/skills/$SKILL/$f "$BASE/$f"
done
```

## ファイル構成

```
.claude/skills/
├── seo-mastery/              # 英語版
│   ├── SKILL.md              # メインスキルファイル
│   ├── technical-seo.md      # 技術SEO詳細
│   ├── content-seo.md        # コンテンツSEO詳細
│   ├── structured-data.md    # 構造化データ詳細
│   ├── core-web-vitals.md    # Core Web Vitals詳細
│   ├── ai-search.md          # AI検索詳細
│   ├── astro-seo.md          # Astro固有のSEO
│   ├── edge-seo.md           # Cloudflare Workers/PagesのエッジSEO
│   └── audit-workflow.md     # 監査ワークフロー詳細
└── seo-mastery-jp/           # 日本語版
    ├── SKILL.md              # メインスキルファイル
    ├── technical-seo.md      # 技術SEO詳細
    ├── content-seo.md        # コンテンツSEO詳細
    ├── structured-data.md    # 構造化データ詳細
    ├── core-web-vitals.md    # Core Web Vitals詳細
    ├── ai-search.md          # AI検索詳細
    ├── astro-seo.md          # Astro固有のSEO
    ├── edge-seo.md           # Cloudflare Workers/PagesのエッジSEO
    └── audit-workflow.md     # 監査ワークフロー詳細

docs/research-notes.md        # 調査ノート: 各記述の根拠と出典
CHANGELOG.md                  # Keep a Changelog + semver の更新履歴
```

`.claude/skills/` 配下の全ファイルには `last_verified: YYYY-MM-DD` のfrontmatterが付いており、CIで検証しています（存在すること、形式が正しいこと、未来日でないこと、英語版と日本語版で一致していること）。

## 使用例

```
# メタタグ最適化を依頼
「このページのメタタグを最適化して」

# 構造化データ生成
「この記事にArticle構造化データを追加して」

# サイト監査実行
「このサイトのSEO監査をして」

# Core Web Vitals改善
「LCPを改善する方法を教えて」

# FAQの構造化データを生成
「このFAQページにJSON-LDを追加して」
```

## 含まれるテンプレート

### 構造化データ
- Article / NewsArticle / BlogPosting
- FAQ（よくある質問）*
- HowTo（ハウツー）*
- Product（商品）
- LocalBusiness（ローカルビジネス）
- BreadcrumbList（パンくずリスト）
- VideoObject（動画）
- Organization / WebSite
- Event（イベント）

\* FAQリッチリザルトはGoogleが2026年5月7日に完全廃止、HowToリッチリザルトは2023年に廃止済み。テンプレートはセマンティックマークアップ用途として提供しています。

### 技術SEO
- robots.txt テンプレート
- sitemap.xml テンプレート
- hreflang 実装パターン
- canonical URL 設定例

### Core Web Vitals
- LCP最適化コード
- INP最適化コード
- CLS最適化コード
- 測定・監視スクリプト

## 対応フレームワーク

- **Astro** — 専用リファレンスあり（[astro-seo.md](../.claude/skills/seo-mastery-jp/astro-seo.md)）。Astro 6 で検証済み
- **Cloudflare Workers / Pages** — 専用リファレンスあり（[edge-seo.md](../.claude/skills/seo-mastery-jp/edge-seo.md)）
- Next.js — コード例は [core-web-vitals.md](../.claude/skills/seo-mastery-jp/core-web-vitals.md) と [technical-seo.md](../.claude/skills/seo-mastery-jp/technical-seo.md)
- Nuxt 3+ — 同じファイル
- 静的HTML — テンプレートはすべてフレームワーク非依存

それ以外（WordPress、Rails、Django など）はフレームワーク非依存のガイダンスでのみカバーしています。
CMS固有のリファレンスファイルはありません。

## バージョニング

本リポジトリは [Semantic Versioning](https://semver.org/lang/ja/) を、APIではなく知識ベースとして解釈して運用します。**MAJOR** は構造の破壊的変更（リファレンスファイルの削除・改名、スキルの改名、過去の助言を無効化する方針転換）、**MINOR** は知識の追加（新しいリファレンスファイル・テンプレート・セクション）、**PATCH** は誤りの修正と鮮度更新（不正確な記述の訂正、廃止機能への追随、`last_verified` の更新）です。`SKILL.md`・2つの `marketplace.json`・CHANGELOGの見出し・gitタグのバージョンは常に一致させており、食い違うとリリースワークフローが失敗します。

## 参考リソース

- [Google Search Central](https://developers.google.com/search)
- [SEO Starter Guide](https://developers.google.com/search/docs/fundamentals/seo-starter-guide)
- [Web.dev - Core Web Vitals](https://web.dev/vitals/)
- [Schema.org](https://schema.org/)

## コントリビューション

プルリクエストや Issue の報告を歓迎します！ [CONTRIBUTING.md](../CONTRIBUTING.md) を参照してください。特に、英語版と日本語版は同期を保つ必要があります（英語版がマスター）。

## ライセンス

MIT License
