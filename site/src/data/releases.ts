import { getCollection, type CollectionEntry } from 'astro:content';
import type { Locale } from './site';

export type Release = CollectionEntry<'releases'>;

/** glob loader の id は `<lang>/<slug>`。言語で絞って新しい順に返す */
export async function releasesFor(locale: Locale): Promise<Release[]> {
  const all = await getCollection('releases');
  return all
    .filter((entry) => entry.id.startsWith(`${locale}/`))
    .sort((a, b) => b.data.date.getTime() - a.data.date.getTime());
}

/** id は `<lang>/<slug>`。URL セグメントは後ろ半分 */
export function slugOf(entry: Release): string {
  return entry.id.slice(entry.id.indexOf('/') + 1);
}

export function releasePath(locale: Locale, slug: string): string {
  return locale === 'ja' ? `/ja/releases/${slug}` : `/releases/${slug}`;
}

export function releaseIndexPath(locale: Locale): string {
  return locale === 'ja' ? '/ja/releases' : '/releases';
}

/** 表示用の日付。ロケールに合わせるが、machine readable な値は datetime 属性で別に出す */
export function formatDate(date: Date, locale: Locale): string {
  return new Intl.DateTimeFormat(locale === 'ja' ? 'ja-JP' : 'en-US', {
    year: 'numeric',
    month: locale === 'ja' ? 'long' : 'short',
    day: 'numeric',
    timeZone: 'UTC',
  }).format(date);
}
