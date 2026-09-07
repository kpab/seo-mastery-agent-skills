import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

/**
 * リリースのお知らせ。1 バージョン × 1 言語で 1 ファイル。
 * ファイル名は `<lang>/v1-5-0.md` で、id がそのまま `en/v1-5-0` になる。
 * 言語と URL セグメントは id から導く。
 *
 * frontmatter に `slug` を置いてはいけない。glob loader はその値で id を上書きするため、
 * en と ja が同じ id に潰れて片方が消える。URL のセグメントにドットを入れないよう、
 * ファイル名は `1.6.0` ではなく `v1-6-0` にする。
 */
const releases = defineCollection({
  loader: glob({ base: './src/content/releases', pattern: '**/*.md' }),
  schema: z.object({
    // 表示・JSON-LD 用の版番号。CHANGELOG と SKILL.md に一致させる
    version: z.string(),
    title: z.string(),
    summary: z.string(),
    date: z.coerce.date(),
    // 記述を後から直したときだけ入れる。無ければ date を dateModified に使う
    updated: z.coerce.date().optional(),
  }),
});

export const collections = { releases };
