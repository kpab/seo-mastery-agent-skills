import rss from '@astrojs/rss';
import type { APIRoute } from 'astro';
import { copy } from '../../data/content';
import { releasePath, releasesFor } from '../../data/releases';
import { site } from '../../data/site';

export const GET: APIRoute = async (context) => {
  const releases = await releasesFor('en');
  return rss({
    title: `${site.name} — ${copy.en.releases.heading}`,
    description: copy.en.releases.metaDescription,
    site: context.site ?? site.origin,
    items: releases.map((entry) => ({
      title: `${entry.data.version} — ${entry.data.title}`,
      description: entry.data.summary,
      pubDate: entry.data.date,
      link: releasePath('en', entry.data.slug),
    })),
    customData: '<language>en-us</language>',
  });
};
