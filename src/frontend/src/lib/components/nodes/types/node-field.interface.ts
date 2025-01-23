import { type EnumOf } from "$lib/utilities/enum-of";

export interface NodeField {
    label: string,
    value?: string,
    type: NodeFieldType,
    required: boolean,
}

export const NodeFieldTypeEnum = {
    input: "input",
    series: "series",
    boolean: "boolean",
} as const;

export type NodeFieldType = EnumOf<typeof NodeFieldTypeEnum>;