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

プルリクエストや Issue の報告を歓迎します。

## リポジトリの構成

英語版スキル（`.claude/skills/seo-mastery/`）と日本語版スキル（`.claude/skills/seo-mastery-jp/`）は互いの翻訳です。`README.md` と `docs/README.ja.md` も同様の関係にあります。

## 英語版と日本語版の同期

**英語版がマスターです。** スキル内容を変更する際は次の順で進めてください。

1. まず英語版（`.claude/skills/seo-mastery/...` または `README.md`）を編集する。
2. 同じプルリクエスト内で、日本語版（`.claude/skills/seo-mastery-jp/...` または `docs/README.ja.md`）に同等の変更を反映する。
3. 見出し・表・コードブロックの構造は両言語で一致させる。例中のローカライズ値（通貨・住所・タイムゾーンのオフセット等）は異なっていて構いません。

片方の言語しか変更していないプルリクエストは、マージ前にもう一方への反映をお願いします。

## バージョニング

バージョンは両スキル共通で、各 `SKILL.md` の frontmatter、`marketplace.json`、`.claude-plugin/marketplace.json` に記載しています。変更時はこれらすべてを更新し、`CHANGELOG.md` に `## [x.y.z] - YYYY-MM-DD` の見出しでエントリを追加し、コミットに `vx.y.z` のタグを付けてください。タグ・マニフェスト・frontmatter が食い違うとリリースワークフローが失敗します。

ナレッジリポジトリにおける semver の基準は次のとおりです。**MAJOR** は構造の破壊的変更（ファイルの削除・改名、方針の転換）、**MINOR** は知識の追加（新しいリファレンスファイル・テンプレート・セクション）、**PATCH** は誤りの修正と鮮度更新です。

## 鮮度の管理

スキルフォルダ内の各Markdownには frontmatter に `last_verified: YYYY-MM-DD` を付与しており、CIが「存在すること・形式が正しいこと・未来日でないこと・英語版と日本語版で一致していること」を検証します。

- 事実にあたる内容を変更したら、一次情報で再検証したうえで `last_verified` を当日の日付に更新してください。
- 確認した内容と出典URLを [`docs/research-notes.md`](docs/research-notes.md) に記録してください。一次情報で裏付けられないものは同ファイルに `UNCONFIRMED` として記し、スキル本文には書きません。
- `Freshness reminder` ワークフローが毎月1日に、確認先の一覧を含むチェックリストIssueを自動作成します。

## 内容のガイドライン

- 推奨事項は [Google Search Central](https://developers.google.com/search) のドキュメントに基づき、可能な限り公式の出典を示してください。
- Googleが機能を廃止・制限した場合（例: HowToリッチリザルト）、schema.org として有効ならテンプレートは残し、現状を説明する日付付きの注記を添えてください。
- 構造化データの例は有効なJSONでなければなりません。
- 仕様変更の日付は「見つけた日」ではなく「変更が有効になった日」を書きます。
