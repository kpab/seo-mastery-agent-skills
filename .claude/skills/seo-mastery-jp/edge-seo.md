---
last_verified: 2026-09-02
---

# エッジSEO リファレンス（Cloudflare Workers / Pages）

アプリケーションではなくエッジ側で行うSEO施策。リダイレクト、レスポンスヘッダ、動的サイトマップ、
クローラー制御、配信直前のHTML書き換えを扱います。Cloudflare Workers / Cloudflare Pagesを前提に
書いていますが、考え方は他のエッジランタイムにも適用できます。

Cloudflare公式ドキュメントで2026年9月2日に検証済み。`_redirects`と`_headers`は静的アセット付き
WorkersでもPagesでも同一に動作します。挙動が分かれる箇所は都度明記します。

## プラットフォームのモデル

リクエストの経路は2つあり、エッジSEOのバグはほぼすべてこの2つの混同から生まれます。

| 経路 | 配信対象 | `_redirects`の適用 | `_headers`の適用 |
|------|----------|--------------------|------------------|
| **静的アセット** | ビルド出力ディレクトリからアップロードしたファイル | される | される |
| **Workerコード / Pages Functions** | コードが返すレスポンス（SSR、APIルート） | **されない** | **されない** |

Cloudflareは、リダイレクトは「リクエストURLがルールに一致しても、Workerコードが処理するリクエストには
適用されない」、カスタムヘッダも「Workerコードが生成したレスポンスには適用されない」と明言しています
（いずれも公式ドキュメントの記述を訳したものです）。静的なマーケティングページとSSRのブログが混在する
サイトでは、リダイレクトとヘッダの
ロジックを**2箇所に実装する**か、Workerコード側に一本化する必要があります。

設定は`wrangler.jsonc`の`assets`以下に書きます。

```jsonc
{
  "name": "example-site",
  "main": "src/index.ts",
  "compatibility_date": "2026-08-01",
  "assets": {
    "directory": "./dist/",
    "binding": "ASSETS",
    "not_found_handling": "404-page",
    // 後述「ナビゲーションリクエストはWorkerを素通りする」参照。not_found_handling を
    // 設定すると run_worker_first 外のSSRルートはブラウザで404になる。
    "run_worker_first": ["/api/*", "!/api/public/*"]
  }
}
```

`run_worker_first`は真偽値かルートパターンの配列を受け付けます（`*`は深い一致、先頭の`!`は否定）。
`.assetsignore`を使うと`_worker.js`・`_redirects`・`_headers`が公開アセットとしてアップロード
されるのを防げます。

**このキーは、そもそもWorkerがリクエストを見るかどうかを決めます。** デフォルトでは一致する静的
アセットがあればそれを返し、一致しない場合にのみWorkerが呼ばれます。HTMLを書き換えたり検査したり
するWorker——本ファイル後半のHTMLRewriterやクエリ正規化のパターン——は、上の設定のままでは
デッドコードです。`/blog/post/`はアセットに一致するのでWorkerまで到達しません。ミドルウェア型の
Workerでは、HTMLのパスを`run_worker_first`に列挙する必要があります。

```jsonc
{
  "assets": {
    "directory": "./dist/",
    "binding": "ASSETS",
    // ハッシュ付きアセット以外はWorkerを先に通す。
    // アセットはエッジからそのまま返したいので除外する。
    "run_worker_first": ["/*", "!/_astro/*", "!/assets/*"]
  }
}
```

代償は前述のトレードオフです。これらのパスには`_headers`も`_redirects`も適用されなくなるため、
ヘッダ設定とリダイレクトはWorker側で自前で行うことになります。プロジェクトごとに選んでください。
純粋な静的サイトならアセット優先、HTMLを本当に変換する必要があるならWorker優先です。

### ナビゲーションリクエストはWorkerを素通りする

上の表には載っていない第3の経路があります。Workerスクリプト（`main`）があり、
`not_found_handling`を設定していて、`compatibility_date`が`2025-04-01`以降（または
`assets_navigation_prefers_asset_serving`フラグが有効）の場合、静的アセットに一致しない
**ナビゲーションリクエスト**（ブラウザがページ遷移時に付ける`Sec-Fetch-Mode: navigate`
ヘッダ付きのリクエスト）は**Workerではなくアセット層が処理します**。ブラウザには`404.html`
（`single-page-application`なら`index.html`）が返り、Workerは一度も実行されません。

クローラーは`Sec-Fetch-Mode`を送らないので、従来どおりWorkerに到達します。ハイブリッド
サイトではこれが最悪の分岐を生みます。GooglebotはSSRページを取得してインデックスし、検索
結果をクリックした人間は全員404ページに着地します。冒頭の1つ目の設定
（`run_worker_first: ["/api/*", …]`＋`not_found_handling: "404-page"`）は、`/api/*`以外の
SSRルートすべてでまさにこの問題を抱えています。

回避策は3つ。優先順に：

1. SSRパスをすべて`run_worker_first`に列挙する。ここに一致するパスはナビゲーション判定を
   完全にスキップします（フラグは効きません）。
2. `assets_navigation_has_no_effect`互換フラグを設定して旧挙動に戻す。アセット不一致は
   すべてWorkerを起動し、その分課金されます。
3. `not_found_handling`を設定しない。このルールは設定されているときだけ発動します。

確認は同じSSRのURLに対してブラウザと`curl`（`Sec-Fetch-Mode`ヘッダなし）の両方で行うこと。
レスポンスが違えばこの状態です。

このうち2つのキーは、自前のリダイレクトが動くより前にURLの正規形を決めてしまいます。

| キー | 値 | SEOへの影響 |
|------|-----|-------------|
| `html_handling` | `auto-trailing-slash`（デフォルト）、`force-trailing-slash`、`drop-trailing-slash`、`none` | `/about` と `/about/` のどちらを配信し、どちらに307を返すかが決まる。`<link rel="canonical">` とサイトマップで使う形に揃えること。ずれていると全ページがリダイレクトを経てからインデックスされる |
| `not_found_handling` | `none`（デフォルト）、`404-page`、`single-page-application` | `404-page`は最も近い`404.html`を本物の404ステータスで返す。`single-page-application`は**一致しない全パスに200で`index.html`を返す**ため、タイプミスや切れたリンクがインデックス可能なソフト404になる。アプリシェルなら許容できるが、コンテンツサイトでは有害 |

## リダイレクト

### _redirectsファイル

静的アセットディレクトリに置くプレーンテキストで、1行1ルール（`[source] [destination] [code?]`）
です。ステータスコードは**省略すると302**になります。恒久的な移転を一時リダイレクトとして公開
してしまうこのパターンが、CloudflareプロジェクトでもっともよくあるSEO事故です。コードは必ず
明示してください。

```txt
# 恒久的な移転 — 301を必ず明示する
/old-blog/*            /blog/:splat            301
/products/legacy-sku   /products/new-sku       301

# プレースホルダーによるロケール統合（1パスセグメントに一致）
/en-us/:slug           /en/:slug               301

# 一時的: あとで復活するキャンペーンページ
/summer-sale           /promotions/            302

# プロキシ（URLを変えないリライト） — 相対パス指定、ステータス200
/docs/*                /documentation/:splat   200
```

押さえるべきルール。

- **プレースホルダー**（`:name`）は区切り文字以外のすべてに一致します。区切り文字は位置によって
  変わり、**ホスト部**では`.`または`/`、**パス部**では`/`のみです。つまりパス中のプレースホルダーは
  **ドットにも一致します**。`/:slug`は`report.pdf`にも一致するため、きれいなスラッグを想定した
  ルールがファイルURLまで書き換えてしまいます。
- **スプラット**（`*`）は貪欲一致で、**1URLにつき1つまで**です。宛先側ではプレースホルダーと
  スプラットをそれぞれ`:name`・`:splat`で参照します。
- サポートされるステータスコードは**301・302・303・307・308**。宛先を`200`にするとリダイレクト
  ではなくプロキシになります。
- **非対応:** クエリパラメータによる一致、ドメインレベルのリダイレクト、国・言語・Cookieによる
  条件分岐。これらはWorkerコード（またはCloudflare Rules）が必要です。

### 制限値

| 項目 | 値 |
|------|-----|
| 静的リダイレクト | 2,000件 |
| 動的リダイレクト（`*`・`:name`を含む） | 100件 |
| 合計 | 2,100件 |
| 1行あたりの文字数 | 1,000文字 |

大規模なレガシーURLを移行するサイトは、動的100件の上限にすぐ到達します。解決策はルールを増やす
ことではなく、後述するKVバックエンドのWorkerです。

### Workerコードでのリダイレクト

ファイル形式で表現できないもの（クエリパラメータ、数千件の個別レガシーURL、条件分岐）はWorkerで
処理します。マップをKVに置けば、デプロイなしでリダイレクトを更新できます。

```js
// src/index.ts
export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    // 1. レガシーURLの完全一致検索（KVに "/old/path" -> "/new/path" を保存）
    const target = await env.REDIRECTS.get(url.pathname);
    if (target) {
      return Response.redirect(new URL(target, url.origin).toString(), 301);
    }

    // 2. クエリパラメータの正規化: 計測用パラメータを除去してクリーンURLへ301
    const TRACKING = new Set(['utm_source', 'utm_medium', 'utm_campaign', 'fbclid', 'gclid']);
    if (url.search) {
      // 生のペアから組み直す。url.searchParams を書き換えるとクエリ全体が
      // 再シリアライズされ、"?q=a%20b" が "?q=a+b" になる。このルールが触って
      // いないパラメータが毎回書き換わるということで、オリジン側が元に戻すなら
      // 2つのルールの間でリクエストが往復し続ける。
      const pairs = url.search.slice(1).split('&').filter(Boolean);
      const kept = pairs.filter((pair) => !TRACKING.has(pair.split('=')[0]));
      if (kept.length !== pairs.length) {
        const query = kept.length ? `?${kept.join('&')}` : '';
        return Response.redirect(`${url.origin}${url.pathname}${query}`, 301);
      }
    }

    return env.ASSETS.fetch(request);
  },
};
```

計測パラメータのリダイレクト除去は慎重に。クライアント側でこれらを読む解析ツールの参照元計測が
壊れます。パラメータによる重複には`rel=canonical`を優先し、エッジでのリダイレクトは本当に価値の
低い別URLを生む場合（セッションID、ソート順）に限定してください。

### リダイレクト設計の原則

- **恒久的なら301、一時的なら302。** 長期間続く302を、Googleは「元のURLをインデックスに残せ」と
  いうシグナルとして扱います。多くの場合それは意図と違います。
- **1ホップに保つ。** 連鎖はクロール効率を落とし、各段階でわずかにシグナルを失います。新しい
  リダイレクトを追加するときは、既存ルールが移転元を指していないか確認して平坦化してください。
- **トップページではなく相当するページへ。** 大量のURLを`/`へまとめて飛ばすとソフト404扱いに
  なります。
- **順序が意味を持つ。** ルールは上から評価され、最初に一致したものが適用されます。個別ルールを
  ワイルドカードより上に置いてください。
- **プロトコルとホストの正規化は別レイヤーで。** HTTP→HTTPSやwww→apex（またはその逆）は
  `_redirects`ではなくゾーンレベルのCloudflare Redirect Rulesで行います。`_redirects`は
  ドメインレベルのリダイレクトに対応していません。

## _headersによるSEOヘッダ制御

ルールブロックはURLパターンの行と、インデントした`Name: value`行で構成されます。上限は
**100ルール**、**1行2,000文字**。先頭に`! `を付けるとヘッダを削除できます。

ファイル全体を支配する挙動が1つあります。**一致したルールは積み上がるだけで、上書きにはなりません。**
Cloudflareは「同じヘッダが`_headers`内で2回適用された場合、値はカンマ区切りで結合される」と
明記しています。広い`/*`ルールと狭い`/_astro/*`ルールの両方が`Cache-Control`を設定すると、
具体的な方が勝つのではなく、意味をなさない結合値が1本送出されます。1つのヘッダ名につき一致する
ルールは1つに保つか、`! ヘッダ名`で継承値を外してから自分の値を設定してください。

```txt
# ステージング・内部プレビューをインデックスさせない
/preview/*
  X-Robots-Tag: noindex, nofollow

# HTML以外のリソースはヘッダでしかrobots指定を持てない
/reports/*.pdf
  X-Robots-Tag: noindex, nofollow

# 長期キャッシュ可能なビルド成果物。Cache-Controlはここだけで設定し、
# これらのパスに一致する他のルールでは設定しない。
/_astro/*
  Cache-Control: public, max-age=31536000, immutable

/*
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
```

意図的に書いていないものがあります。HTML用の`Cache-Control`ルールです。デフォルトの
`auto-trailing-slash`ではページは拡張子なしのURLで配信されるため、`/*.html`パターンは実質何にも
一致しません。かといって`/*`に書くと上のアセット用ルールと衝突します。HTMLのキャッシュは
ゾーンレベルのCloudflare Cache Rulesで、SSRルートはWorkerコード側で設定してください。

### X-Robots-Tag

`X-Robots-Tag`は、HTML以外のリソース（PDF、画像、JSONフィード）にrobots指定を適用できる唯一の
手段です。これらは`<meta name="robots">`を持てないためです。metaタグと同じディレクティブ
（`noindex`・`nofollow`・`none`・`nosnippet`・`max-snippet:[n]`・`max-image-preview:[setting]`・
`max-video-preview:[n]`・`notranslate`・`noimageindex`・`unavailable_after:[date]`・
`indexifembedded`）に対応し、ユーザーエージェント名を前置すればクローラーを指定できます。

```txt
X-Robots-Tag: googlebot: nofollow
X-Robots-Tag: otherbot: noindex, nofollow
```

ユーザーエージェント指定のないルールは全クローラーに適用され、衝突時は**より制限の強い**ルールが
優先されます。

**ただしクローラー個別指定は`_headers`では表現できません。** Googleのユーザーエージェント別の書き方は
`X-Robots-Tag`を*別々のヘッダ行*として送ることを前提にしていますが、Cloudflareは「同じヘッダが
`_headers`内で2回適用された場合、値はカンマ区切りで結合される」と明記しています。2行書いても1本の
結合ヘッダとして送出され、ユーザーエージェント接頭辞を含む結合値をGoogleがどう解釈するかは
ドキュメント化されていません。クローラー個別の指定が必要なら、各行を自分で制御できるWorkerコード側で
ヘッダを設定してください。

さらに落とし穴が2つあります。

- **robots.txtでクロール拒否しているURLに付けた`noindex`ヘッダは効きません。** クローラーが
  レスポンスを取得できずヘッダを読めないためです。どちらかを選んでください。クロールを拒否するか、
  クロールを許可して`noindex`を返すか。
- プレビュー環境で`/*`に`X-Robots-Tag: noindex`を付けるのは正しい対応ですが、その設定を残したまま
  本番に昇格させると壊滅的で、しかも気づきにくいものです。環境変数で切り替えてください。

### Cache-Control

キャッシュヘッダは、サイトをクロールするコストを決めるという意味でSEOの領域です。

| リソース | 推奨値 | 理由 |
|----------|--------|------|
| ハッシュ付きアセット（`/_astro/*`、`/assets/*.[hash].js`） | `public, max-age=31536000, immutable` | 再検証されず、クロール・レンダリング予算を消費しない |
| HTML | `public, max-age=0, must-revalidate` ＋ 明示パージ付きCDNキャッシュ | 内容は最新である必要があるが、リクエストごとにオリジンを叩くべきではない |
| `sitemap.xml`、`robots.txt` | `public, max-age=3600` | クローラーが頻繁に取得する。1時間で十分に新鮮 |

オリジンが遅い場合はHTMLに`stale-while-revalidate`を使ってください。クローラーには高速な
レスポンスを返しつつ（Googleが割くクロールレートの向上につながります）、エッジは背後で更新します。

### Workerコードとのギャップ

`_headers`はWorkerが生成したレスポンスに適用されないため、SSRページのヘッダはコードで設定します。

```js
const response = await renderPage(request);
const headers = new Headers(response.headers);
headers.set('X-Robots-Tag', env.ENVIRONMENT === 'production' ? 'all' : 'noindex, nofollow');
headers.set('Cache-Control', 'public, max-age=0, must-revalidate');
return new Response(response.body, { status: response.status, headers });
```

監査は簡単です。静的URLとSSR URLをそれぞれ`curl -I`して比較し、ヘッダが違えばそこがギャップです。

## D1 / KV駆動の動的サイトマップ

エッジで生成するサイトマップは常に最新です。ビルドより速くコンテンツが変わるサイトではこれが効き
ます。生成方法にかかわらずGoogle側の制約は同じで、**1ファイルあたり50,000 URL・非圧縮50MB**、
そして`lastmod`は検証可能な正確さがある場合にのみ使われます。

### D1から生成する

```js
// src/sitemap.ts
export const PAGE_SIZE = 25000;   // 50,000 URL上限に対して十分な余裕を取る

export async function sitemapForPage(env, page) {
  const { results } = await env.DB.prepare(
    `SELECT slug, updated_at FROM posts
      WHERE published = 1
      ORDER BY updated_at DESC
      LIMIT ?1 OFFSET ?2`
  ).bind(PAGE_SIZE, page * PAGE_SIZE).all();

  // 範囲外のページには行が無い。それをここで返せば、呼び出し側は毎リクエストで
  // COUNT(*) をもう1往復させずに404を返せる。
  if (results.length === 0) return null;

  const urls = results
    .map((row) => {
      // NULLやパースできないタイムスタンプがあると toISOString() が例外を投げ、
      // サイトマップ全体を道連れにする。lastmod は任意項目であり、そもそも
      // Googleは一貫して正確な場合しか信用しないので、出さない方がよい。
      const lastmod = isoOrNull(row.updated_at);
      return (
        `  <url>\n` +
        `    <loc>${escapeXml(locFor(row.slug))}</loc>\n` +
        (lastmod ? `    <lastmod>${lastmod}</lastmod>\n` : '') +
        `  </url>`
      );
    })
    .join('\n');

  return `<?xml version="1.0" encoding="UTF-8"?>\n` +
    `<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${urls}\n</urlset>`;
}

export async function pageCount(env) {
  const { results } = await env.DB.prepare(
    'SELECT COUNT(*) AS n FROM posts WHERE published = 1'
  ).all();
  return Math.ceil(results[0].n / PAGE_SIZE);
}

function locFor(slug) {
  // 仕様が求める順序は「先にパーセントエンコード、後で実体参照」。
  // ただしセグメント単位で行う。スラッグ全体に encodeURIComponent をかけると
  // "/" までエスケープされ、"2026/my-post" のような階層スラッグが
  // /blog/2026%2Fmy-post/ という別URL——しかも404になるURL——として出力される。
  // セグメント単位なら<loc>を実際に壊す空白と非ASCIIはそのまま処理できる。
  const path = slug.split('/').filter(Boolean).map((s) => encodeURIComponent(s)).join('/');
  return `https://example.com/blog/${path}/`;
}

function isoOrNull(value) {
  if (value == null) return null;
  // SQLiteは "2026-08-01 12:00:00" 形式で保存することが多い。この空白区切りは
  // ISO 8601 ではなく、new Date() の解釈がエンジン依存になるため先に正規化する。
  const normalised = typeof value === 'string' ? value.trim().replace(' ', 'T') : value;
  const date = new Date(normalised);
  return Number.isNaN(date.getTime()) ? null : date.toISOString();
}

function escapeXml(value) {
  const ENTITIES = { '<': '&lt;', '>': '&gt;', '&': '&amp;', "'": '&apos;', '"': '&quot;' };
  let out = '';
  for (const ch of String(value)) {
    const code = ch.codePointAt(0);
    // 制御文字はXMLで不正であり、エスケープでは救えないので除去する。
    // タブ(0x09)・LF(0x0a)・CR(0x0d)だけが例外。
    if (code < 0x20 && code !== 0x09 && code !== 0x0a && code !== 0x0d) continue;
    out += ENTITIES[ch] ?? ch;
  }
  return out;
}
```

エスケープは省略できません。スラッグに`&`が含まれるとXMLが壊れ、Search Consoleはサイトマップ全体を
読み取り不能として扱います。1行の不備でファイル1つ分をまるごと失います。`<loc>`については順序も
決まっていて、サイトマップ仕様はURLを*先に*パーセントエンコードし、そのあとで実体参照する形を
求めています。`locFor()`がパスのセグメントごとにパーセントエンコードし、組み立て終えたURLを
`escapeXml()`に渡しているのはこのためです。

### サイトマップインデックスとキャッシュ

分割ファイルを指すインデックスを配信し、両方をエッジでキャッシュします。クローラーが50ファイルを
取得しにきても、データベースへのクエリが50回走らないようにするためです。

```js
// src/index.js
import { sitemapForPage, pageCount } from './sitemap.js';

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const page = url.pathname === '/sitemap-index.xml'
      ? 'index'
      : url.pathname.match(/^\/sitemap-(\d+)\.xml$/)?.[1];
    // キャッシュを触る前にルーティングする。それ以外のパスは静的アセットで、
    // このWorkerが書き込まないキーを引いても必ずミスするだけだから。
    if (page === undefined) return env.ASSETS.fetch(request);

    // caches.default が受け付けるのはGETだけ。それ以外では put() が
    // "Cannot cache response to non-GET request" を投げる。クローラーや死活監視は
    // サイトマップに日常的にHEADを送るので、この判定が無いと waitUntil の中で
    // 毎回rejectする。
    const cacheable = request.method === 'GET';
    const cache = caches.default;
    if (cacheable) {
      const cached = await cache.match(request);
      if (cached) return cached;
    }

    let body;
    if (page === 'index') {
      const pages = await pageCount(env);
      // ページ数0はURL数0であり、空のサイトマップに正当な形はない。
      // <sitemapindex>には子要素が、<urlset>には<url>が最低1つ必要だから。
      // 1に丸めても不正なドキュメントが1階層下がるだけなので、何も返さない。
      // 静的ルートもここに含めれば、そもそもこのケースは発生しない。
      if (pages === 0) return new Response('Not found', { status: 404 });
      body =
        `<?xml version="1.0" encoding="UTF-8"?>\n` +
        `<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n` +
        Array.from({ length: pages }, (_, i) =>
          `  <sitemap><loc>https://example.com/sitemap-${i}.xml</loc></sitemap>`
        ).join('\n') +
        `\n</sitemapindex>`;
    } else {
      // 抑えないと /sitemap-999999.xml が空の<urlset>を200で返す。インデックス
      // 可能なURLが無限に生まれる、このファイルが後段で警告しているクローラー
      // トラップそのものになる。sitemapForPage() は既に走らせたクエリから空
      // ページを判定して返すので、この上限チェックに追加コストはかからない。
      body = await sitemapForPage(env, Number(page));
      if (body === null) return new Response('Not found', { status: 404 });
    }

    const response = new Response(body, {
      headers: {
        'Content-Type': 'application/xml; charset=utf-8',
        'Cache-Control': 'public, max-age=3600',
      },
    });
    if (cacheable) ctx.waitUntil(cache.put(request, response.clone()));
    return response;
  },
};
```

インデックスは`robots.txt`から参照します（`Sitemap: https://example.com/sitemap-index.xml`）。
インデックスに記載するサイトマップは、インデックスと同じディレクトリかそれ以下の階層に置く必要が
あるため、ルート直下に配置してください。

KVを使う場合は、レンダリング済みXMLをキーに保存し、リクエストごとではなくCron Triggerで再生成
します。クローラーの都合でクエリが走るより安く、挙動も予測しやすくなります。

## エッジでのbotハンドリング

エッジはクローラートラフィックを制御する適切な場所であると同時に、自サイトを最も簡単に
インデックスから消せる場所でもあります。原則は1つ。**ユーザーエージェントだけでクローラーを
ブロックしない。** UA文字列は容易に偽装できるため、UAベースの許可リストは偽装者を通し、UAベースの
拒否リストは何も止められません。

### Googleクローラーの検証

Googleは検証方法を2つ公開しています。エッジで現実的なのはIPレンジ照合です。

```js
// Googleが公開するIPレンジを取得・キャッシュし、接続元IPと照合する。
// 2026年3月31日に配置が変更され、googlebot.json は common-crawlers.json に改名された。
const RANGE_FILES = [
  'https://developers.google.com/static/crawling/ipranges/common-crawlers.json',
  'https://developers.google.com/static/crawling/ipranges/special-crawlers.json',
  'https://developers.google.com/static/crawling/ipranges/user-triggered-fetchers.json',
];

async function googleRanges(env) {
  const cached = await env.BOT_KV.get('google-ranges', 'json');
  // 空配列も真値になる。length を見ないと、取得に一度失敗しただけで
  // 24時間キャッシュが汚染され、本物のクローラーを全部弾いてしまう。
  if (Array.isArray(cached) && cached.length) return cached;

  // 失敗もキャッシュする。これがないと障害中は毎リクエストで3本のfetchが
  // 再発行され、偽装UAの大量リクエストがGoogleへの外向きfetchストームに変わり、
  // Workerのサブリクエスト枠を食い潰す。
  if (await env.BOT_KV.get('google-ranges-failed')) {
    throw new Error('range lookup failed recently; backing off');
  }

  try {
    const files = await Promise.all(
      RANGE_FILES.map(async (u) => {
        const res = await fetch(u, { cf: { cacheTtl: 3600 } });
        if (!res.ok) throw new Error(`${u} -> ${res.status}`);
        return res.json();
      })
    );
    const prefixes = files.flatMap((f) => f.prefixes ?? []);
    if (!prefixes.length) throw new Error('no prefixes in Google range files');
    await env.BOT_KV.put('google-ranges', JSON.stringify(prefixes), { expirationTtl: 86400 });
    return prefixes;
  } catch (err) {
    await env.BOT_KV.put('google-ranges-failed', '1', { expirationTtl: 300 });
    throw err;
  }
}

async function isVerifiedGoogle(request, env) {
  const ua = request.headers.get('user-agent') ?? '';
  if (!/Googlebot|Google-InspectionTool|Storebot-Google/i.test(ua)) return false;

  const ip = request.headers.get('cf-connecting-ip');
  if (!ip) return false;

  let prefixes;
  try {
    prefixes = await googleRanges(env);
  } catch (err) {
    // フェイルオープンにするのは、**この関数が制御するのがレート制限だから**。
    // 障害中は偽装したGooglebot UAがすべて検証済み扱いになる。これはこのファイル
    // が禁じているUAだけの信用そのもので、失うものがレート制限の適用だけなら許容
    // できるが、コンテンツやアクセスを制御する判定なら決して許容できない。その
    // 場合はフェイルクローズにし、再試行の頻度は上の失敗キャッシュで抑える。
    console.error('crawler range lookup failed', err);
    return true;
  }

  const wantV6 = ip.includes(':');
  return prefixes.some((p) => {
    const cidr = wantV6 ? p.ipv6Prefix : p.ipv4Prefix;
    return cidr ? ipInCidr(ip, cidr) : false;
  });
}
```

`ipInCidr` は自前で用意します。IPv4は数行で済みますが、IPv6はアドレスが32ビット整数に収まらないため
BigIntが必要です。

```js
// 解析できない入力にはnullを返す。例外は投げない。この処理は
// isVerifiedGoogle のprefixループ内、つまりtry/catchの**外**で走るため、
// ここで例外が出るとこの判定が識別しようとしている当のクローラーに5xxを返す。
function ipToBigInt(ip) {
  if (ip.includes(':')) {
    const parts = ip.split('::');
    if (parts.length > 2) return null;            // "::" は1回まで
    const [head, tail = ''] = parts;
    const left = head ? head.split(':') : [];
    const right = tail ? tail.split(':') : [];

    // IPv4射影アドレスは末尾がドット区切り（"::ffff:192.0.2.1"）。
    // parseInt('192.0.2.1', 16) はエラーなく402を返してしまうので、
    // その値を通さずに16ビット×2グループへ展開する。
    const tailGroups = right.length ? right : left;
    const last = tailGroups[tailGroups.length - 1];
    if (last && last.includes('.')) {
      const octets = last.split('.').map(Number);
      if (octets.length !== 4) return null;
      if (octets.some((n) => !Number.isInteger(n) || n < 0 || n > 255)) return null;
      tailGroups.splice(-1, 1,
        ((octets[0] << 8) | octets[1]).toString(16),
        ((octets[2] << 8) | octets[3]).toString(16));
    }

    const fill = 8 - left.length - right.length;
    if (fill < 0 || (fill > 0 && parts.length !== 2)) return null;
    const groups = [...left, ...Array(fill).fill('0'), ...right];

    let acc = 0n;
    for (const g of groups) {
      // BigInt(NaN) は RangeError を投げるので、グループ側で弾く。
      if (!/^[0-9a-f]{1,4}$/i.test(g || '0')) return null;
      acc = (acc << 16n) | BigInt(parseInt(g || '0', 16));
    }
    return acc;
  }

  const octets = ip.split('.');
  if (octets.length !== 4) return null;
  let acc = 0n;
  for (const o of octets) {
    if (!/^\d{1,3}$/.test(o) || Number(o) > 255) return null;
    acc = (acc << 8n) | BigInt(Number(o));
  }
  return acc;
}

function ipInCidr(ip, cidr) {
  const [network, bitsRaw] = cidr.split('/');
  if (!network || !/^\d{1,3}$/.test(bitsRaw ?? '')) return false;
  if (ip.includes(':') !== network.includes(':')) return false;   // アドレスファミリ不一致

  const width = network.includes(':') ? 128n : 32n;
  const bits = BigInt(bitsRaw);
  if (bits > width) return false;

  const addr = ipToBigInt(ip);
  const net = ipToBigInt(network);
  if (addr === null || net === null) return false;

  const mask = bits === 0n ? 0n : (~0n << (width - bits)) & ((1n << width) - 1n);
  return (addr & mask) === (net & mask);
}
```

なお、Cloudflareのbot検出は同じ判定を既に行っています。有料プランならVerified Botsのシグナルを
使う方が確実で、上のコードはWorkerのロジック内で判定したい場合の実装例です。

公開されているファイルは`common-crawlers.json`（Googlebot系）、`special-crawlers.json`（AdsBot等）、
`user-triggered-fetchers.json`、`user-triggered-fetchers-google.json`、`user-triggered-agents.json`
で、アドレスはCIDR形式です。これらに含まれないGoogleのIPは
`https://www.gstatic.com/ipranges/goog.json`に掲載されています。もう1つの方法は逆引きDNSで、
PTRレコードが`googlebot.com`・`google.com`・`googleusercontent.com`のいずれかに解決し、その名前を
正引きすると元のIPに戻ることを確認します。

CloudflareにはVerified Botsプログラムがあり、**Web Bot Auth**にも対応しています。エージェントが
リクエストに署名する方式です（`Signature`・`Signature-Input`・`Signature-Agent`ヘッダ、Ed25519鍵）。
利用できる場合、暗号署名はどのIPリストよりも強い検証手段です。

### AIクローラー

AIクローラーへの方針はrobots.txtで決めるビジネス判断です（`ai-search.md`参照）。エッジはそれを
*強制*する場所です。robots.txtはあくまで任意遵守だからです。Cloudflareの**AI Crawl Control**
（旧AI Audit）は、どのAIサービスがサイトを取得しているかを可視化し、クローラー個別の許可・拒否
ルール、robots.txt遵守状況の追跡、プライベートベータのpay-per-crawlモデルを提供します。全プラン
で利用できます。

ブロックする前に、`ai-search.md`の2つの問いを分けて考えてください。「自分のコンテンツをモデルの
学習に使ってよいか」と「AI検索が自分を引用・リンクしてよいか」です。後者をエッジでブロックすると、
robots.txtだけでは失わなかったはずの流入まで失います。

### 誤ブロックを避ける

過剰なエッジ防御はサイトを静かにインデックスから外します。次の点に注意してください。

- **検証済みの検索クローラーにチャレンジやレート制限をかけない。** GooglebotにCAPTCHAを返す
  ページはインデックスされません。
- **一時的なブロックは403ではなく503を返す。** `Retry-After`付きの503は「あとで来い」という意味に
  なります。403や404は「もう存在しない」と伝わり、いずれインデックスから削除されます。
- **クローラーに別のHTMLを返さない。** 検証済みの身元に応じてレート制限を調整するのは問題ありませんが、
  ユーザーエージェントによって内容を変えるのはクローキングです。
- **地域ブロックに注意。** Googlebotは主に米国のIPアドレスからクロールします。米国を除外する国別
  ブロックはGoogleをブロックします。
- **WAF変更のたびにテストする。**
  `curl -A "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"`
  でページを取得して200と完全なHTMLを確認し、その後Search ConsoleのURL検査でGoogle側の見え方も
  確認してください。

## HTMLRewriterによるメタデータ書き換え

`HTMLRewriter`はWorkerを通過するHTMLをストリーミングのまま変換します。ドキュメント全体をバッファ
しません。自分で制御できないHTML（レガシーなオリジン、変更できないCMS、A/Bテスト中のタイトル）に
対する配信直前のメタデータ修正に適したツールです。

### タイトルとメタタグの書き換え

```js
class MetaRewriter {
  constructor(meta) {
    this.meta = meta;
  }

  element(element) {
    // ハンドラが例外を投げるとパースが停止しレスポンスボディがエラーになる。
    // メタデータの微修正が5xxに化けるので、例外を外に出さない。
    try {
      if (element.tagName === 'title') {
        if (this.meta.title) element.setInnerContent(this.meta.title);
        return;
      }
      const name = element.getAttribute('name') ?? element.getAttribute('property');
      if (name === 'description' && this.meta.description) {
        element.setAttribute('content', this.meta.description);
      }
      if (name === 'og:title' && this.meta.title) {
        element.setAttribute('content', this.meta.title);
      }
    } catch (err) {
      console.error('meta rewrite failed', err);
    }
  }
}

export default {
  async fetch(request, env) {
    const response = await env.ASSETS.fetch(request);
    if (!response.headers.get('content-type')?.includes('text/html')) return response;

    const meta = await env.META.get(new URL(request.url).pathname, 'json');
    if (!meta) return response;

    const rewriter = new MetaRewriter(meta);
    return new HTMLRewriter()
      // `title` ではなく `head > title`。裸のセレクタはインラインSVG内の
      // <title> にも一致し、アイコンのツールチップまで書き換えてしまう。
      .on('head > title', rewriter)
      .on('head > meta', rewriter)
      .transform(response);
  },
};
```

このコードが**やらないこと**が2つあります。既存のタグを編集するだけで、存在しない
`<meta name="description">`は追加できません（HTMLRewriterはストリーミングなので、追加は次節の
`head`へのappendで行います）。そして、そもそもWorkerがリクエストを見られること、つまりHTMLのパスが
`run_worker_first`に入っていることが前提です。

### 構造化データの注入

JSON-LDの追加は`<head>`へのappendが安全です。既存のマークアップを一切壊しません。

```js
class JsonLdInjector {
  constructor(data) {
    this.payload = JSON.stringify(data).replace(/</g, '\\u003c');
  }
  element(head) {
    head.append(
      `<script type="application/ld+json">${this.payload}</script>`,
      { html: true }
    );
  }
}

// new HTMLRewriter().on('head', new JsonLdInjector(graph)).transform(response)
```

`<`をUnicodeエスケープすることで、値に`</script>`が含まれていてもタグが途中で閉じられません。
サーバーサイドテンプレートと同じ注意点です。

### 注意点

- **テキストはチャンク単位で届く。** Cloudflareは「テキストチャンクはテキストノードと同じもの
  ではない」と警告しています。1つのテキストノードが複数回の`text()`呼び出しに分かれて届くことが
  あります。文字列全体を見たい場合は`lastInTextNode`が真になるまで蓄積してください。
- **ハンドラが例外を投げるとレスポンスが死ぬ。** 例外はパースを停止させレスポンスボディをエラーに
  します。メタデータの微修正が5xxに化けます。ハンドラ本体は`try/catch`で囲んでください。
- **HTML以外は書き換えない。** 先に`content-type`を確認してください。JSONやXMLにRewriterを通すのは
  CPUの無駄で、出力を壊す可能性もあります。
- **書き換えは恒久的な修正ではない。** エッジで当てたメタデータはリポジトリを読む人には見えません。
  HTMLRewriterはオリジンを直すまでの橋渡しと位置づけ、なぜ存在するかを記録してください。

## エッジキャッシュとクロールバジェット

クロールバジェットは、クローラーが「どれだけ取得したいか」と、サイトが「無理なくどれだけ取得
させられるか」の関数です。レスポンスが遅くなったりエラーが出たりするとGoogleはクロールレートを
下げます。健全なエッジキャッシュはその上限を引き上げます。

実際に効くのは次の点です。

- **クローラーにもキャッシュから配信する。** エッジのヒット率が高いとTTFBが低く安定します。
  Googleのクロールレート判定はまさにそこを見ています。
- **5xxは即座に直す。** サーバーエラーが続くと、Googleは該当URLだけでなくサイト全体のクロールを
  抑制します。
- **無限のURL空間にクローラーを迷い込ませない。** ファセットナビゲーション、カレンダー、ソート
  パラメータは無制限にURLを生成します。エッジで処理する（それでも1回の取得コストは発生する）より、
  robots.txtでパターン単位にブロックし、クロール段階で止めてください。
- **可能なら304を返す。** `If-Modified-Since` / `If-None-Match`を尊重すれば、クローラーは安価に
  再検証できます。
- **恒久的に削除したコンテンツには410を使う。** 意図を正確に伝えられるからです。404より速く処理
  されるとGoogleは明言していないので、速度ではなく正確さを理由に選んでください。
- **サイトマップの`lastmod`を正直に保つ。** Googleは一貫して正確な場合にのみこの値を使います。
  全URLに今日の日付を打つのは、この項目を無視するよう学習させる行為です。

クロールバジェットが本当に制約になるのは大規模サイト（おおむね、クローラーが数日で取得しきれない
規模）だけです。数千ページ規模ならコンテンツと内部リンクに労力を割いたほうが効果的です。

## エッジSEOチェックリスト

- [ ] `_redirects`の全ルールがステータスコードを明示している（デフォルトは302）
- [ ] リダイレクトの連鎖がなく、ルールは個別→ワイルドカードの順に並んでいる
- [ ] リダイレクト件数が静的2,000件／動的100件に収まっている、またはKVバックエンドのWorkerへ移した
- [ ] HTTP→HTTPSとホスト正規化は`_redirects`ではなくゾーンレベルで処理している
- [ ] SSRルートは`X-Robots-Tag`と`Cache-Control`をコードで設定している（`_headers`は届かない）
- [ ] robots.txtでクロール拒否しているURLに`X-Robots-Tag: noindex`を付けていない
- [ ] プレビュー・ステージングの`noindex`は環境変数で制御し、ハードコードしていない
- [ ] ハッシュ付きアセットは`immutable`、HTMLは再検証、サイトマップ・robotsは約1時間キャッシュ
- [ ] 動的サイトマップは全フィールドをXMLエスケープし、1ファイル50,000 URL／50MB以内に収めている
- [ ] サイトマップのレスポンスをエッジキャッシュし、クロールがDB負荷試験にならないようにしている
- [ ] クローラーの識別はIPレンジ（またはWeb Bot Auth）で検証し、ユーザーエージェント単独では判定しない
- [ ] 一時的なブロックは403/404ではなく503＋`Retry-After`を返す
- [ ] 検証済みの検索クローラーはWAFチャレンジとレート制限の対象外にしている
- [ ] HTMLRewriterのハンドラは`content-type`を確認し、例外を捕捉し、注入するJSON-LDをエスケープしている

## 公式リソース

- [Cloudflare Workers static assets](https://developers.cloudflare.com/workers/static-assets/)
- [Redirects (Workers)](https://developers.cloudflare.com/workers/static-assets/redirects/) / [Redirects (Pages)](https://developers.cloudflare.com/pages/configuration/redirects/)
- [Headers (Workers)](https://developers.cloudflare.com/workers/static-assets/headers/) / [Headers (Pages)](https://developers.cloudflare.com/pages/configuration/headers/)
- [HTMLRewriter](https://developers.cloudflare.com/workers/runtime-apis/html-rewriter/)
- [Verified bots](https://developers.cloudflare.com/bots/concepts/bot/verified-bots/) と [Web Bot Auth](https://developers.cloudflare.com/bots/reference/bot-verification/web-bot-auth/)
- [AI Crawl Control](https://developers.cloudflare.com/ai-crawl-control/)
- [Googlebotなどのクローラーの確認](https://developers.google.com/search/docs/crawling-indexing/verifying-googlebot)
- [X-Robots-Tag ディレクティブ](https://developers.google.com/search/docs/crawling-indexing/robots-meta-tag)
- [大規模なサイトマップ](https://developers.google.com/search/docs/crawling-indexing/sitemaps/large-sitemaps)
