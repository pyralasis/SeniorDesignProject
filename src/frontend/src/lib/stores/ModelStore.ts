import { BACKEND_API_BASE_URL } from "$lib/utilities/api.constants";
import { writable } from "svelte/store";
import type { ModelStore, ModelStoreProps } from "./types/models-store.interface";

const createModelStore = (): ModelStore =>{
    const { subscribe, set, update } = writable<ModelStoreProps>({
        availableModels: undefined,
        activeModel: undefined
    });
    const createModel = async (): Promise<void> => {
        
    } 
    const getAvailableModels = async (): Promise<void> => {
        // await new Promise(resolve => setTimeout(resolve, 2000));
        //         await fetch(`${BACKEND_API_BASE_URL}/model/available`, {
        //             method: 'GET',
        //             headers: {
        //                 'Content-Type': 'application/json',
        //             }
        //         })
        //             .then(response => response.json())
        //             .then(data => {
        //             }
        //             )
    }
    const loadModelById = (): void =>{}
    return{
        set, update, subscribe, createModel, getAvailableModels, loadModelById
    };
}

export const modelStore = createModelStore();