import type { ArchitectureId } from '$lib/types/architecture';
import type { MetaData } from '$lib/types/metadata';
import { type Writable } from 'svelte/store';

export interface activeModel{}


export interface AvailableModel{

}

export interface ModelStoreProps{
    availableModels: AvailableModel[] | undefined;
    activeModel: activeModel | undefined;
}

export interface ModelStore extends Writable<ModelStoreProps> {
    createModel: (architecture_id: ArchitectureId, metadata: MetaData) => void;
    getAvailableModels: () => void;
    loadModelById: () => void;
}

export type CreateModelRequestBody = {
    architecture_id: number,
    meta: MetaData
}

export type AvailableModelsResponse = {
    available: AvalableModel[],
    sucess: boolean
}