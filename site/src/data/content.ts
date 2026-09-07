import type { Locale } from './site';

export interface Item {
  title: string;
  body: string;
}

export interface Copy {
  htmlLang: string;
  meta: { title: string; description: string };
  nav: { coverage: string; install: string; freshness: string; faq: string; releases: string; repo: string; lang: string; menu: string };
  hero: {
    eyebrow: string;
    heading: string;
    lead: string;
    primary: string;
    secondary: string;
    badges: string[];
  };
  install: { label: string; heading: string; note: string; steps: { caption: string; cmd: string }[]; alt: string; altBody: string };
  why: { label: string; heading: string; items: Item[] };
  coverage: { label: string; heading: string; lead: string; items: Item[] };
  usage: { label: string; heading: string; lead: string; prompts: string[]; reply: string };
  files: { label: string; heading: string; lead: string; note: string };
  freshness: { label: string; heading: string; lead: string; items: Item[] };
  faq: { label: string; heading: string; items: { q: string; a: string }[] };
  cta: { heading: string; body: string; primary: string; secondary: string };
  footer: { built: string; license: string; skill: string };
  releases: {
    metaTitle: string;
    metaDescription: string;
    heading: string;
    lead: string;
    latest: string;
    all: string;
    changelog: string;
    back: string;
    published: string;
    updated: string;
    detailSuffix: string;
    breadcrumbHome: string;
  };
}

const en: Copy = {
  htmlLang: 'en',
  meta: {
    title: 'SEO Mastery — an SEO Agent Skill for Claude Code and Codex',
    description:
      'A Markdown-only Agent Skill that gives Claude Code and Codex reproducible SEO judgement: technical SEO, JSON-LD, Core Web Vitals, E-E-A-T, AI search, Astro and Cloudflare edge SEO, and site audits.',
  },
  nav: {
    coverage: 'Coverage',
    install: 'Install',
    freshness: 'Freshness',
    faq: 'FAQ',
    releases: 'Releases',
    repo: 'GitHub',
    lang: '日本語',
    menu: 'Menu',
  },
  hero: {
    eyebrow: 'Agent Skill for Claude Code & Codex',
    heading: 'SEO your agent can actually reproduce.',
    lead: "Google publishes the criteria. This skill turns them into steps an agent follows — technical SEO, structured data, Core Web Vitals, E-E-A-T, AI search, and full site audits. Markdown only: no API key, no MCP server, nothing to run.",
    primary: 'Install the skill',
    secondary: 'View on GitHub',
    badges: ['Markdown only', 'English & Japanese', 'MIT licensed'],
  },
  install: {
    label: 'Install',
    heading: 'Two commands.',
    note: 'Installs both the English and Japanese skills, and keeps them updatable through the plugin manager.',
    steps: [
      { caption: 'Add the marketplace', cmd: 'claude plugin marketplace add kpab/seo-mastery-agent-skills' },
      { caption: 'Install the plugin', cmd: 'claude plugin install seo-mastery@seo-mastery-agent-skills' },
    ],
    alt: 'Prefer to copy the files?',
    altBody:
      'Clone the repository and copy .claude/skills/seo-mastery into your project — or into .codex/skills for Codex. A skill is SKILL.md plus its reference files: copy the whole folder, not just SKILL.md.',
  },
  why: {
    label: 'Why this one',
    heading: 'Three things it does differently.',
    items: [
      {
        title: 'Zero dependency',
        body: 'Markdown files and nothing else. No API keys to provision, no MCP server to keep alive, no install script. Copy the folder and it works offline.',
      },
      {
        title: 'Strong on edge and static sites',
        body: 'Dedicated reference layers for Astro and Cloudflare Workers/Pages: island hydration against INP and LCP, the blind spots of _redirects and _headers next to Worker code, dynamic sitemaps out of D1 or KV, crawler verification at the edge.',
      },
      {
        title: 'Staleness is tracked, not hoped away',
        body: 'Every reference file carries a last_verified date that CI enforces. Corrected claims trace back to a primary source in research-notes.md, releases follow semver, and a scheduled workflow opens a re-verification issue every month.',
      },
    ],
  },
  coverage: {
    label: 'Coverage',
    heading: 'Eight reference files behind one skill.',
    lead: 'SKILL.md routes the request; the reference file that matches gets loaded. Both language versions ship the same eight.',
    items: [
      { title: 'Technical SEO', body: 'robots.txt, sitemaps, canonical, hreflang, index coverage, redirect and status-code handling.' },
      { title: 'Content SEO', body: 'Meta tags, heading structure, internal linking, and E-E-A-T signals that reviewers can actually check.' },
      { title: 'Structured data', body: 'JSON-LD templates: Article, Product, LocalBusiness, BreadcrumbList, VideoObject, Organization, WebSite, Event.' },
      { title: 'Core Web Vitals', body: 'LCP, INP and CLS — the causes, the fixes as code, and the measurement scripts to confirm them.' },
      { title: 'AI search / GEO / LLMO', body: 'AI Overviews and AI Mode, crawler control for GPTBot, ClaudeBot and Google-Extended, citation-ready content, entity clarity, information gain.' },
      { title: 'Astro SEO', body: 'Client directives against hydration cost, @astrojs/sitemap, ClientRouter, content collections. Verified against Astro 6.' },
      { title: 'Edge SEO', body: 'Cloudflare Workers and Pages: _redirects, _headers, X-Robots-Tag, HTMLRewriter, D1/KV sitemaps, Pages Functions.' },
      { title: 'Audit workflow', body: 'A staged audit process and the report format that comes out of it, so two runs on the same site are comparable.' },
    ],
  },
  usage: {
    label: 'Usage',
    heading: 'Ask in plain language.',
    lead: 'The skill description carries the routing. You do not name the file, and you do not name the skill.',
    prompts: [
      'Optimize the meta tags for this page',
      'Add Article structured data to this blog post',
      'Run an SEO audit on this site',
      'How can I improve LCP here?',
      'Should this site have an llms.txt?',
    ],
    reply: 'Claude loads seo-mastery, opens the reference file that matches, and answers against the criteria in it — not against a half-remembered blog post.',
  },
  files: {
    label: 'Layout',
    heading: 'What lands in your repo.',
    lead: 'Two skills, English and Japanese, kept in sync by CI. English is the source of truth.',
    note: 'Fetching SKILL.md alone leaves the skill incomplete — the reference files are where the criteria live.',
  },
  freshness: {
    label: 'Freshness',
    heading: 'What is guaranteed, and what is not.',
    lead: 'SEO guidance rots. This repository does not claim every line is currently correct; it guarantees the process and the date stamp.',
    items: [
      { title: 'Date-stamped', body: 'Every file under .claude/skills carries last_verified in its frontmatter. CI checks it is present, valid, not in the future, and identical between the English and Japanese versions.' },
      { title: 'Sourced', body: 'Claims added or corrected in a verification pass are traceable to a primary source in docs/research-notes.md — the vendor documentation, not a summary of it.' },
      { title: 'Versioned', body: 'Semver read for a knowledge base: MAJOR for reversed guidance or a removed file, MINOR for new knowledge, PATCH for corrections and freshness. The release workflow fails if SKILL.md, both manifests, the CHANGELOG heading and the git tag disagree.' },
      { title: 'Re-checked on a schedule', body: 'A scheduled workflow opens a re-verification issue every month, so a stale claim surfaces as work rather than sitting quietly in a file.' },
    ],
  },
  faq: {
    label: 'FAQ',
    heading: 'Questions worth answering up front.',
    items: [
      {
        q: 'Does it work with Codex, or only Claude Code?',
        a: 'Both. The skill is plain Markdown, so it works anywhere a skills directory is read. For Codex, copy the folder into .codex/skills for a project or ~/.codex/skills globally.',
      },
      {
        q: 'English or Japanese — which one do I install?',
        a: 'Both ship together and you load whichever matches the language you write in. seo-mastery for English, seo-mastery-jp for Japanese. Loading both at once is not intended.',
      },
      {
        q: 'Does it guarantee rankings or AI citations?',
        a: 'No, and it says so. GEO, LLMO and AEO are working terms, not levers. Generative-visibility recommendations are labelled High, Medium or Experimental so you can tell an established practice from a bet.',
      },
      {
        q: 'Does it need an API key or a server?',
        a: 'No. There is no API key, no MCP server, no script to run. Copy the folder and the skill works offline.',
      },
      {
        q: 'Which frameworks are covered?',
        a: 'Astro and Cloudflare Workers/Pages have dedicated reference files. Next.js and Nuxt 3+ appear as code examples. Everything else — WordPress, Rails, Django — is covered by the framework-agnostic guidance only.',
      },
    ],
  },
  cta: {
    heading: 'Put the criteria in the repo.',
    body: 'MIT licensed. Pull requests and issues welcome — the English and Japanese versions have to stay in sync.',
    primary: 'Install the skill',
    secondary: 'Read the source',
  },
  footer: { built: 'Built by', license: 'MIT License', skill: 'Skill version' },
  releases: {
    metaTitle: 'Releases — SEO Mastery Agent Skills',
    metaDescription:
      'What changed in each version of the seo-mastery and seo-mastery-jp Agent Skills: new reference files, corrected claims, and the freshness passes behind them.',
    heading: 'Releases',
    lead:
      'Both skills share one version number. A MAJOR bump means reversed guidance or a removed file, MINOR means new knowledge, PATCH means corrections and freshness work.',
    latest: 'Latest',
    all: 'All releases',
    changelog: 'Full CHANGELOG on GitHub',
    back: 'All releases',
    published: 'Published',
    updated: 'Updated',
    detailSuffix: 'SEO Mastery Agent Skills',
    breadcrumbHome: 'Home',
  },
};

const ja: Copy = {
  htmlLang: 'ja',
  meta: {
    title: 'SEO Mastery — Claude Code / Codex 用の SEO エージェントスキル',
    description:
      'Markdown だけでできた SEO エージェントスキル。技術 SEO、JSON-LD、Core Web Vitals、E-E-A-T、AI 検索、Astro・Cloudflare エッジ SEO、サイト監査を、エージェントが再現できる手順として渡します。',
  },
  nav: {
    coverage: '範囲',
    install: '導入',
    freshness: '鮮度',
    faq: 'FAQ',
    releases: 'お知らせ',
    repo: 'GitHub',
    lang: 'English',
    menu: 'メニュー',
  },
  hero: {
    eyebrow: 'Claude Code / Codex 用エージェントスキル',
    heading: 'SEO の判断を、エージェントが再現できる形に。',
    lead: '判断基準は公開されている。それを手順に落としたのがこのスキルです。技術 SEO、構造化データ、Core Web Vitals、E-E-A-T、AI 検索、サイト監査までを扱います。中身は Markdown だけ。API キーも MCP サーバーも要りません。',
    primary: 'スキルを入れる',
    secondary: 'GitHub で見る',
    badges: ['Markdown のみ', '日本語・英語', 'MIT ライセンス'],
  },
  install: {
    label: '導入',
    heading: 'コマンド 2 つ。',
    note: '英語版と日本語版の両方が入り、プラグインマネージャーからそのまま更新できます。',
    steps: [
      { caption: 'マーケットプレイスを追加', cmd: 'claude plugin marketplace add kpab/seo-mastery-agent-skills' },
      { caption: 'プラグインを入れる', cmd: 'claude plugin install seo-mastery@seo-mastery-agent-skills' },
    ],
    alt: 'ファイルを直接置きたい場合',
    altBody:
      'リポジトリをクローンして .claude/skills/seo-mastery をプロジェクトへコピーします。Codex なら .codex/skills が置き場所です。スキルは SKILL.md と参照ファイルで 1 組なので、SKILL.md だけを取ると欠けた状態になります。',
  },
  why: {
    label: '特徴',
    heading: 'ほかと違うのは 3 点。',
    items: [
      {
        title: '依存ゼロ',
        body: '中身は Markdown だけ。用意する API キーも、動かし続ける MCP サーバーも、実行するスクリプトもありません。フォルダを置けばオフラインで動きます。',
      },
      {
        title: 'エッジと静的サイトに厚い',
        body: 'Astro と Cloudflare Workers / Pages に専用の参照ファイルがあります。アイランドの水和と INP・LCP の関係、_redirects と _headers が Worker のコードと組んだときの死角、D1 / KV から作る動的サイトマップ、エッジでのクローラー検証まで扱います。',
      },
      {
        title: '古びを追跡する',
        body: 'すべての参照ファイルが last_verified の日付を持ち、CI がそれを検査します。検証で直した記述は docs/research-notes.md の一次情報まで辿れ、リリースは semver に従い、毎月の定期ワークフローが再検証の issue を立てます。',
      },
    ],
  },
  coverage: {
    label: '範囲',
    heading: '1 つのスキルの裏に、参照ファイル 8 枚。',
    lead: '振り分けは SKILL.md が担い、合致した参照ファイルだけが読み込まれます。日本語版・英語版とも同じ 8 枚です。',
    items: [
      { title: '技術 SEO', body: 'robots.txt、サイトマップ、canonical、hreflang、インデックス状況、リダイレクトとステータスコードの扱い。' },
      { title: 'コンテンツ SEO', body: 'メタタグ、見出し構造、内部リンク、そして実際に確認できる形の E-E-A-T シグナル。' },
      { title: '構造化データ', body: 'JSON-LD テンプレート。Article、Product、LocalBusiness、BreadcrumbList、VideoObject、Organization、WebSite、Event。' },
      { title: 'Core Web Vitals', body: 'LCP・INP・CLS の原因、コードとしての対処、そして直ったことを確かめる計測スクリプト。' },
      { title: 'AI 検索 / GEO / LLMO', body: 'AI Overviews と AI モード、GPTBot・ClaudeBot・Google-Extended のクローラー制御、引用されやすい書き方、エンティティの明確化、情報の独自性。' },
      { title: 'Astro SEO', body: 'client ディレクティブと水和コスト、@astrojs/sitemap、ClientRouter、Content Collections。Astro 6 で検証済み。' },
      { title: 'エッジ SEO', body: 'Cloudflare Workers / Pages。_redirects、_headers、X-Robots-Tag、HTMLRewriter、D1 / KV のサイトマップ、Pages Functions。' },
      { title: '監査ワークフロー', body: '段階を踏む監査手順と、そこから出るレポート形式。同じサイトを 2 回測ったときに比べられます。' },
    ],
  },
  usage: {
    label: '使い方',
    heading: '普通の言葉で頼む。',
    lead: '振り分けはスキルの description が持っています。ファイル名もスキル名も、こちらから指定しません。',
    prompts: [
      'このページのメタタグを最適化して',
      'この記事に Article 構造化データを追加して',
      'このサイトの SEO 監査をして',
      'ここの LCP はどう改善できる？',
      'このサイトに llms.txt は必要？',
    ],
    reply: 'Claude が seo-mastery を読み込み、合致する参照ファイルを開き、そこにある基準に沿って答えます。うろ覚えの記事ではなく。',
  },
  files: {
    label: '構成',
    heading: 'リポジトリに入るもの。',
    lead: '英語版と日本語版の 2 つ。CI で同期を保っており、正本は英語版です。',
    note: 'SKILL.md だけを取ると欠けた状態になります。基準が書いてあるのは参照ファイルのほうです。',
  },
  freshness: {
    label: '鮮度',
    heading: '保証していること、していないこと。',
    lead: 'SEO の情報は古びます。このリポジトリは「全行がいま正しい」とは主張しません。保証しているのは、手順と日付です。',
    items: [
      { title: '日付が入っている', body: '.claude/skills 配下のすべてのファイルが frontmatter に last_verified を持ちます。存在すること、日付として妥当なこと、未来でないこと、英語版と日本語版で一致していることを CI が検査します。' },
      { title: '出典が辿れる', body: '検証で追加・修正した記述は docs/research-notes.md から一次情報へ辿れます。まとめ記事ではなく、提供元のドキュメントです。' },
      { title: 'バージョンが付く', body: '知識ベースとして読み替えた semver。MAJOR は助言の反転や参照ファイルの削除、MINOR は知識の追加、PATCH は修正と鮮度更新。SKILL.md・2 つのマニフェスト・CHANGELOG の見出し・git タグが食い違うとリリースが落ちます。' },
      { title: '定期的に見直す', body: '毎月、定期ワークフローが再検証の issue を立てます。古びた記述がファイルの中で黙って残らず、作業として表に出ます。' },
    ],
  },
  faq: {
    label: 'FAQ',
    heading: '先に答えておきたいこと。',
    items: [
      {
        q: 'Codex でも使えますか。Claude Code 専用ですか。',
        a: '両方で使えます。中身は素の Markdown なので、スキルのディレクトリを読む環境ならどこでも動きます。Codex ではプロジェクトの .codex/skills、または全体の ~/.codex/skills にフォルダを置いてください。',
      },
      {
        q: '英語版と日本語版、どちらを入れますか。',
        a: '両方が同時に入ります。読み込むのは、自分が書く言語に合うほうです。英語なら seo-mastery、日本語なら seo-mastery-jp。同時に両方を読み込む使い方は想定していません。',
      },
      {
        q: '順位や AI の引用は保証されますか。',
        a: 'されません。そう明記しています。GEO・LLMO・AEO は作業用の呼び名であって、操作できるレバーではありません。生成 AI 上の可視性に関する推奨には High / Medium / Experimental の区別を付けてあり、確立した手法と賭けを見分けられます。',
      },
      {
        q: 'API キーやサーバーは要りますか。',
        a: '要りません。API キーも MCP サーバーも、実行するスクリプトもありません。フォルダを置けばオフラインで動きます。',
      },
      {
        q: '対応フレームワークは。',
        a: 'Astro と Cloudflare Workers / Pages には専用の参照ファイルがあります。Next.js と Nuxt 3+ はコード例として登場します。それ以外（WordPress、Rails、Django など）は、フレームワークに依らない記述だけでの対応です。',
      },
    ],
  },
  cta: {
    heading: '判断基準を、リポジトリの中に置く。',
    body: 'MIT ライセンス。プルリクエストと issue を歓迎します。ただし英語版と日本語版は同期させてください。',
    primary: 'スキルを入れる',
    secondary: 'ソースを読む',
  },
  footer: { built: '作者', license: 'MIT License', skill: 'スキルのバージョン' },
  releases: {
    metaTitle: 'お知らせ・リリースノート — SEO Mastery Agent Skills',
    metaDescription:
      'seo-mastery / seo-mastery-jp スキルの各バージョンで何が変わったか。参照ファイルの追加、記述の修正、そのもとになった検証を版ごとに記録しています。',
    heading: 'お知らせ',
    lead:
      '2 つのスキルは版番号を共有します。MAJOR は助言の反転か参照ファイルの削除、MINOR は知識の追加、PATCH は修正と鮮度更新です。',
    latest: '最新',
    all: 'すべてのリリース',
    changelog: 'GitHub の CHANGELOG を見る',
    back: 'お知らせ一覧',
    published: '公開',
    updated: '更新',
    detailSuffix: 'SEO Mastery Agent Skills',
    breadcrumbHome: 'ホーム',
  },
};

export const copy: Record<Locale, Copy> = { en, ja };
