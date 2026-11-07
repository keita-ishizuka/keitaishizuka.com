import { defineCollection } from 'astro:content';

// The blog was removed on 2026-11-02; sources are kept in
// archive/blog-removed-20261102/ if it is ever brought back.
export const collections = {} as Record<string, ReturnType<typeof defineCollection>>;
