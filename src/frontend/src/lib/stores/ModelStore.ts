import { BACKEND_API_BASE_URL } from "$lib/utilities/api.constants";
import { writable } from "svelte/store";
import type {
  AvailableModel,
  AvailableModelsResponse,
  LossConfig,
  ModelId,
  ModelInfoDescription,
  ModelMetaDescription,
  ModelStore,
  ModelStoreProps,
  OptimizerConfig,
  OptimizerParams,
  TrainingConfig,
} from "./types/models-store.interface";
import type { MetaData } from "$lib/types/metadata";
import type { ArchitectureId } from "$lib/types/architecture";
import type { Parameter } from "$lib/types/parameter";

const createModelStore = (): ModelStore => {
  const { subscribe, set, update } = writable<ModelStoreProps>({
    availableModels: undefined,
    activeModel: undefined,
    availableOptimizers: undefined,
    availableLosses: undefined,
  });
  const createModel = async (
    architecture_id: ArchitectureId,
    metadata: MetaData
  ): Promise<boolean> => {
    const modifiedMetadata = {
      ...metadata,
      name: metadata.name,
    };
    return await fetch(`${BACKEND_API_BASE_URL}/model/create`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        architecture_id: architecture_id,
        meta: modifiedMetadata,
      }),
    }).then((response) => {
      response.json();
      return response.status === 200;
    });
  };
  const getAvailableModels = async (): Promise<void> => {
    await fetch(`${BACKEND_API_BASE_URL}/model/available`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((response) => response.json())
      .then((data) => {
        let response = data as AvailableModelsResponse;
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
  const loadModelById = (): void => {};

  const deleteModel = async (id: ModelId): Promise<void> => {
    await fetch(`${BACKEND_API_BASE_URL}/model/delete`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ id: id }),
    });
    getAvailableModels();
  };

  const trainModel = async (cfg: TrainingConfig): Promise<void> => {
    await fetch(`${BACKEND_API_BASE_URL}/model/train/start`, {
      method: "post",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        meta: {},
        config: cfg,
      }),
    });
  };

  const getAvailableOptimizers = async (): Promise<void> => {
    await fetch(`${BACKEND_API_BASE_URL}/model/optimizer/available`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((response) => response.json())
      .then((data) => {
        let response = data;
        update((store) => {
          store.availableOptimizers = response;
          return store;
        });
      });
  };

  const getAvailableLosses = async (): Promise<void> => {
    await fetch(`${BACKEND_API_BASE_URL}/model/loss/available`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((response) => response.json())
      .then((data) => {
        let response = data;
        update((store) => {
          store.availableLosses = response;
          return store;
        });
      });
  };

  const getModelNameById = async (id: ModelId): Promise<string> => {
    return await fetch(`${BACKEND_API_BASE_URL}/model/meta/load?id=${id}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((response) => response.json())
      .then((data) => {
        return data.data.name;
      });
  };
  return {
    set,
    update,
    subscribe,
    createModel,
    getAvailableModels,
    loadModelById,
    deleteModel,
    trainModel,
    getAvailableLosses,
    getAvailableOptimizers,
    getModelNameById,
  };
};

export const modelStore = createModelStore();
