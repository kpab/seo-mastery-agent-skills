# 🚀 SEO Mastery Agent Skills

Claude/Codex向けの包括的なSEO最適化Agent Skills。Google公式ドキュメントに基づく技術SEO、コンテンツSEO、構造化データ、Core Web Vitals、サイト監査を統合的にサポートします。

## ✨ 特徴

- 📋 **技術SEOチェックリスト** - robots.txt、sitemap、canonical、hreflang等
- 📝 **コンテンツSEO最適化** - メタタグ、見出し構造、E-E-A-T対策
- 🏗️ **構造化データテンプレート** - Article、FAQ、Product、LocalBusiness等
- ⚡ **Core Web Vitals対応** - LCP、INP、CLSの詳細な最適化手法
- 🔍 **サイト監査ワークフロー** - 体系的な監査プロセスとレポート形式
- 🎯 **実践的なコード例** - コピペで使えるテンプレート多数

## 📦 インストール

### Claude Code / Claude.ai

```bash
# プロジェクトにインストール
mkdir -p .claude/skills/seo-mastery
curl -o .claude/skills/seo-mastery/SKILL.md https://raw.githubusercontent.com/YOUR_USERNAME/seo-mastery-agent-skills/main/.claude/skills/seo-mastery/SKILL.md
```

### Codex

```bash
# プロジェクトローカル
mkdir -p .codex/skills/seo-mastery
curl -o .codex/skills/seo-mastery/SKILL.md https://raw.githubusercontent.com/YOUR_USERNAME/seo-mastery-agent-skills/main/.claude/skills/seo-mastery/SKILL.md

# ユーザーグローバル
mkdir -p ~/.codex/skills/seo-mastery
curl -o ~/.codex/skills/seo-mastery/SKILL.md https://raw.githubusercontent.com/YOUR_USERNAME/seo-mastery-agent-skills/main/.claude/skills/seo-mastery/SKILL.md
```

## 📁 ファイル構成

```
.claude/skills/seo-mastery/
├── SKILL.md              # メインスキルファイル
├── technical-seo.md      # 技術SEO詳細
├── content-seo.md        # コンテンツSEO詳細
├── structured-data.md    # 構造化データ詳細
├── core-web-vitals.md    # Core Web Vitals詳細
└── audit-workflow.md     # 監査ワークフロー詳細
```

## 💡 使用例

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

## 📚 含まれるテンプレート

### 構造化データ
- Article / NewsArticle / BlogPosting
- FAQ（よくある質問）
- HowTo（ハウツー）
- Product（商品）
- LocalBusiness（ローカルビジネス）
- BreadcrumbList（パンくずリスト）
- VideoObject（動画）
- Organization / WebSite
- Event（イベント）

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

## 🔧 対応フレームワーク

- Next.js
- Nuxt.js
- 静的HTML
- WordPress（参考）

## 📖 参考リソース

- [Google Search Central](https://developers.google.com/search)
- [SEO Starter Guide](https://developers.google.com/search/docs/fundamentals/seo-starter-guide)
- [Web.dev - Core Web Vitals](https://web.dev/vitals/)
- [Schema.org](https://schema.org/)

## 🤝 コントリビューション

プルリクエストや Issue の報告を歓迎します！

## 📄 ライセンス

MIT License

---

**Note:** このスキルは [google-official-seo-guide](https://github.com/Hieubkav/wincellarCloneBackend/tree/master/.claude/skills/optimize/google-official-seo-guide) を参考に、より実践的で強化された内容を追加して作成されました。
