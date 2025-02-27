import type { MetaData } from '$lib/types/metadata';
import { type Writable } from 'svelte/store';

export interface availableModel{}
export interface activeModel{}


export interface AvalableModel{

}

export interface ModelStoreProps{
    availableModels: availableModel[] | undefined;
    activeModel: activeModel | undefined;
}

export interface ModelStore extends Writable<ModelStoreProps> {
    createModel: () => void;
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