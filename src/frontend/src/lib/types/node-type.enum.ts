import type { EnumOf } from "$lib/utilities/enum-of";

export const NodeTypeEnum = {
    Layer: 'layer',
} as const;

export type NodeType = EnumOf<typeof NodeTypeEnum>;