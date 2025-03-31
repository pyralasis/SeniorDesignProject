import type { ArchitectureId } from '$lib/types/architecture';
import type { Info } from '$lib/types/info';
import type { MetaData } from '$lib/types/metadata';
import type { Parameter, ParameterValue } from '$lib/types/parameter';
import { type Writable } from 'svelte/store';

export interface activeModel { }

export type ModelId = string;
export type ModelInfoDescription = Info & {}
export type ModelMetaDescription = MetaData & {}

export interface AvailableModel {
    id: ModelId;
    meta: ModelMetaDescription;
    info: ModelInfoDescription;
}

export interface AvailableLoss {
    id: string;
    name: string;
    parameters: Parameter<any>[];
}

export interface AvailableOptimizer {
    id: string;
    name: string;
    parameters: Parameter<any>[];
}

export interface ModelStoreProps {
    availableModels: AvailableModel[] | undefined | any;
    activeModel: activeModel | undefined;
    availableLosses: AvailableLoss[] | undefined | any;
    availableOptimizers: AvailableOptimizer[] | undefined | any;
}

export interface ModelStore extends Writable<ModelStoreProps> {
    createModel: (architecture_id: ArchitectureId, metadata: MetaData) => void;
    getAvailableModels: () => void;
    loadModelById: () => void;
    deleteModel: () => void;
    trainModel: (model_id: number,
        source_id: number,
        learning_rate: number,
        loss: LossConfig,
        optimizer: OptimizerConfig,
        batch_size: number,
        shuffle_data: boolean,
        epochs: number) => void;
    getAvailableOptimizers: () => void;
    getAvailableLosses: () => void;
}

export type CreateModelRequestBody = {
    architecture_id: number,
    meta: MetaData
}

export type AvailableModelsResponse = {
    available: AvailableModel[],
    sucess: boolean
}


export type LossConfig = {
    id: number
    param_values: Parameter<any>[]
}

export type OptimizerConfig = {
    id: number,
    param_values: Parameter<any>[]
}
    
export type OptimizerParams = {[id: string]: ParameterValue<any>}