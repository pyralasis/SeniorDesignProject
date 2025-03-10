import type { EnumOf } from '$lib/utilities/enum-of';

export const HandleStatusEnum = {
    default: 'default',
    success: 'success',
    error: 'error',
} as const;

export type HandleStatus = EnumOf<typeof HandleStatusEnum>;