---
last_verified: 2026-08-30
---

# Astro SEO リファレンス

Astro特有のSEOパターン。Astroのデフォルト（JavaScriptゼロ、静的HTML出力）は他フレームワークが
プラグインで解決している問題の多くを最初から解消しています。残るのは、Astroが開発者に委ねている
判断です。どのアイランドをハイドレートするか、ビルド時に絶対URLをどう組み立てるか、
コンテンツのメタデータをどう構造化データに変換するか。

Astro 7（2026年6月22日リリース）で検証済み。このファイルで扱うAPIはv7では変更されていません。
v7が変えたのはAstroが出力するHTMLそのもので、末尾の移行ポイントにまとめてあります。v5とv6で
異なる場合はv6の書き方を先に示し、v5の形を注記します。

## Islands ArchitectureとCore Web Vitals

Astroは`client:*`ディレクティブを付けない限りクライアントJavaScriptを一切出力しません。つまり
ディレクティブを1つ追加するたびにINPとLCPのコストを意図的に払っていることになり、ディレクティブ
選択そのものがパフォーマンス改善作業です。

### クライアントディレクティブと指標の対応

| ディレクティブ | ハイドレートのタイミング | オプション | 指標への影響 |
|----------------|--------------------------|------------|--------------|
| `client:load` | ページ読み込み直後、高優先度 | — | INP・LCPともに最悪ケース。クリティカルレンダリングパスと競合する |
| `client:idle` | 読み込み完了後、`requestIdleCallback`発火時（非対応環境は`load`イベント） | `timeout`（ms） | LCP計測窓の外にハイドレーションを追い出せる。ただしメインスレッド消費は残る |
| `client:visible` | コンポーネントがビューポートに入ったとき（`IntersectionObserver`） | `rootMargin` | ファーストビュー外のアイランドの既定解。スクロールされるまでコストゼロ |
| `client:media` | CSSメディアクエリが一致したとき | メディアクエリ文字列 | モバイル専用・PC専用UIに有効 |
| `client:only={"react"}` | クライアントのみ。サーバーレンダリングを一切行わない | フレームワーク名、`slot="fallback"` | **レンダリング前のコンテンツはクローラーから見えない。**インデックス対象には絶対に使わない |

`server:defer`は用途が異なります。コンポーネントを**サーバーアイランド**に変え、ページ本体の
レンダリングとは切り離してオンデマンドで描画します。パーソナライズ部分や生成の遅い断片に使えば、
残りのページはキャッシュして高速に返せます。

### ディレクティブの選び方

次の2つを、この順番で判断します。

1. **その内容を初期HTMLでクローラーに見せる必要があるか。**
   必要ならサーバーレンダリング必須です。`client:only`は使えず、ハイドレート前でもサーバー側で
   意味のあるHTMLを出力できていなければなりません。
2. **ユーザーが最初に操作するのはいつか。**
   ファーストビュー内で即操作されるなら`client:load`。ファーストビュー内だが急がないもの
   （ドロップダウン、テーマ切り替え）は`client:idle`。ファーストビュー外は`client:visible`。

```astro
---
// src/pages/index.astro
import Hero from '../components/Hero.astro';           // JavaScriptゼロ（デフォルト）
import SearchBox from '../components/SearchBox.jsx';
import CommentThread from '../components/CommentThread.jsx';
import ThemeToggle from '../components/ThemeToggle.jsx';
---
<Hero />                                  {/* 静的HTML、JS 0 KB */}
<SearchBox client:load />                 {/* ファーストビュー内、すぐ操作される */}
<ThemeToggle client:idle={{ timeout: 2000 }} />
<CommentThread client:visible={{ rootMargin: "200px" }} />
```

よくあるLCP劣化パターン: ヒーロー部分をアニメーションさせたいだけのためにフレームワーク
コンポーネントで包み、`client:load`を付けてしまう。ヒーローはLCP要素そのものです。素の`.astro`
コンポーネントのままにして、アニメーションはCSSで行ってください。

### Islandsチェックリスト

- [ ] インデックスさせたい要素に`client:only`を使っていない
- [ ] LCP要素はハイドレートされるアイランドではなく静的な`.astro`コンポーネント内にある
- [ ] ファーストビュー外のアイランドは`client:load`ではなく`client:visible`
- [ ] サードパーティウィジェット（チャット、計測）は`client:idle`/`client:visible`、または初回操作時に読み込む
- [ ] `astro build`の出力に想定外のクライアントバンドルが含まれていないか確認した

## canonical URLとOGタグ

絶対URLの組み立てに使う値は2つです。

- `Astro.site` — `astro.config.mjs`の`site`の値。**`site`未設定なら`undefined`**になり、相対URLや
  壊れたcanonicalが静かに出力されます。
- `Astro.url` — レンダリング中のページのURL。

まず`site`を設定してください。以降の内容はすべてこれが前提です。

```js
// astro.config.mjs
import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://example.com',
  trailingSlash: 'always',   // どちらかに決め、リンク・canonical・サイトマップで統一する
});
```

### レイアウトで一括生成する

ベースレイアウトでcanonicalとOGタグを一度だけ生成し、全ページに継承させます。canonicalを
`Astro.url.href`ではなく`Astro.url.pathname`から組み立てると、クエリ文字列とフラグメントが落ちます。
たいていの場合はこれが望ましい挙動です。

```astro
---
// src/layouts/BaseLayout.astro
interface Props {
  title: string;
  description: string;
  image?: string;
  type?: 'website' | 'article';
  publishedTime?: Date;
  canonicalUrl?: string;
}

const { title, description, image, type = 'website', publishedTime, canonicalUrl } = Astro.props;

const canonical = canonicalUrl ?? new URL(Astro.url.pathname, Astro.site).href;
const ogImage = new URL(image ?? '/og-default.png', Astro.site).href;
---
<html lang="ja">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />

    <title>{title}</title>
    <meta name="description" content={description} />
    <link rel="canonical" href={canonical} />

    <meta property="og:type" content={type} />
    <meta property="og:title" content={title} />
    <meta property="og:description" content={description} />
    <meta property="og:url" content={canonical} />
    <meta property="og:image" content={ogImage} />
    {publishedTime && (
      <meta property="article:published_time" content={publishedTime.toISOString()} />
    )}

    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content={title} />
    <meta name="twitter:description" content={description} />
    <meta name="twitter:image" content={ogImage} />

    <slot name="head" />
  </head>
  <body><slot /></body>
</html>
```

OG画像はホスト名を含む絶対URLでなければなりません。`new URL(..., Astro.site)`ならそれが保証
されます。AstroプロジェクトでSNSのシェアプレビューが壊れる原因は、ほぼこの相対パス指定です。

### Astro 6以降のgetStaticPathsとAstro.site

`getStaticPaths()`はページのリクエストコンテキストが存在しない段階で実行されます。Astro 6以降、
`getStaticPaths()`内の`Astro.site`は**非推奨で警告が出ます**。他の`Astro`プロパティにアクセス
するとエラーになります。同じ設定値を持つ`import.meta.env.SITE`を使ってください。

```astro
---
// src/pages/blog/[...slug].astro
import { getCollection, render } from 'astro:content';
import BaseLayout from '../../layouts/BaseLayout.astro';

export async function getStaticPaths() {
  const posts = await getCollection('blog', ({ data }) => !data.draft);

  return posts.map((post) => ({
    params: { slug: post.id },
    props: {
      post,
      // Astro 6+: ここでは Astro.site ではなく import.meta.env.SITE を使う
      shareUrl: new URL(`/blog/${post.id}/`, import.meta.env.SITE).href,
    },
  }));
}

const { post, shareUrl } = Astro.props;
const { Content } = await render(post);
---
<BaseLayout
  title={post.data.title}
  description={post.data.description}
  type="article"
  canonicalUrl={shareUrl}
>
  <Content />
</BaseLayout>
```

URLはpropで渡します。`head`スロットで2つ目の`og:url`を出力してはいけません。スロットはレイアウト
自身のタグの**後**に描画され、スクレイパーは最初に見つけた`og:url`を採用します。つまりスロットでの
上書きは黙って無視され、ページには矛盾するタグが2つ並ぶだけです。

### 末尾スラッシュ

Astroの`trailingSlash`設定、内部リンク、canonicalタグ、サイトマップはすべて一致していなければ
なりません。ずれていると1ページにつき2つのURLを公開し、どちらを採用するかをGoogleに委ねることに
なります。Astro固有の落とし穴が2つあります。

- **拡張子付きエンドポイント。** Astro 6以降、`/sitemap.xml`や`/rss.xml`のようなルートは
  「`build.trailingSlash`の設定にかかわらず、末尾スラッシュなしでのみアクセスできる」仕様です。
  リンクは末尾スラッシュなしで書いてください。
- **ホスト側も正規化する。** 静的ホスティングは独自に末尾スラッシュを正規化することがあります。
  開発サーバーではなく、デプロイ後の挙動を`curl -I`で確認してください。

## Content CollectionsからのJSON-LD生成

Content Collectionsは全エントリをZodスキーマで検証します。このスキーマは、構造化データが必要と
する定義そのものです。ここからJSON-LDを生成すれば、構造化データの不備はSearch Consoleの
エラーではなくビルドエラーになります。

### コレクションを定義する

Astro 6以降、コレクションは`src/content.config.ts`に置き（旧`src/content/config.ts`は削除済み）、
`loader`の明示が必須です。

```ts
// src/content.config.ts
import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const blog = defineCollection({
  loader: glob({ base: './src/content/blog', pattern: '**/*.{md,mdx}' }),
  schema: ({ image }) =>
    z.object({
      title: z.string().max(110),           // 編集上の上限。Googleはheadlineに文字数制限を設けて
                                             // いないが「長いタイトルは端末により切り詰められる」
      description: z.string(),
      publishedAt: z.coerce.date(),
      updatedAt: z.coerce.date().optional(),
      cover: image(),                        // 検証＋最適化の対象になる
      author: z.object({
        name: z.string(),
        url: z.string().url().optional(),
      }),
      draft: z.boolean().default(false),
    }),
});

export const collections = { blog };
```

自分たちの編集ルールをスキーマに書いておけば（headlineの文字数上限、著者URLの`.url()`）、不正な記事は
壊れたマークアップとして公開される前に`astro build`で落ちます。

### マークアップを生成する

フロントマターでオブジェクトを組み立て、`set:html`でシリアライズします。Astroは`<script>`要素の
内部をエスケープしないため、JSONは自分でエスケープしてください。値の中に`</script>`が含まれると
そこでscriptタグが終了してしまいます。`<`をUnicodeエスケープに置き換えるだけで十分で、JSONとしても
有効なままです。

```astro
---
// src/components/ArticleJsonLd.astro
interface Props {
  post: import('astro:content').CollectionEntry<'blog'>;
}
const { post } = Astro.props;

const url = new URL(Astro.url.pathname, Astro.site).href;

const jsonLd = {
  '@context': 'https://schema.org',
  '@type': 'BlogPosting',
  headline: post.data.title,
  description: post.data.description,
  image: new URL(post.data.cover.src, Astro.site).href,
  datePublished: post.data.publishedAt.toISOString(),
  dateModified: (post.data.updatedAt ?? post.data.publishedAt).toISOString(),
  author: {
    '@type': 'Person',
    name: post.data.author.name,
    ...(post.data.author.url ? { url: post.data.author.url } : {}),
  },
  mainEntityOfPage: { '@type': 'WebPage', '@id': url },
};

// 本文中の "</script>" でタグが閉じられないよう `<` をエスケープする
const serialized = JSON.stringify(jsonLd).replace(/</g, '\\u003c');
---
<script type="application/ld+json" set:html={serialized} />
```

出力されるのは通常のJSON-LDで、`structured-data.md`に記載しているものと同じです。

```json
{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "AstroのアイランドをINP観点で最適化する",
  "description": "クライアントディレクティブの選択がインタラクション遅延をどう変えるか。",
  "image": "https://example.com/_astro/cover.abc123.webp",
  "datePublished": "2026-08-01T09:00:00.000Z",
  "dateModified": "2026-08-20T11:30:00.000Z",
  "author": { "@type": "Person", "name": "著者名", "url": "https://example.com/about/" },
  "mainEntityOfPage": { "@type": "WebPage", "@id": "https://example.com/blog/astro-inp/" }
}
```

### サイト共通のグラフ

Organization・WebSite・BreadcrumbListはページごとではなくベースレイアウトに置きます。`@graph`で
まとめて一度だけ出力すれば、各ページはそのページ固有のエンティティだけを持つことになります。

```astro
---
// src/components/SiteJsonLd.astro — BaseLayoutで一度だけ描画する
// "undefined" を含むURLを出力するくらいならビルド時に落とす。非nullアサーション
//（Astro.site!）はTypeScriptを黙らせるだけで、本当の問題は解決しない。
if (!Astro.site) throw new Error('astro.config.mjs に `site` がありません。JSON-LDには絶対URLが必要です');
const site = Astro.site.href;

const graph = {
  '@context': 'https://schema.org',
  '@graph': [
    { '@type': 'Organization', '@id': `${site}#org`, name: 'Example Inc.', url: site,
      logo: new URL('/logo.png', site).href },
    { '@type': 'WebSite', '@id': `${site}#website`, url: site, name: 'Example',
      publisher: { '@id': `${site}#org` } },
  ],
};
---
<script type="application/ld+json" set:html={JSON.stringify(graph).replace(/</g, '\\u003c')} />
```

`WebSite`ノードに`SearchAction`（サイトリンク検索ボックス）を**追加しないでください**。この機能は
2024年11月に廃止されています。詳細は`structured-data.md`を参照。

## @astrojs/sitemapによるサイトマップ

### セットアップとオプション

`@astrojs/sitemap`には`site`が必須です。`sitemap-index.xml`と連番の`sitemap-0.xml`を出力し、
`entryLimit`（デフォルト45,000。Googleの上限である1ファイル50,000 URL・非圧縮50MBより下）で
分割します。

```js
// astro.config.mjs
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://example.com',
  integrations: [
    sitemap({
      filter: (page) =>
        !page.includes('/draft/') &&
        !page.includes('/thank-you/'),
      serialize(item) {
        if (item.url.endsWith('/blog/')) item.priority = 0.8;
        return item;
      },
      entryLimit: 10000,
    }),
  ],
});
```

なお Google は**`<priority>`と`<changefreq>`を無視します**。設定しても害はありませんが効果もあり
ません。正確さが問われるのは`lastmod`だけで、それも本当に正確な場合に限ります。

### 除外の正しいやり方

`filter`はサイトマップからURLを除くだけで、インデックス登録は止めません。検索結果に出したくない
ページには`noindex`も必要です。逆に`noindex`のページをサイトマップに載せてはいけません。矛盾した
シグナルになります。

```astro
---
// src/pages/internal/preview.astro
import BaseLayout from '../../layouts/BaseLayout.astro';
---
<BaseLayout title="内部プレビュー" description="検索エンジン向けではない">
  <!-- <head> の中に置く必要がある。上のBaseLayoutは `head` スロットを用意している -->
  <meta slot="head" name="robots" content="noindex, nofollow" />
  <p>…</p>
</BaseLayout>
```

### 多言語サイトマップ

`i18n`オプションは翻訳ページごとに`<xhtml:link rel="alternate" hreflang="…">`を追加します。
これは`technical-seo.md`で説明しているサイトマップ方式のhreflang実装そのものです。

```js
// astro.config.mjs
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://example.com',
  i18n: {
    defaultLocale: 'en',
    locales: ['en', 'ja', 'fr'],
  },
  integrations: [
    sitemap({
      i18n: {
        defaultLocale: 'en',
        locales: { en: 'en-US', ja: 'ja-JP', fr: 'fr-FR' },
      },
    }),
  ],
});
```

`sitemap.i18n.locales`のキーはAstroが生成するパスセグメント（`/ja/…`）と一致させる必要があります。
値が出力されるhreflangコードです。キーがずれていると、代替リンクのないサイトマップが黙って
生成されます。

hreflangは依然として**双方向**リンクを要求します。各言語版が自分自身を含む全言語版を参照して
いなければなりません。インテグレーションが認識できるページについては自動処理されますが、
`customPages`で追加したページは翻訳対象になりません。

### robots.txt

Astroにrobots.txtの生成機能はありません。`public/`に静的ファイルを置き、サイトマップインデックス
を指定します。

```txt
User-agent: *
Allow: /

Sitemap: https://example.com/sitemap-index.xml
```

AIクローラー向けの記述は`ai-search.md`を参照。環境ごとにルールを変えるなど動的生成が必要な場合は
`src/pages/robots.txt.ts`のエンドポイントで対応できます。Astro 6以降はリンクを末尾スラッシュなしで
書いてください。

## View TransitionsとSEO

### ネイティブ遷移とClientRouter

Astroには2つの方式があり、SEO上の性質が大きく異なります。

1. **ネイティブのクロスドキュメント（MPA）View Transitions** — CSSのみ。各遷移は本物のドキュメント
   読み込みのままです。JavaScriptもルーターも不要で、SEOリスクはありません。まずこちらを検討します。
2. **`<ClientRouter />`** — サイトをクライアントルーティング化し、`transition:persist`、遷移をまたぐ
   状態保持、ライフサイクルフックを可能にします。Astro公式ドキュメントも「遷移後にスクリプトや
   状態を手動で再初期化する必要があるといった欠点がある」とトレードオフを明記しています。

クローラーが見るのはどちらの方式でもサーバーレンダリング済みHTMLなので、ClientRouterによって
コンテンツがGoogleから隠れることはありません。リスクはクライアント側にあります。計測、スクリプトで
注入する構造化データ、そして「1セッション1ページロード」を前提としたサードパーティウィジェットです。

```astro
---
// クライアントルーティングを使うなら、上のBaseLayoutの <head> に追加する。
// v6の名称。v5では <ViewTransitions /> だったが現在は削除済み。
import { ClientRouter } from 'astro:transitions';
---
<ClientRouter />
```

### 遷移後のスクリプトと計測

Astroはバンドルされたモジュールスクリプトについて「一度しか実行されず、初回実行後は無視される」と
明記しています。ページビュー送信をトップレベルのモジュールスクリプトとして書くと初回しか発火せず、
以降の遷移をすべて取りこぼします。

対処は2通り。推奨順に示します。

```astro
<!-- 推奨: ルーターのライフサイクルイベントを一度だけ購読する -->
<script>
  document.addEventListener('astro:page-load', () => {
    window.gtag?.('event', 'page_view', {
      page_location: location.href,
      page_title: document.title,
    });
  });
</script>

<!-- 代替: インラインスクリプトを遷移のたびに再実行させる -->
<script is:inline data-astro-rerun>
  initThirdPartyWidget();
</script>
```

ライフサイクルイベントの発火順は`astro:before-preparation` → `astro:after-preparation` →
`astro:before-swap` → `astro:after-swap` → `astro:page-load`です。新しいDOMが揃っている必要がある
処理には`astro:page-load`を使ってください。

### アクセシビリティ・モーション・永続化

- ClientRouterはページタイトルの変更を支援技術に自動でアナウンスします。ただし各ページが実際に
  異なる`<title>`を持っている場合に限ります。タイトルの重複はアナウンスと検索スニペットの両方を
  壊します。
- `prefers-reduced-motion`は尊重され、該当ユーザーにはアニメーションが無効化されます。
- View Transitions API非対応ブラウザでのフォールバックは`animate`・`swap`・`none`から選べます。
- `transition:persist`は要素とその状態を遷移後も維持します。ページ固有の構造化データやメタデータを
  含む要素を永続化すると古い内容がDOMに残ります。永続化してよいのはプレーヤーやサイドバーであって、
  コンテンツではありません。

## SEOに影響するバージョン移行ポイント

### Astro 7（2026年6月22日リリース）

Astro 7はこのファイルで扱うAPIを変更していません。変わったのはAstroが出力するHTMLそのものです。
importの名前が変わるより、クローラーにとっては影響が大きい部類です。

| 変更点 | SEOへの影響 |
|--------|-------------|
| Rustコンパイラが唯一のデフォルト`.astro`コンパイラに | 「未閉じタグはエラーになる」「意味的に不正なHTMLは自動補正されない」。旧コンパイラはHTMLパース仕様に合わせて不正なマークアップを黙って組み替えていましたが、v7は書いたまま通します。v6では問題なく描画されていたページが、実際に書かれていた壊れた入れ子のまま出力されることになります。大半はビルドエラーとして表面化します。ビルドが通ったものは見出しの順序と`<head>`の中身を再確認してください |
| `compressHTML`のデフォルトが`true`から`'jsx'`に | 隣接するインライン要素の間の空白が詰められます。`<span>hello</span><em>world</em>`は`helloworld`として出力されます。隣接要素を組み合わせて作っているタイトル・見出し・アンカーテキストは単語の区切りを失い、それがGoogleのインデックス対象テキストになります。空白が必要な箇所には明示的に`{" "}`を入れてください |
| MarkdownのレンダリングがremarkからSätteriへ | `@astrojs/markdown-remark`はデフォルトではインストールされなくなりました。見出しアンカー、外部リンクへの`rel`付与、抜粋生成など、SEO目的で入れていたremark/rehypeプラグインは、パッケージを再導入して`unified()`をプロセッサに設定するまで黙って動かなくなります。公開前に、生成される見出しIDと既存のページ内アンカーを突き合わせてください |
| `src/fetch.ts`がAdvanced Routing用の予約ファイルに | 標準のfetchハンドラーでリクエストパイプライン全体を制御できるようになりました。SSRルートのリダイレクトとレスポンスヘッダーはここが置き場所です。`edge-seo.md`が指摘するWorker生成レスポンスの穴と同じ話です |
| `astro:transitions`の内部APIを削除 | `TRANSITION_*`定数と`isTransitionBeforeSwapEvent()`・`createAnimationScope()`などのヘルパーが削除されました。ライフサイクル*イベント名*は変わっていないため、上記の`astro:page-load`による計測フックはそのまま使えます |

### Astro 6（2026年3月10日リリース）

| 変更点 | 対応 |
|--------|------|
| `<ViewTransitions />`の削除 | importとコンポーネントを`astro:transitions`の`<ClientRouter />`に置き換える |
| `getStaticPaths()`内の`Astro.site`が非推奨 | `import.meta.env.SITE`を使う。他の`Astro`プロパティはエラーになる |
| 拡張子付きエンドポイント | `/sitemap.xml`・`/rss.xml`等へのリンクは**末尾スラッシュなし**にする |
| `src/content/config.ts`の削除 | `src/content.config.ts`へ移動し、全コレクションに`loader`を付与する |
| Markdown見出しIDの末尾ハイフンが残る | ページ内アンカーと外部からの`#fragment`リンクを再確認する |
| 画像はアップスケールせず、切り抜きがデフォルト | ヒーロー画像のアートディレクションを再確認する。LCP画像が黙って小さくなるとLCP候補要素が変わる |

Astro 6には**Fonts API**（セルフホスティング、キャッシュ、フォールバックメトリクス生成、preload）
と**CSP API**も追加されました。Fonts APIはCLSに直接効きます。生成されるフォールバックメトリクスが
Webフォント差し替え時のレイアウトシフトを減らすためです。

## Astro SEOチェックリスト

- [ ] `astro.config.mjs`に`site`が設定されている（以降すべての前提）
- [ ] `trailingSlash`・内部リンク・canonical・サイトマップが一致している
- [ ] canonicalとOGタグは`Astro.url` + `Astro.site`からベースレイアウトで一括生成している
- [ ] OG画像のURLが絶対URLになっている
- [ ] インデックス対象に`client:only`を使っていない。LCP要素がハイドレート対象アイランドの中にない
- [ ] ファーストビュー外のアイランドは`client:visible`を使っている
- [ ] JSON-LDはコレクションスキーマから生成し、`set:html`の前に`<`をUnicodeエスケープしている
- [ ] Organization/WebSiteの`@graph`は一度だけ出力し、`SearchAction`を含めていない
- [ ] `@astrojs/sitemap`を導入し、下書き・ユーティリティページをフィルタし、かつ`noindex`もしている
- [ ] 多言語サイトでは`sitemap({ i18n })`のロケールキーがルートのパスセグメントと一致している
- [ ] `public/`の`robots.txt`が`sitemap-index.xml`を参照している
- [ ] ClientRouter使用時: 計測は`astro:page-load`にフックし、各ページのタイトルが一意である
- [ ] Astro 6以降: `getStaticPaths()`内に`Astro.site`がなく、`<ViewTransitions />`も残っていない
- [ ] Astro 7: RustコンパイラのHTML検証をビルドが通過している。`compressHTML: 'jsx'`によってタイトル・見出し・アンカーテキストの単語がつながっていない

## 公式リソース

- [Astro ドキュメント](https://docs.astro.build/)
- [Astro v7 へのアップグレード](https://docs.astro.build/en/guides/upgrade-to/v7/)
- [Astro v6 へのアップグレード](https://docs.astro.build/en/guides/upgrade-to/v6/)
- [テンプレートディレクティブリファレンス](https://docs.astro.build/en/reference/directives-reference/)
- [View transitions](https://docs.astro.build/en/guides/view-transitions/)
- [Content collections](https://docs.astro.build/en/guides/content-collections/)
- [@astrojs/sitemap](https://docs.astro.build/en/guides/integrations-guide/sitemap/)
- [Astro 7.0 リリースノート](https://astro.build/blog/astro-7/)
- [Astro 6.0 リリースノート](https://astro.build/blog/astro-6/)
