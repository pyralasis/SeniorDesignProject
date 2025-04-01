import type { EnumOf } from "$lib/utilities/enum-of";

export const NodeTypeEnum = {
    Layer: 'layer',
    Transform: 'transform',
    Source: 'source',
    Input: 'input',
    Output: 'output',
    ValuesOutput: 'valuesOutput',
    LabelsOutput: 'labelsOutput',
} as const;

export type NodeType = EnumOf<typeof NodeTypeEnum>;