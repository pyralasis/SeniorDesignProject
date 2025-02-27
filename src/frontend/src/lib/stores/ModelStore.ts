import { writable } from "svelte/store";
import type { ModelStore, ModelStoreProps } from "./types/models-store.interface";

const createModelStore = (): ModelStore =>{
    const { subscribe, set, update } = writable<ModelStoreProps>({
        availableModels: undefined,
        activeModel: undefined
    });
    const getAvailableModels = (): void =>{}
    const loadModelById = (): void =>{}
    return{
        set, update, subscribe, getAvailableModels, loadModelById
    };
}