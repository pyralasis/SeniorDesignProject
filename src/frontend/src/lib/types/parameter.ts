import type { EnumOf } from "$lib/utilities";

export const ParameterTypeEnum = {
    Bool: 'bool',
    Float: 'float',
    Int: 'int',
    Size2D: 'size2d',
    String: 'str',
} as const;

export type ParameterType = EnumOf<typeof ParameterTypeEnum>;
export type ParameterId = string;
export type ParameterName = string;

export type OneOf<T> = {
    type: 'oneOf',
    values: T[],
}

export type WithRange = {
    type: 'range',
    min: number | undefined,
    max: number | undefined,
}

export type AnyConstraint<T> = OneOf<T> | WithRange;

export type Parameter<T> = {
    id: ParameterId,
    name: ParameterName,
    constraint: AnyConstraint<T> | undefined,
    default: ParameterValue<any> | undefined,
    type: ParameterType,
}

export type ParameterValue<T> = {
    val: T,
    type: ParameterType
}