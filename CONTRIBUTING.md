# Contributing

Pull requests and issue reports are welcome!

## Repository layout

The English skill (`.claude/skills/seo-mastery/`) and the Japanese skill (`.claude/skills/seo-mastery-jp/`) are translations of each other, as are `README.md` and `docs/README.ja.md`.

## Keeping EN and JP in sync

**English is the source of truth.** When changing skill content:

1. Edit the English file first (`.claude/skills/seo-mastery/...` or `README.md`).
2. Apply the equivalent change to the Japanese counterpart (`.claude/skills/seo-mastery-jp/...` or `docs/README.ja.md`) in the same pull request.
3. Keep the document structure (headings, tables, code blocks) identical between the two languages. Locale-specific values inside examples (currency, addresses, timezone offsets) may differ.

A PR that changes only one language will be asked to add the other before merging.

## Versioning

Both skills share a version number, declared in each `SKILL.md` frontmatter, in `marketplace.json` and in `.claude-plugin/marketplace.json`. When you bump the version, update all of them, add a `CHANGELOG.md` entry under a `## [x.y.z] - YYYY-MM-DD` heading, and tag the commit `vx.y.z` — the release workflow fails if the tag, the manifests and the skill frontmatter disagree.

Semver for a knowledge repository: **MAJOR** = breaking structural change (file removed/renamed, guidance reversed), **MINOR** = new knowledge (new reference file, template or section), **PATCH** = corrections and freshness updates.

## Freshness

Every markdown file in a skill folder carries `last_verified: YYYY-MM-DD` in its frontmatter, and CI checks that it is present, well-formed, not in the future, and identical between EN and JP.

- When you change a file's factual content, re-verify it against primary sources and set `last_verified` to today.
- Record what you checked, and the source URL, in [`docs/research-notes.md`](docs/research-notes.md). Anything not confirmable against a primary source is marked `UNCONFIRMED` there and kept out of the skill files.
- The `Freshness reminder` workflow opens a checklist issue on the 1st of each month listing the sources to re-check.

## Content guidelines

- Base recommendations on [Google Search Central](https://developers.google.com/search) documentation and cite official sources where possible.
- When Google retires or restricts a feature (e.g. HowTo rich results), keep the template if it is still valid schema.org, but add a dated note explaining the current status.
- Structured data examples must be valid JSON.
- Record the date a specification change took effect, not the date you found it.

---

# コントリビューション（日本語）

**英語版がマスターです。** スキル内容を変更する際は、先に英語版（`.claude/skills/seo-mastery/`・`README.md`）を編集し、同じPR内で日本語版（`.claude/skills/seo-mastery-jp/`・`docs/README.ja.md`）にも同等の変更を反映してください。見出し・表・コードブロックの構造は両言語で一致させます（例中の通貨・住所・タイムゾーン等のローカライズ値は異なっていて構いません）。

バージョンは両スキル共通です。変更時は各 `SKILL.md` の frontmatter、`marketplace.json`、`.claude-plugin/marketplace.json`、`CHANGELOG.md` を更新し、コミットに `vx.y.z` のタグを付けてください。タグ・マニフェスト・frontmatter が食い違うとリリースワークフローが失敗します。semver の基準は、知識の追加が MINOR、誤り修正・鮮度更新が PATCH、構造の破壊的変更が MAJOR です。

スキルフォルダ内の各Markdownには `last_verified: YYYY-MM-DD` を付与しています。内容を変更したら一次情報で再検証したうえで当日の日付に更新し、確認した内容と出典URLを [`docs/research-notes.md`](docs/research-notes.md) に記録してください。仕様変更の日付は「見つけた日」ではなく「変更が有効になった日」を書きます。
