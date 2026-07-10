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

Both skills share a version number, declared in each `SKILL.md` frontmatter and in `marketplace.json`. When you bump the version, update all three places and add an entry to `CHANGELOG.md`.

## Content guidelines

- Base recommendations on [Google Search Central](https://developers.google.com/search) documentation and cite official sources where possible.
- When Google retires or restricts a feature (e.g. HowTo rich results), keep the template if it is still valid schema.org, but add a dated note explaining the current status.
- Structured data examples must be valid JSON.

---

# コントリビューション（日本語）

**英語版がマスターです。** スキル内容を変更する際は、先に英語版（`.claude/skills/seo-mastery/`・`README.md`）を編集し、同じPR内で日本語版（`.claude/skills/seo-mastery-jp/`・`docs/README.ja.md`）にも同等の変更を反映してください。見出し・表・コードブロックの構造は両言語で一致させます（例中の通貨・住所・タイムゾーン等のローカライズ値は異なっていて構いません）。

バージョンは両スキル共通です。変更時は各 `SKILL.md` の frontmatter、`marketplace.json`、`CHANGELOG.md` の3箇所を更新してください。
