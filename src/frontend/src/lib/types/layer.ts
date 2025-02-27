import { type EnumOf } from '$lib/utilities/enum-of';
import type { Parameter } from './parameter';

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

export type LayerInstanceId = number;
export type TensorSize = number[];