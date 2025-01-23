import { type EnumOf } from '$lib/utilities/enum-of';

export const ParameterTypeEnum = {
    Bool: 'bool',
    Float: 'float',
    Int: 'int',
    Size2D: 'size2d',
    String: 'string',
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
    value: T,
    type: ParameterType
}

export type InputDefinition = {
    name: string | undefined,
    maxDimensions: number,
    minDimensions: number | undefined,
}

export type LayerId = string;
export type LayerName = string;

export type Layer<T> = {
    id: LayerId,
    name: LayerName,
    inputs: InputDefinition[],
    parameters: Parameter<T>[],
}