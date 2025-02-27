import { type Writable } from 'svelte/store';

export interface availableModel{}
export interface activeModel{}

export interface ModelStoreProps{
    availableModels: availableModel[] | undefined;
    activeModel: activeModel | undefined;
}

export interface ModelStore extends Writable<ModelStoreProps> {
    getAvailableModels: () => void;
    loadModelById: () => void;
}