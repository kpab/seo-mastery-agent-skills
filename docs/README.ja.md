# SEO Mastery Agent Skills

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](../LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Agent%20Skill-7C3AED)](https://docs.claude.com/en/docs/claude-code/overview)
[![Languages: EN | JP](https://img.shields.io/badge/Languages-EN%20%7C%20JP-success)](../README.md)

Claude Code / Codex 向けの包括的なSEO最適化Agent Skills。Google公式ドキュメントに基づく技術SEO、コンテンツSEO、構造化データ、Core Web Vitals、E-E-A-T、サイト監査を統合的にサポートします。

## 特徴

- **技術SEOチェックリスト** - robots.txt、sitemap、canonical、hreflang等
- **コンテンツSEO最適化** - メタタグ、見出し構造、E-E-A-T対策
- **構造化データテンプレート** - Article、FAQ、Product、LocalBusiness等
- **Core Web Vitals対応** - LCP、INP、CLSの詳細な最適化手法
- **サイト監査ワークフロー** - 体系的な監査プロセスとレポート形式
- **実践的なコード例** - コピペで使えるテンプレート多数

## インストール

各スキルは `SKILL.md` と複数の参照ファイル（`technical-seo.md`、`content-seo.md` 等）で構成されています。`SKILL.md` だけを取得するとスキルが不完全になるため、スキルフォルダ内の**すべてのファイル**をインストールしてください。

### 推奨: リポジトリをクローン

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
for f in SKILL.md technical-seo.md content-seo.md structured-data.md core-web-vitals.md audit-workflow.md; do
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
for f in SKILL.md technical-seo.md content-seo.md structured-data.md core-web-vitals.md audit-workflow.md; do
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
│   └── audit-workflow.md     # 監査ワークフロー詳細
└── seo-mastery-jp/           # 日本語版
    ├── SKILL.md              # メインスキルファイル
    ├── technical-seo.md      # 技術SEO詳細
    ├── content-seo.md        # コンテンツSEO詳細
    ├── structured-data.md    # 構造化データ詳細
    ├── core-web-vitals.md    # Core Web Vitals詳細
    └── audit-workflow.md     # 監査ワークフロー詳細
```

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

\* FAQリッチリザルトは著名な政府機関・医療機関サイト限定、HowToリッチリザルトはGoogleが2023年に廃止済み。テンプレートはセマンティックマークアップ用途として提供しています。

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

- Next.js
- Nuxt.js
- 静的HTML
- WordPress（参考）

## 参考リソース

- [Google Search Central](https://developers.google.com/search)
- [SEO Starter Guide](https://developers.google.com/search/docs/fundamentals/seo-starter-guide)
- [Web.dev - Core Web Vitals](https://web.dev/vitals/)
- [Schema.org](https://schema.org/)

## コントリビューション

プルリクエストや Issue の報告を歓迎します！ [CONTRIBUTING.md](../CONTRIBUTING.md) を参照してください。特に、英語版と日本語版は同期を保つ必要があります（英語版がマスター）。

## ライセンス

MIT License
