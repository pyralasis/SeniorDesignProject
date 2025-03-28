import type { ArchitectureId } from '$lib/types/architecture';
import type { Info } from '$lib/types/info';
import type { MetaData } from '$lib/types/metadata';
import { type Writable } from 'svelte/store';

export interface activeModel{}

export type ModelId = string;
export type ModelInfoDescription = Info & {}
export type ModelMetaDescription = MetaData & {}

export interface AvailableModel{
    id: ModelId;
    meta: ModelInfoDescription;
    info: ModelMetaDescription;
}

export interface ModelStoreProps{
    availableModels: AvailableModel[] | undefined | any;
    activeModel: activeModel | undefined;
}

export interface ModelStore extends Writable<ModelStoreProps> {
    createModel: (architecture_id: ArchitectureId, metadata: MetaData) => void;
    getAvailableModels: () => void;
    loadModelById: () => void;
    deleteModel: () => void;
    trainModel: (model_id: number,
                source_id: number,
                learning_rate: number,
                batch_size: number,
                epochs: number,) => void;
}

export type CreateModelRequestBody = {
    architecture_id: number,
    meta: MetaData
}

export type AvailableModelsResponse = {
    available: AvailableModel[],
    sucess: boolean
}