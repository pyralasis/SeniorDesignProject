import type { EnumOf } from '$lib/utilities'

export const FlyoutSideEnum = {
    left: 'left',
    right: 'right',
    top: 'top',
    bottom: 'bottom',
} as const;

export type FlyoutSide = EnumOf<typeof FlyoutSideEnum>;

