import type { Parameter } from './parameter';

export type LayerInstanceId = number;
export type LayerId = string;
export type LayerName = string;

export type LayerInput = {
    max_dimensions: number | null,
    min_dimensions: number | null,
    name: string | null,
}

export type LayerBlueprint<T> = {
    id: LayerId,
    name: LayerName,
    inputs: LayerInput[],
    parameters: Parameter<T>[],
}


export type TensorSize = number[];