---
last_verified: 2026-08-29
---

# AI検索リファレンス（AI Overviews / AIモード / AIクローラー）

生成AI検索への最適化と制御の方法。GoogleのAI OverviewsとAIモード、およびサードパーティAIクローラー（OpenAI、Anthropic、Perplexity等）を扱います。GoogleのAI機能ガイド、2026年5月15日公開の生成AI最適化ガイド、および公式クローラードキュメントに基づいています。

## Googleの公式ガイダンス（AI Overviews / AIモード）

出典: [AI features and your website](https://developers.google.com/search/docs/appearance/ai-features) および [Optimizing your website for generative AI features](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide)

公式ガイドで確認済みの要点:

- **表示要件は3つある。** ページが**インデックス可能**であること、**スニペット表示可能**であること、そしてサイトがSearch Consoleで**「検索の生成AI機能」に含まれている**こと。Googleは明記しています。「Search の技術要件に加えて、Google Search の生成AI機能に表示される資格を得るには、サイトが Search Console で Search の生成AI機能に含まれている必要がある」。
- **特別なマークアップやファイルは不要。** 「Google Search（生成AI機能を含む）に表示されるために、新しい機械可読ファイル・AIテキストファイル・マークアップ・Markdownを作る必要はない。Google Search 自身がそれらを使っていないからだ」。これは**llms.txt**（後述）、コンテンツのチャンク分割（「AIが理解しやすいように細切れにする必要はない」）、AI向けの文体、AI専用スキーマ（「生成AI検索に構造化データは必須ではない」）のすべてに当てはまります。
- **標準的なSEOがそのまま最適化になる。** 生成AI機能は「Search のコアなランキング・品質システムに根ざしている」。上位表示され、質問に明確に答えるコンテンツがAI機能に引用されます。「AI用ランキング」が別に存在するわけではありません。
- **表示制御はSearch Consoleのコントロールと既存のスニペットコントロールで行う。** 新しいディレクティブはありません（次の2セクション参照）。
- **トラフィックはSearch Consoleで確認できる。** 検索タイプ「ウェブ」に含まれ、AI Overviews / AIモードからのクリックもそこで通常のクリックとして計上されます。2026年6月3日からは専用の**検索の生成AIパフォーマンスレポート**も提供されています（制約は計測セクション参照）。

### Search Consoleの生成AIコントロール

**2026年6月3日**から提供開始（当初は英国の一部プロパティ、2026年7月以降に他地域へ拡大）。通常の検索スニペットを損なわずにAI機能だけをオプトアウトできる唯一の手段です。

場所は **設定 → 検索の生成AI**。選択肢は3つあります。

| 選択肢 | 効果 |
|--------|------|
| サイトのリンクとコンテンツを検索の生成AI機能に含める | **デフォルト。** コンテンツがリンクとして表示され、AI応答のグラウンディングに使われる。これらの機能から表示回数と流入を得られる |
| サイトのリンクとコンテンツを検索の生成AI機能から除外する | AI Overviews・AIモード・Discoverの生成AI機能で表示・リンク・グラウンディングに使われなくなる |
| 親から継承 | 親プロパティの設定に従う |

**やらないこと:** Googleはこのコントロールについて「Search の他の部分に影響するランキングや掲載のシグナルとしては使用しない」と明記しています。通常の検索結果とDiscoverフィードには影響しません。変更の反映には通常1〜2日かかります。

このコントロールと `nosnippet` の使い分け:

- **Search Consoleのコントロール** — AI機能への表示だけを止めます。通常のスニペット、したがって通常のCTRには影響しません。「AIに自分のコンテンツを使わせたくない」が目的ならこちらを選びます。
- **`nosnippet` / `max-snippet`** — 通常の検索結果を含む*すべての*スニペットを消す・短くします。通常のスニペットも抑制したい場合にのみ使ってください。

### AI機能への表示制御

スニペットとインデックスを制御する既存の手段をそのまま使います:

```html
<!-- ページを検索から完全に除外（AI機能からも除外される） -->
<meta name="robots" content="noindex">

<!-- インデックスは維持しつつスニペットを非表示（AI Overviews / AIモードでのコンテンツ利用も防ぐ） -->
<meta name="robots" content="nosnippet">

<!-- スニペット長を制限（AI機能が引用できる量も制限される） -->
<meta name="robots" content="max-snippet:160">
```

```html
<!-- ページの一部だけをスニペット・AI機能から除外。
     data-nosnippet がサポートされるのは span / div / section 要素のみ —
     それ以外の要素（<p> 等）では無視される。 -->
<p><span data-nosnippet>このテキストはスニペットにもAI Overviewsにも表示されません。</span></p>
```

トレードオフ: `nosnippet` や小さい `max-snippet` 値は通常の検索スニペットも消したり短くしたりするため、一般にCTRが下がります。本当に引用されたくないコンテンツにのみ使ってください。AI機能だけを除外したいなら、上のSearch Consoleコントロールを使います。

## AIクローラー制御（robots.txt）

### Google-Extended の正確なスコープ

出典: [Google's common crawlers](https://developers.google.com/search/docs/crawling-indexing/google-common-crawlers)

`Google-Extended` は独立したクローラーではなく**製品トークン**です。制御できるのは1点のみ: コンテンツを**Gemini世代モデルの学習・グラウンディングに利用してよいか**です。

- `Google-Extended` をブロックしても、Google検索から**除外されない**。
- `Google-Extended` をブロックしても、AI Overviews / AIモードから**除外されない**（これらは検索機能であり、インデックスとスニペットコントロールで制御される）。
- `Google-Extended` は**ランキングシグナルではない**。

```txt
# Geminiの学習・グラウンディングのみ拒否 — 検索とAI Overviewsには影響しない
User-agent: Google-Extended
Disallow: /
```

### 主要AIクローラーのユーザーエージェント

| ユーザーエージェント | 運営元 | 用途 | ブロックの効果 |
|------------|--------|------|----------------|
| `Google-Extended` | Google | Gemini学習・グラウンディングの拒否トークン | 検索 / AI Overviewsには影響なし |
| `GPTBot` | OpenAI | モデル学習 | 今後の学習データから除外 |
| `OAI-SearchBot` | OpenAI | ChatGPT検索のインデックス | ChatGPT検索で引用されなくなる |
| `ChatGPT-User` | OpenAI | ChatGPTからのユーザー起点アクセス | 限定的 — OpenAIはユーザー起点のアクセスにはrobots.txtが「適用されない場合がある」と明記 |
| `ClaudeBot` | Anthropic | モデル学習 | 今後の学習データから除外 |
| `Claude-SearchBot` | Anthropic | Claude検索のインデックス | Claude検索で引用されなくなる |
| `Claude-User` | Anthropic | Claudeからのユーザー起点アクセス | Claudeがページを開けなくなる |
| `PerplexityBot` | Perplexity | 検索インデックス | Perplexityの回答で引用されなくなる |
| `Perplexity-User` | Perplexity | ユーザー起点アクセス | 実質なし — Perplexityはこのフェッチャーがrobots.txtを一般に無視すると明記している |
| `Applebot-Extended` | Apple | モデル学習の拒否トークン | Appleのモデル学習から除外 |
| `CCBot` | Common Crawl | オープンなWebコーパス（多くの学習に利用） | Common Crawlデータセットから除外 |
| `Meta-ExternalAgent` | Meta | モデル学習・インデックス | Metaの学習から除外 |
| `Bytespider` | ByteDance | モデル学習 | ByteDanceの学習から除外 |

UA文字列と用途は変わるため、設定前に各運営元の公式ドキュメントで最新情報を確認してください。またrobots.txtは自主的な取り決めであり、主要な運営元は尊重しますが、アクセス制御の代わりにはなりません。

### トレードオフ: 学習拒否とAI検索での引用

次の2つは別の問いとして分けて判断します:

1. **「コンテンツを将来のモデル学習に使わせてよいか？」** → 学習用クローラー（`GPTBot`、`ClaudeBot`、`Google-Extended`、`Applebot-Extended`、`CCBot` 等）。ブロックしても現在の可視性には影響しない。
2. **「AI検索製品に引用・リンクさせてよいか？」** → 検索・アクセス用クローラー（`OAI-SearchBot`、`Claude-SearchBot`、`PerplexityBot`、ユーザー起点フェッチャー）。ブロックするとAIの回答から消え、**そこからの参照トラフィックも失う**。

```txt
# レシピA: 学習は拒否し、AI検索での引用は維持（メディア・ブログでよくある選択）
User-agent: GPTBot
Disallow: /

User-agent: ClaudeBot
Disallow: /

User-agent: Google-Extended
Disallow: /

User-agent: Applebot-Extended
Disallow: /

User-agent: CCBot
Disallow: /

User-agent: Meta-ExternalAgent
Disallow: /

User-agent: Bytespider
Disallow: /
```

```txt
# レシピB: AIアクセスを全面ブロック（学習もAI検索引用も拒否 — AI経由の流入はほぼゼロになる前提。
# 注意: Perplexity-User や ChatGPT-User などユーザー起点フェッチャーはrobots.txtを無視することがある）
User-agent: GPTBot
Disallow: /

User-agent: OAI-SearchBot
Disallow: /

User-agent: ChatGPT-User
Disallow: /

User-agent: ClaudeBot
Disallow: /

User-agent: Claude-SearchBot
Disallow: /

User-agent: Claude-User
Disallow: /

User-agent: PerplexityBot
Disallow: /

User-agent: Perplexity-User
Disallow: /

User-agent: Google-Extended
Disallow: /

User-agent: Applebot-Extended
Disallow: /

User-agent: CCBot
Disallow: /

User-agent: Meta-ExternalAgent
Disallow: /

User-agent: Bytespider
Disallow: /
```

## llms.txt

`llms.txt` は、LLMが主要コンテンツを見つけやすくするために `/llms.txt` にMarkdown形式のサイト索引を置くというコミュニティ提案です。

- **Googleは利用しない。** 生成AI最適化ガイドは明確です。「AIテキストファイル」は不要であり、「Google Search 自身がそれらを使っていない」。設置してもGoogleへの効果は期待しないこと。
- 他のAIベンダーの採用状況も限定的・未確認。任意・低コスト・効果のエビデンスは薄い、という位置づけで扱う。
- 他のAIクローラー向けに設置する場合、提案されている書式は次のとおり:

```txt
# サイト名

> サイトの1行説明。

## Main content

- [ページタイトル](https://example.com/page): 1行説明
- [別のページ](https://example.com/other): 1行説明

## Optional

- [重要度の低いページ](https://example.com/misc): 1行説明
```

## AI検索に引用されやすいコンテンツ設計

AIの回答は、抽出と出典表示がしやすいコンテンツを好みます。レバーは質の高い編集型SEOと同じです:

- **結論を先に。** 最初の段落で答えを述べ、その後に詳細を展開する。具体的な質問への直接的な回答が最も引用されやすい。
- **明確な事実記述。** 具体的な数値・日付・定義・手順を書く。曖昧なマーケティング調の文章は避ける。
- **独自データと一次経験。** 調査・ベンチマーク・事例・実体験（E-E-A-Tの「Experience」）は、AI要約が言い換えで済ませられず出典として引用せざるを得ない要素。
- **構造化された見出し。** H2/H3ごとに1つの質問・サブトピックに絞り、パッセージ単体で成立させる。質問形の見出しの直後に答えを置く。
- **出典として安全なページ。** 著者・日付・情報源の明記（E-E-A-T）は、AI機能にとって引用しやすいページの条件になる。

チェックリスト:

- [ ] 冒頭約100語以内に主要な答えがある
- [ ] 各H2/H3がちょうど1つの質問・サブトピックを扱っている
- [ ] 重要な事実が抽出可能な文（数値+単位+日付）で書かれている
- [ ] 他のページにない要素（データ・経験・事例）を含んでいる
- [ ] 著者・日付・情報源がページ上で確認できる

## AI検索トラフィックの計測

### Search Console

- AI Overviews / AIモードの表示回数・クリックは検索パフォーマンスの**検索タイプ「ウェブ」**に含まれる（AIモードは2025年6月から集計）。
- 専用の**検索の生成AIパフォーマンスレポート**（2026年6月3日提供開始、Discover版もあり）は、AI Overviews・AIモード・Discoverの生成AI機能をまたいで表示回数をページ・国・デバイス・日付別に分解できる。前提となる制約が2つある。データは**2026年5月18日以降**で過去分の遡及がないこと、初期版は**表示回数のみでクリックがない**こと。
- 専用レポートにクリックがないため、貢献度の把握は引き続き「ウェブ」タイプに依存する。情報系クエリで「表示回数は横ばい、クリックは減少」というパターンに注意 — AI Overviewsがクリックを吸収している典型的な兆候。

### Analytics（参照元の分離）

AIアシスタント経由の流入は通常の参照トラフィックとして届きます。参照元ドメインでセグメント分けします:

```txt
chatgpt.com
perplexity.ai
gemini.google.com
copilot.microsoft.com
claude.ai
```

例（GA4）: カスタムチャネルグループ、またはExplorationのフィルタで「セッションの参照元」に正規表現条件を設定:

```txt
chatgpt\.com|perplexity\.ai|gemini\.google\.com|copilot\.microsoft\.com|claude\.ai
```

注意: リファラーを送らないAIサービスもあるため、計測できるAIトラフィックは下限値です。

## 公式リソース

- [AI features and your website](https://developers.google.com/search/docs/appearance/ai-features)
- [Optimizing your website for generative AI features on Google Search](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide)
- [検索の生成AIコントロール（Search Console ヘルプ）](https://support.google.com/webmasters/answer/16908024)
- [Introducing Search Generative AI performance reports](https://developers.google.com/search/blog/2026/06/gen-ai-performance-reports)
- [Google's common crawlers（Google-Extended）](https://developers.google.com/search/docs/crawling-indexing/google-common-crawlers)
- [スニペットコントロール（メタタグ）](https://developers.google.com/search/docs/appearance/snippet)
- [OpenAIのクローラー](https://platform.openai.com/docs/bots)
- [Anthropicのクローラー](https://support.claude.com/en/articles/8896518-does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-the-crawler)
- [Perplexityのクローラー](https://docs.perplexity.ai/guides/bots)
