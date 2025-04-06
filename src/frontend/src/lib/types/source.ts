import type { Parameter, ParameterValue } from "./parameter";
import type { InstanceId } from "./pipeline";

export type SourceId = string;
export type Source = 'source';

export type SourceBlueprint<T> = {
    id: SourceId;
    name: string;
    parameters: Parameter<T>[];
}

export type SourceConfig = {
    type: Source;
    instance_id: InstanceId;
    src_id: SourceId;
    param_values: [string, ParameterValue<any>][];
}