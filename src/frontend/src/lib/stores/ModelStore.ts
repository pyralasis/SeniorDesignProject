import { BACKEND_API_BASE_URL } from "$lib/utilities/api.constants";
import { writable } from "svelte/store";
import type { AvailableModelsResponse, ModelStore, ModelStoreProps } from "./types/models-store.interface";
import type { MetaData } from "$lib/types/metadata";
import type { ArchitectureId } from "$lib/types/architecture";

const createModelStore = (): ModelStore =>{
    const { subscribe, set, update } = writable<ModelStoreProps>({
        availableModels: undefined,
        activeModel: undefined
    });
    const createModel = async (architecture_id: ArchitectureId, metadata: MetaData): Promise<void> => {
        await fetch(`${BACKEND_API_BASE_URL}/model/create`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                architecture_id: architecture_id,
                meta: metadata
            }),
        })
    };
    const getAvailableModels = async (): Promise<void> => {
        await fetch(`${BACKEND_API_BASE_URL}/model/available`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => response.json())
        .then(data => {
            let response = data as AvailableModelsResponse;
            update((store) => {
                store.availableModels = response.available;
                return store;
            });
        });
    };
    const loadModelById = (): void =>{};
    return{
        set, update, subscribe, createModel, getAvailableModels, loadModelById
    };
}

export const modelStore = createModelStore();