import { type EnumOf } from '$lib/utilities'

export const HeaderColorEnum = {
    default: 'default',
    secondary: 'secondary',
} as const;

export type HeaderColor = EnumOf<typeof HeaderColorEnum>;