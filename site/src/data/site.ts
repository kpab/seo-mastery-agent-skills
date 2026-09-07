/** サイト全体で使う定数。数字は marketplace.json / SKILL.md と一致させる */
export const site = {
  name: 'SEO Mastery Agent Skills',
  origin: 'https://seo.kpab.dev',
  repo: 'https://github.com/kpab/seo-mastery-agent-skills',
  author: 'kpab',
  authorUrl: 'https://kpab.dev',
  license: 'MIT',
  version: '1.5.0',
  lastVerified: '2026-09-07',
} as const;

export const marketplaceCmd = 'claude plugin marketplace add kpab/seo-mastery-agent-skills';
export const installCmd = 'claude plugin install seo-mastery@seo-mastery-agent-skills';

export type Locale = 'en' | 'ja';

export const ogLocale: Record<Locale, string> = { en: 'en_US', ja: 'ja_JP' };

/** 現在のパスから言語を判定する。/ja 配下だけが日本語 */
export function localeFromPath(pathname: string): Locale {
  return pathname === '/ja' || pathname.startsWith('/ja/') ? 'ja' : 'en';
}

/** hreflang 用に、同じページの各言語版パスを返す */
export function alternatePaths(pathname: string) {
  const en = pathname.replace(/^\/ja(?=\/|$)/, '') || '/';
  return { en, ja: en === '/' ? '/ja' : `/ja${en}` };
}
