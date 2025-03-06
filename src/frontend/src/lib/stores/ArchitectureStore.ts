import { type ArchitectureStore, type ArchitectureStoreProps } from "./types/architecture-store.interface";
import { BACKEND_API_BASE_URL } from "$lib/utilities/api.constants";
import { BackendApi } from "$lib/utilities/api.utilities";
import { get, writable, type Writable } from "svelte/store";
import type {
    NetworkArchitectureDescription,
    ArchitectureId,
    ArchitectureDataDescription,
    ArchitectureMetaDescription,
    ArchitectureInfoDescription,
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

function getLayerParametersByLayerId(layerId: string): Promise<any> {
    return BackendApi.getLayerById(layerId.toLowerCase()).then((layer) => {
        return layer.parameters;
    });
}

function findParameterById(parameters: any[], id: string): Parameter<any> {
    return parameters.find((parameter) => parameter.id === id);
}

async function parseLayersIntoNodesAndEdges(layers: any[], layout: any): Promise<{ nodes: Node[]; edges: Edge[] }> {
    let nodes: Node[] = [];
    let edges: Edge[] = layout.edges.map((edge: any) => edge as Edge);

    await Promise.all(
        layers.map(async (layer: any) => {
            const layerParameters = await getLayerParametersByLayerId(layer.layer_id);
            nodes.push({
                id: layer.instance_id.toString(),
                type: "layer",
                data: {
                    color: writable<string>(layout.nodes[layer.instance_id]?.metadata.color ?? "#FFFFFF"),
                    title: writable<string>(layout.nodes[layer.instance_id]?.metadata.title ?? "Untitled Layer"),
                    layer_id: writable<string>(layer.layer_id),
                    parameters: writable<{ parameter: Parameter<any>; value: ParameterValue<any> }[]>(
                        Object.entries(layer.param_values).map(([key, value]) => {
                            let parameterTemplate = findParameterById(layerParameters, key);
                            return {
                                parameter: parameterTemplate,
                                value: value as ParameterValue<any>,
                            };
                        })
                    ),
                    expanded: writable<boolean>(false),
                },
                position: { x: layout.nodes[layer.instance_id]?.x ?? 0, y: layout.nodes[layer.instance_id]?.y ?? 0 },
                dragHandle: ".node__header",
            } satisfies Node);
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
            update((store) => ({ ...store, activeArchitecture: undefined, loading: true }));
            updateSaveStatus(true, SaveStatusEnum.Success);
            const response = await fetch(`${BACKEND_API_BASE_URL}/architecture/load?${new URLSearchParams({ id }).toString()}`);
            const data = ((await response.json()) as LoadArchitectureResponse).object;
            const archData = data.data.data;
            const layoutData = data.data.layout;

            const { nodes, edges } = await parseLayersIntoNodesAndEdges(archData.layers, layoutData);
            update((store) => ({
                ...store,
                activeArchitecture: {
                    id: data.id,
                    meta: {
                        name: data.data.meta.name,
                        description: data.data.meta.description,
                        created_at: data.data.meta.created_at,
                        last_modified: data.data.meta.last_modified,
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
        console.log("In clear Function");
        update((store) => {
            store.activeArchitecture = undefined;

            return store;
        });
    };

    const deleteArchitecture = async (id: ArchitectureId): Promise<void> => {
        await fetch(`${BACKEND_API_BASE_URL}/architecture/delete`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ id: id }),
        });
        getAvailableArchitectures();
    };

    const saveActiveArchitecture = async (isNew: boolean = false): Promise<boolean> => {
        const aStore = get(architectureStore);
        if (!aStore.activeArchitecture) {
            return false;
        }

        const nodes = get(aStore.activeArchitecture.nodes);
        const edges = get(aStore.activeArchitecture.edges);

        const architecture: NetworkArchitectureDescription = {
            id: (aStore.activeArchitecture.id as ArchitectureId) ?? "",
            data: {
                data: {
                    inputs: [], // TODO
                    layers: nodes.map((node) => {
                        const parameters = get(
                            node.data.parameters as Writable<{ parameter: Parameter<any>; value: ParameterValue<any> }[]>
                        );
                        return {
                            instance_id: parseInt(node.id, 10),
                            layer_id: get(node.data.layer_id as Writable<string>),
                            input: [],
                            param_values: Object.fromEntries(parameters.map(({ parameter, value }) => [parameter.id, value])),
                        };
                    }),
                    output: 0, // TODO
                } as ArchitectureDataDescription,
                layout: {
                    nodes: Object.fromEntries(
                        nodes.map((node) => [
                            node.id,
                            {
                                x: node.position.x,
                                y: node.position.y,
                                metadata: {
                                    color: get(node.data.color as Writable<string>),
                                    title: get(node.data.title as Writable<string>),
                                },
                            },
                        ])
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
            const response = await fetch(`${BACKEND_API_BASE_URL}/architecture/${isNew ? "create" : "update"}`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(
                    isNew
                        ? { meta: architecture.data.meta, data: architecture.data.data, layout: architecture.data.layout }
                        : { id: aStore.activeArchitecture.id, object: architecture.data }
                ),
            });

            if (!response.ok) throw new Error(`Server Error: ${response.status}`);

            const data: { id: string } = await response.json();

            if (isNew) {
                getAvailableArchitectures();
            }
            return true;
        } catch (error) {
            console.error("Save failed:", error);
            return false;
        }
    };

    const createNewArchitecture = async (name: string, description?: string): Promise<void> => {
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
        saveActiveArchitecture(true);
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
        console.log("autosave happening...");
        updateArchitectureSaveStatus();
    };
    //Changing it so there has to be a node selected
    const deleteNodeFromActiveArchitecture = (id: string | null): void => {
        update((store) => {
            if (!store.activeArchitecture || !store.activeArchitecture.nodes) {
                console.log("No active architecture or nodes - Deletion blocked");
                return store;
            }

            let currentNodes = get(store.activeArchitecture.nodes);

            if (!id) {
                console.log("No node selected for deletion");
                return store;
            }

            if (!currentNodes.some((node) => node.id === id)) {
                console.log(`Node with id ${id} does not exist - No changes made`);
                return store;
            }

            console.log("Node found, deleting...");

            store.activeArchitecture.nodes.update((nodes) => {
                return nodes.filter((node) => node.id !== id);
            });
            return store;
        });
        updateArchitectureSaveStatus();
    };
    ///Checks saveActiveArchitecture and updates the UI
    //Also is used as an autosave since we call it on node insertion/deletion
    const updateArchitectureSaveStatus = async (): Promise<void> => {
        try {
            console.log("updateArchitectureSaveStatus called");

            // Update UI state first
            updateSaveStatus(false, SaveStatusEnum.Saving);
            console.log("Status set to Saving...");

            const success = await saveActiveArchitecture();

            if (success) {
                setTimeout(() => {
                    console.log("Save successful - updating UI state");
                    updateSaveStatus(true, SaveStatusEnum.Success);
                }, 500);
            } else {
                console.log("Save failed - updating UI state");
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
