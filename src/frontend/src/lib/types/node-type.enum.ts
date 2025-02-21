import type { EnumOf } from "$lib/utilities/enum-of";

export const NodeTypeEnum = {
    Layer: 'layer',
    Transform: 'transform',
    Source: 'source',
} as const;

export type NodeType = EnumOf<typeof NodeTypeEnum>;