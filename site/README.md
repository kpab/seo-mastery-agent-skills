# seo.kpab.dev

`seo-mastery` / `seo-mastery-jp` スキルの紹介サイト。スキル本体と同じリポジトリに置き、
バージョンや `last_verified` の表示が本体とずれないようにしている。

## 構成

- Astro（`output: 'static'`）+ 素の CSS。Tailwind も UI ライブラリも使わない
- 英語が既定（`/`）、日本語は `/ja`。文言は `src/data/content.ts` の 1 ファイルに両言語ぶん
- Cloudflare Workers の静的アセットとして配信（`wrangler.jsonc`、カスタムドメインのみ）

## コマンド

```sh
npm install
npm run dev       # ローカル確認
npm run build     # dist/ を生成
npm run deploy    # build して wrangler deploy
```

## SEO 上の取り決め

このサイト自体がスキルの実演なので、次を守る。

- 末尾スラッシュなしで統一（`trailingSlash: 'never'` と Workers の `drop-trailing-slash`）
- `canonical` は `Astro.url.pathname` から組み立て、クエリとフラグメントを落とす
- `hreflang` は en / ja の双方向 + `x-default`（英語）。noindex のページには出さない
- Web フォントを読み込まない。LCP を font の往復で遅らせない
- `robots.txt` は全許可。AI クローラーも止めない（認知が目的）
- `llms.txt` は任意対応。仕様として確立したものではない前提で、要約だけを置く

## 数字を直す場所

`src/data/site.ts` の `version` と `lastVerified` は、`.claude/skills/*/SKILL.md` の
frontmatter と一致させる。リリースで版が上がったらここも上げる。

## お知らせ（リリースノート）を追加する

1 リリース × 1 言語で 1 ファイル。英語と日本語の両方を置く。

```
src/content/releases/en/v1-6-0.md
src/content/releases/ja/v1-6-0.md
```

frontmatter は次の形。`slug` はファイル名と一致させる（URL にドットを入れないため、
`1.6.0` ではなく `v1-6-0`）。

```yaml
---
version: "1.6.0"
slug: "v1-6-0"
title: "1 行の見出し"
summary: "一覧と meta description、RSS に出る 1〜2 文の要約"
date: 2026-10-01
# 公開後に本文を直したときだけ
# updated: 2026-10-05
---
```

本文は Markdown。CHANGELOG の該当セクションをそのまま貼り、`### Added` / `### 追加` の
見出しで区切る。貼ったあとに確認すること。

- `version` が `.claude/skills/*/SKILL.md`・`marketplace.json`・git タグと一致しているか
- `src/data/site.ts` の `version` と `lastVerified` も上げたか（フッターと JSON-LD に出る）
- 英語版と日本語版の両方を置いたか（片方だけだと hreflang が片側 404 を指す）

出力されるもの:

- 一覧 `/releases`、`/ja/releases`（`CollectionPage` + `ItemList` の JSON-LD）
- 詳細 `/releases/v1-6-0`（`BlogPosting` + `BreadcrumbList`、`og:type=article`）
- RSS `/releases/rss.xml`、`/ja/releases/rss.xml`
- サイトマップの hreflang 対訳リンク（`@astrojs/sitemap` の i18n が自動で付ける）
