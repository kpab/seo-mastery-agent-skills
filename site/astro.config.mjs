import sitemap from '@astrojs/sitemap';
import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://seo.kpab.dev',
  output: 'static',
  // canonical・内部リンク・サイトマップをすべて末尾スラッシュなしに揃える
  trailingSlash: 'never',
  i18n: {
    defaultLocale: 'en',
    locales: ['en', 'ja'],
    routing: { prefixDefaultLocale: false },
  },
  integrations: [
    sitemap({
      // 404 は noindex。サイトマップに載せると矛盾したシグナルになる
      filter: (page) => !page.endsWith('/404'),
      i18n: {
        defaultLocale: 'en',
        locales: { en: 'en-US', ja: 'ja-JP' },
      },
    }),
  ],
});
