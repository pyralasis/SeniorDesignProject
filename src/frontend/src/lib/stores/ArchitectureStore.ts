import {
  type ArchitectureStore,
  type ArchitectureStoreProps,
} from "./types/architecture-store.interface";
import { BACKEND_API_BASE_URL } from "$lib/utilities/api.constants";
import { BackendApi } from "$lib/utilities/api.utilities";
import { get, writable, type Writable } from "svelte/store";
import type {
  NetworkArchitectureDescription,
  ArchitectureId,
  ArchitectureDataDescription,
  ArchitectureMetaDescription,
  ArchitectureInfoDescription,
  InputLayerDescription,
  NetworkLayerDescription,
} from "$lib/types/architecture";
import type { NetworkLayoutDescription } from "$lib/types/layout";
import type { Node, Edge } from "@xyflow/svelte";
import type { Parameter, ParameterValue } from "$lib/types/parameter";
import {
  SaveStatusEnum,
  type AvailableArchitecture,
  type AvailableArchitecturesResponse,
  type LoadArchitectureResponse,
} from "./types/architecture-store.interface";
import type { Version } from "$lib/types/info";
import type { LayerInput, LayerInstanceId, TensorSize } from "$lib/types/layer";
import { HandleStatusEnum } from "$lib/components/Node/handle-status.enum";

function getLayerParametersByLayerId(layerId: string): Promise<any> {
  return BackendApi.getLayerById(layerId.toLowerCase()).then((layer) => {
    return layer.parameters;
  });
}

function findParameterById(parameters: any[], id: string): Parameter<any> {
  return parameters.find((parameter) => parameter.id === id);
}

function getLayerInputs(
  id: string,
  edges: Edge[]
): LayerInstanceId | LayerInstanceId[] {
  return edges
    .filter((edge) => edge.target === id)
    .map((edge) => parseInt(edge.source));
}

async function parseLayersIntoNodesAndEdges(
  layers: NetworkLayerDescription[],
  layout: any,
  inputs: InputLayerDescription[],
  output: number
): Promise<{ nodes: Node[]; edges: Edge[] }> {
  let nodes: Node[] = [];
  let edges: Edge[] = layout.edges.map((edge: any) => edge as Edge);

  await Promise.all(
    inputs.map(async (input: any) => {
      nodes.push({
        id: input.instance_id.toString(),
        type: "input",
        data: {
          color: writable<string>(
            layout.nodes[input.instance_id]?.metadata.color ?? "#FFFFFF"
          ),
          outputSize: writable<TensorSize>(
            input.size.map((value: number) => value.toString())
          ),
          rightConnected: writable<boolean>(
            layout.nodes[input.instance_id]?.metadata.rightConnected ?? false
          ),
          rightStatus: writable<string>(
            layout.nodes[input.instance_id]?.metadata.rightStatus ??
              HandleStatusEnum.default
          ),
        },
        position: {
          x: layout.nodes[input.instance_id]?.x ?? 0,
          y: layout.nodes[input.instance_id]?.y ?? 0,
        },
        dragHandle: ".node__header",
      } satisfies Node);
    })
  );

  await Promise.all(
    layers.map(async (layer) => {
      const layerParameters = await getLayerParametersByLayerId(layer.layer_id);
      nodes.push({
        id: layer.instance_id.toString(),
        type: "layer",
        data: {
          color: writable<string>(
            layout.nodes[layer.instance_id]?.metadata.color ?? "#FFFFFF"
          ),
          title: writable<string>(
            layout.nodes[layer.instance_id]?.metadata.title ?? "Untitled Layer"
          ),
          expanded: writable<boolean>(
            layout.nodes[layer.instance_id]?.metadata.expanded ?? false
          ),
          leftConnected: writable<boolean>(
            layout.nodes[layer.instance_id]?.metadata.leftConnected ?? false
          ),
          rightConnected: writable<boolean>(
            layout.nodes[layer.instance_id]?.metadata.rightConnected ?? false
          ),
          leftStatus: writable<string>(
            layout.nodes[layer.instance_id]?.metadata.leftStatus ??
              HandleStatusEnum.default
          ),
          rightStatus: writable<string>(
            layout.nodes[layer.instance_id]?.metadata.rightStatus ??
              HandleStatusEnum.default
          ),
          inputs: writable<LayerInput[]>(
            layout.nodes[layer.instance_id]?.metadata?.inputs ?? []
          ),
          outputSize: writable<TensorSize>(
            layout.nodes[layer.instance_id]?.metadata.outputSize ?? ["0"]
          ),
          layer_id: layer.layer_id,
          parameters: writable<
            { parameter: Parameter<any>; value: ParameterValue<any> }[]
          >(
            layer.param_values.map(([key, value]) => {
              let parameterTemplate = findParameterById(layerParameters, key);
              return {
                parameter: parameterTemplate,
                value: value as ParameterValue<any>,
              };
            })
          ),
        },
        position: {
          x: layout.nodes[layer.instance_id]?.x ?? 0,
          y: layout.nodes[layer.instance_id]?.y ?? 0,
        },
        dragHandle: ".node__header",
      } satisfies Node);
      if (output > 0) {
        nodes.push({
          id: "69",
          type: "output",
          data: {
            leftConnected: writable<boolean>(
              layout.nodes["69"]?.metadata.leftConnected ?? false
            ),
            leftStatus: writable<string>(
              layout.nodes["69"]?.metadata.leftStatus ??
                HandleStatusEnum.default
            ),
          },
          position: {
            x: layout.nodes["69"]?.x ?? 0,
            y: layout.nodes["69"]?.y ?? 0,
          },
          dragHandle: ".node__header",
        } satisfies Node);
      }
    })
  );

  return { nodes, edges };
}

const createArchitectureStore = (): ArchitectureStore => {
  const { subscribe, set, update } = writable<ArchitectureStoreProps>({
    availableArchitectures: undefined,
    activeArchitecture: undefined,
    isSaved: true,
    saveStatus: SaveStatusEnum.Success,
  });

  const updateSaveStatus = (saved: boolean, status: SaveStatusEnum): void => {
    update((state) => {
      if (state.isSaved === saved && state.saveStatus === status) return state;
      return {
        ...state,
        isSaved: saved,
        saveStatus: status,
      };
    });
  };

  const getAvailableArchitectures = async (): Promise<void> => {
    await fetch(`${BACKEND_API_BASE_URL}/architecture/available`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((response) => response.json())
      .then((data) => {
        let response = data as AvailableArchitecturesResponse;
        update((store) => {
          store.availableArchitectures = response.available.map((arch) => {
            return {
              id: arch.id as ArchitectureId,
              meta: {
                name: arch.meta.name,
                description: arch.meta.description,
                last_modified: arch.meta.last_modified,
                created_at: arch.meta.created_at,
              } as ArchitectureMetaDescription,
              info: {
                version: arch.info.version,
              } as ArchitectureInfoDescription,
            } as AvailableArchitecture;
          });
          return store;
        });
      });
  };

  const loadArchitectureById = async (id: ArchitectureId): Promise<void> => {
    try {
      update((store) => ({
        ...store,
        activeArchitecture: undefined,
        loading: true,
      }));
      updateSaveStatus(true, SaveStatusEnum.Success);
      const response = await fetch(
        `${BACKEND_API_BASE_URL}/architecture/load?${new URLSearchParams({ id }).toString()}`
      );
      const data = ((await response.json()) as LoadArchitectureResponse).object;
      const archData = data.content.data;
      const layoutData = data.content.layout;

      const { nodes, edges } = await parseLayersIntoNodesAndEdges(
        archData.layers,
        layoutData,
        archData.inputs,
        archData.output
      );
      update((store) => ({
        ...store,
        activeArchitecture: {
          id: data.id,
          meta: {
            name: data.content.meta.name,
            description: data.content.meta.description,
            created_at: data.content.meta.created_at,
            last_modified: data.content.meta.last_modified,
            version: data.info?.version ?? 0,
          },
          nodes: writable<Node[]>(nodes),
          edges: writable<Edge[]>(edges),
          loading: false,
        },
      }));
    } catch (error) {
      console.error("Error loading architecture:", error);
      update((store) => ({
        ...store,
        activeArchitecture: undefined,
        loading: false,
      }));
    }
  };

  const clearActiveArchitecture = (): void => {
    updateSaveStatus(false, SaveStatusEnum.NotSaved);
    update((store) => {
      store.activeArchitecture = undefined;

      return store;
    });
  };

  const deleteArchitecture = async (id: ArchitectureId): Promise<boolean> => {
    let status = await fetch(`${BACKEND_API_BASE_URL}/architecture/delete`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ id: id }),
    }).then((response) => {
      return response.status === 200;
    });
    getAvailableArchitectures();
    return status;
  };

  const saveActiveArchitecture = async (
    isNew: boolean = false
  ): Promise<{ id?: ArchitectureId; success: boolean }> => {
    const aStore = get(architectureStore);
    if (!aStore.activeArchitecture) {
      return { success: false };
    }

    const nodes = get(aStore.activeArchitecture.nodes);
    const edges = get(aStore.activeArchitecture.edges);
    const layerNodes = nodes.filter((node) => node.type === "layer");
    const inputNodes = nodes.filter((node) => node.type === "input");
    const outputNode = nodes.filter((node) => node.id === "69")[0];
    const architecture: NetworkArchitectureDescription = {
      id: (aStore.activeArchitecture.id as ArchitectureId) ?? "",
      content: {
        data: {
          inputs: inputNodes.map((node) => {
            let outputSize = get(node.data.outputSize as Writable<TensorSize>);
            return {
              instance_id: parseInt(node.id, 10),
              size: outputSize.map((value: number) => value) as TensorSize,
            } as InputLayerDescription;
          }),
          layers: layerNodes.map((node) => {
            const parameters = get(
              node.data.parameters as Writable<
                { parameter: Parameter<any>; value: ParameterValue<any> }[]
              >
            );
            return {
              instance_id: parseInt(node.id, 10),
              layer_id: node.data.layer_id,
              input: getLayerInputs(node.id, edges),
              param_values: parameters.map(({ parameter, value }) => [
                parameter.id,
                value,
              ]),
            };
          }),
          output: outputNode
            ? (parseInt(
                edges.filter((edge) => edge.target === outputNode.id)[0]
                  ?.source ?? 0
              ) as LayerInstanceId)
            : -1,
        } as ArchitectureDataDescription,
        layout: {
          nodes: Object.fromEntries(
            nodes.map((node) => {
              return [
                node.id,
                {
                  x: node.position.x,
                  y: node.position.y,
                  metadata: {
                    color: get(node.data?.color as Writable<string>),
                    title: get(node.data?.title as Writable<string>),
                    expanded: get(node.data?.expanded as Writable<boolean>),
                    leftConnected: get(
                      node.data?.leftConnected as Writable<boolean>
                    ),
                    rightConnected: get(
                      node.data?.rightConnected as Writable<boolean>
                    ),
                    leftStatus: get(node.data?.leftStatus as Writable<string>),
                    rightStatus: get(
                      node.data?.rightStatus as Writable<string>
                    ),
                    inputs: get(node.data?.inputs as Writable<LayerInput[]>),
                    outputSize: get(
                      node.data?.outputSize as Writable<TensorSize>
                    ),
                  },
                },
              ];
            })
          ),
          edges,
        } as NetworkLayoutDescription,
        meta: {
          name: aStore.activeArchitecture.meta.name,
          description: aStore.activeArchitecture.meta.description,
          created_at: aStore.activeArchitecture.meta.created_at,
          last_modified: new Date().toISOString(),
        } as ArchitectureMetaDescription,
      },
      info: {
        version: aStore.activeArchitecture?.meta.version ?? (0 as Version),
      } as ArchitectureInfoDescription,
    };

    try {
      const response = await fetch(
        `${BACKEND_API_BASE_URL}/architecture/${isNew ? "create" : "update"}`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(
            isNew
              ? {
                  meta: architecture.content.meta,
                  data: architecture.content.data,
                  layout: architecture.content.layout,
                }
              : {
                  id: aStore.activeArchitecture.id,
                  object: architecture.content,
                }
          ),
        }
      );

      if (!response.ok) throw new Error(`Server Error: ${response.status}`);

      if (isNew) {
        let id: ArchitectureId = (await response.json()).id as ArchitectureId;
        getAvailableArchitectures();
        return { id: id, success: true };
      }
      return { success: true };
    } catch (error) {
      console.error("Save failed:", error);
      return { success: false };
    }
  };

  const createNewArchitecture = async (
    name: string,
    description?: string
  ): Promise<{ id?: ArchitectureId; success: boolean }> => {
    updateSaveStatus(true, SaveStatusEnum.Success);
    update((store) => {
      store.activeArchitecture = {
        meta: {
          name: name,
          description: description,
          created_at: new Date().toISOString(),
          last_modified: new Date().toISOString(),
          version: 0,
        },
        nodes: writable<Node[]>([]),
        edges: writable<Edge[]>([]),
        loading: false,
      };
      return store;
    });
    return await saveActiveArchitecture(true);
  };

  const addNodeToActiveArchitecture = (node: Node): void => {
    update((store) => {
      if (!store.activeArchitecture) {
        return store;
      }
      store.activeArchitecture.nodes.update((nodes) => {
        nodes.push(node);
        return nodes;
      });

      return store;
    });
    updateArchitectureSaveStatus();
  };
  //Changing it so there has to be a node selected
  const deleteNodeFromActiveArchitecture = (id: string | null): void => {
    update((store) => {
      if (!store.activeArchitecture || !store.activeArchitecture.nodes) {
        return store;
      }

      let currentNodes = get(store.activeArchitecture.nodes);

      if (!id) {
        return store;
      }

      if (!currentNodes.some((node) => node.id === id)) {
        return store;
      }

      store.activeArchitecture.nodes.update((nodes) => {
        return nodes.filter((node) => node.id !== id);
      });
      updateArchitectureSaveStatus();
      return store;
    });
  };
  ///Checks saveActiveArchitecture and updates the UI
  //Also is used as an autosave since we call it on node insertion/deletion
  const updateArchitectureSaveStatus = async (): Promise<void> => {
    try {
      // Update UI state first
      updateSaveStatus(false, SaveStatusEnum.Saving);

      const success = await saveActiveArchitecture();

      if (success) {
        setTimeout(() => {
          updateSaveStatus(true, SaveStatusEnum.Success);
        }, 500);
      } else {
        updateSaveStatus(false, SaveStatusEnum.Failed);
      }
    } catch (error) {
      console.error("Save error:", error);
      updateSaveStatus(false, SaveStatusEnum.Failed);
    }
  };

  return {
    set,
    update,
    subscribe,
    getAvailableArchitectures,
    loadArchitectureById,
    clearActiveArchitecture,
    deleteArchitecture,
    saveActiveArchitecture,
    createNewArchitecture,
    addNodeToActiveArchitecture,
    deleteNodeFromActiveArchitecture,
    updateArchitectureSaveStatus,
    updateSaveStatus,
  };
};

export const architectureStore = createArchitectureStore();
