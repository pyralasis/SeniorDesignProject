import { BACKEND_API_BASE_URL } from "$lib/utilities/api.constants";
import { writable } from "svelte/store";
import type { AvailableModel, AvailableModelsResponse, ModelId, ModelInfoDescription, ModelMetaDescription, ModelStore, ModelStoreProps } from "./types/models-store.interface";
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
        await fetch(`${BACKEND_API_BASE_URL}/model/meta/available`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => response.json())
        .then(data => {
            let response = data as AvailableModelsResponse;
            update((store) => {
                store.availableModels = response.available.map((model) => {
                    return {
                        // id: model.id as ModelId,
                        id: model as unknown as ModelId,
                        // meta: {
                        //     name: model.meta.name,
                        //     description: model.meta.description,
                        //     last_modified: model.meta.last_modified,
                        //     created_at: model.meta.created_at,
                        // } as ModelMetaDescription,
                        meta: {
                            name: "a",
                            description: "a",
                            last_modified: "a",
                            created_at: "a",
                        } as ModelMetaDescription,
                        // info: {
                        //     version: arch.info.version,
                        // } as ModelInfoDescription,
                        info: {
                            version: 1,
                        } as ModelInfoDescription,
                    } as unknown as AvailableModel;
                });
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