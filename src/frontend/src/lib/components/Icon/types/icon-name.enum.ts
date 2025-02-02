import { type EnumOf } from '$lib/utilities/enum-of';

export const IconNameEnum = {
    chevron_right: 'chevron_right',
} as const;

export type IconName = EnumOf<typeof IconNameEnum>;
