import type { EnumOf } from "$lib/utilities";
import type { Parameter, ParameterValue } from "./parameter";
import type { InstanceId } from "./pipeline";

export type TransformId = string;
export type Transform = "transform";

export const TransformTypeEnum = {
    value: 'value_transform',
    datasource: 'datasource_transform',
} as const;

export type TransformType = EnumOf<typeof TransformTypeEnum>;

export type TransformBlueprint<T> = {
    id: TransformId;
    name: string;
    parameters: Parameter<T>[];
    type: TransformType;
}

export type TransformConfig = {
    type: Transform;
    instance_id: InstanceId;
    transform_id: TransformId;
    input: InstanceId;
    param_values: [string, ParameterValue<any>][];
}