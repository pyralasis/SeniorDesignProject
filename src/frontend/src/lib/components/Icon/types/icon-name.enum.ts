import { type EnumOf } from '$lib/utilities/enum-of';

export const IconNameEnum = {
    chevron_right: 'chevron_right',
    plus: 'plus',
    collapse: 'collapse',
    sideways_hamburger: 'sideways_hamburger',
    trash: 'trash',
} as const;

export type IconName = EnumOf<typeof IconNameEnum>;
