import { type EnumOf } from '$lib/utilities'

export const HeaderTypeEnum = {
    h1: 'h1',
    h2: 'h2',
    h3: 'h3',
    h4: 'h4',
    subheader: 'subheader',
} as const;

export type HeaderType = EnumOf<typeof HeaderTypeEnum>;