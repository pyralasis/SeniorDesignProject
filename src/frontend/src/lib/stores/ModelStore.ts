import { BACKEND_API_BASE_URL } from "$lib/utilities/api.constants";
import { writable } from "svelte/store";
import type { AvailableModel, AvailableModelsResponse, ModelId, ModelInfoDescription, ModelMetaDescription, ModelStore, ModelStoreProps } from "./types/models-store.interface";
import type { MetaData } from "$lib/types/metadata";
import type { ArchitectureId } from "$lib/types/architecture";

const createModelStore = (): ModelStore => {
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
                console.log(data);
                update((store) => {
                    store.availableModels = response.available.map((model) => {
                        return {
                            id: model.id as ModelId,
                            meta: {
                                name: model.meta.name,
                                description: model.meta.description,
                                last_modified: model.meta.last_modified,
                                created_at: model.meta.created_at,
                            } as ModelMetaDescription,
                            info: {
                                version: model.info.version,
                            } as ModelInfoDescription,
                        } as unknown as AvailableModel;
                    });
                    return store;
                });
            });
    };
    const loadModelById = (): void => { };
    const deleteModel = (): void => { };

    const trainModel =
        async (model_id: number,
            source_id: number,
            learning_rate: number,
            batch_size: number,
            shuffle_data: boolean,
            epochs: number): Promise<void> => {
            await fetch(`${BACKEND_API_BASE_URL}/model/train`, {
                method: 'post',
                headers: {
                    'Content-Type': 'application/json',

                },
                body: JSON.stringify({
                    "config":
                    {
                        "model_id": model_id,
                        "source_id": source_id,
                        "learning_rate": learning_rate,
                        "batch_size": batch_size,
                        "shuffle_data": shuffle_data,
                        "epochs": epochs,
                    }
                }
                ),
            })
        };
    return {
        set, update, subscribe, createModel, getAvailableModels, loadModelById, deleteModel, trainModel
    };
}

export const modelStore = createModelStore();