import { type ArchitectureStore, type ArchitectureStoreProps } from "./types/architecture-store.interface";
import { BACKEND_API_BASE_URL } from "$lib/utilities/api.constants";
import { BackendApi } from "$lib/utilities/api.utilities";
import { get, writable, type Writable } from "svelte/store";
import type { NetworkArchitectureDescription, ArchitectureId, NetworkLayoutDescription, ArchitectureDataDescription, ArchitectureMetaDescription, ArchitectureInfoDescription, ArchitectureVersion } from "$lib/types/architecture";
import type { Node, Edge } from "@xyflow/svelte";
import type { Parameter, ParameterValue } from "$lib/types/layer";
import type { AvailableArchitecturesResponse, LoadArchitectureResponse, } from "./types/architecture-store.interface";

function getLayerParametersByLayerId(layerId: string): Promise<any> {
    return BackendApi.getLayerById(layerId.toLowerCase()).then((layer) => {
        return layer.parameters;
    });
}

function findParameterById(parameters: any[], id: string): Parameter<any> {
    return parameters.find((parameter) => parameter.id === id);
}

async function parseLayersIntoNodesAndEdges(layers: any[], layout: any): Promise<{ nodes: Node[], edges: Edge[] }> {
    let nodes: Node[] = [];
    let edges: Edge[] = layout.edges.map((edge: any) => edge as Edge);

    await Promise.all(layers.map(async (layer: any) => {
        const layerParameters = await getLayerParametersByLayerId(layer.layer_id);
        nodes.push({
            id: layer.instance_id.toString(),
            type: 'layer',
            data: {
                color: writable<string>(layout.nodes[layer.instance_id]?.metadata.color ?? '#FFFFFF'),
                title: writable<string>(layout.nodes[layer.instance_id]?.metadata.title ?? 'Untitled Layer'),
                layer_id: writable<string>(layer.layer_id),
                parameters: writable<{ parameter: Parameter<any>; value: ParameterValue<any> }[]>(


                    Object.entries(layer.param_values).map(([key, value]) => {
                        let parameterTemplate = findParameterById(layerParameters, key);
                        return ({
                            parameter: parameterTemplate,
                            value: value as ParameterValue<any>
                        });
                    })
                ),
                expanded: writable<boolean>(false),
            },
            position: { x: layout.nodes[layer.instance_id]?.x ?? 0, y: layout.nodes[layer.instance_id]?.y ?? 0 },
            dragHandle: '.node__header',
        } satisfies Node);

    }));


    return { nodes, edges };
}

const createArchitectureStore = (): ArchitectureStore => {
    const { subscribe, set, update } = writable<ArchitectureStoreProps>({
        availableArchitectures: undefined,
        activeArchitecture: undefined
    });

    const getAvailableArchitectures = async (): Promise<void> => {
        await new Promise(resolve => setTimeout(resolve, 2000));
        await fetch(`${BACKEND_API_BASE_URL}/architecture/available`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        })
            .then(response => response.json())
            .then(data => {
                let response = data as AvailableArchitecturesResponse;
                update((store) => {
                    store.availableArchitectures = response.available.map((arch) => {
                        return {
                            id: arch.id,
                            meta: {
                                name: arch.meta.name,
                                description: arch.meta.description,
                            },
                            info: {
                                version: arch.info.version,
                            }
                        };
                    });
                    return store;

                });
            });
    }

    const loadArchitectureById = async (id: ArchitectureId): Promise<void> => {
        try {
            update(store => ({ ...store, activeArchitecture: undefined, loading: true }));

            const response = await fetch(`${BACKEND_API_BASE_URL}/architecture/load?${new URLSearchParams({ id }).toString()}`);
            const data = (await response.json() as LoadArchitectureResponse).object;
            const archData = data.data.data;
            const layoutData = data.data.layout;

            const { nodes, edges } = await parseLayersIntoNodesAndEdges(
                archData.layers,
                layoutData
            );
            update(store => ({
                ...store,
                activeArchitecture: {
                    id: data.id,
                    meta: {
                        name: data.data.meta.name,
                        description: data.data.meta.description,
                    },
                    nodes: writable<Node[]>(nodes),
                    edges: writable<Edge[]>(edges),
                    loading: false

                }

            }));
        } catch (error) {
            console.error('Error loading architecture:', error);
            update(store => ({
                ...store,
                activeArchitecture: undefined,
                loading: false
            }));
        }
    }

    const clearActiveArchitecture = (): void => {
        update((store) => {
            store.activeArchitecture = undefined
            return store;
        });
    }

    const deleteArchitecture = async (id: ArchitectureId): Promise<void> => {
        await fetch(`${BACKEND_API_BASE_URL}/architecture/delete`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ id: id })
        })
        getAvailableArchitectures();
    }

    const saveActiveArchitecture = async (isNew: boolean = false): Promise<void> => {
        const aStore = get(architectureStore);
        if (!aStore.activeArchitecture) {
            return;
        }
        const nodes = get(aStore.activeArchitecture.nodes);
        const edges = get(aStore.activeArchitecture.edges);
        const architecture: NetworkArchitectureDescription = {
            id: aStore.activeArchitecture.id as ArchitectureId ?? '',
            data: {
                data: {
                    inputs: [], //TODO
                    layers: nodes.map((node) => {
                        const parameters = get(node.data.parameters as Writable<{ parameter: Parameter<any>; value: ParameterValue<any>; }[]>);
                        return {

                            instance_id: parseInt(node.id, 10),
                            layer_id: get(node.data.layer_id as Writable<string>),
                            input: [],
                            param_values: Object.fromEntries(
                                parameters.map(({ parameter, value }) => [parameter.id, value])
                            )
                        };
                    }),
                    output: 0, //TODO
                } as ArchitectureDataDescription,
                layout: {
                    nodes: Object.fromEntries(
                        nodes.map(node => [
                            node.id,
                            {
                                x: node.position.x,
                                y: node.position.y,
                                metadata: {
                                    color: get(node.data.color as Writable<string>),
                                    title: get(node.data.title as Writable<string>),
                                }
                            }
                        ])
                    ),
                    edges
                } as NetworkLayoutDescription,
                meta: {
                    name: aStore.activeArchitecture.meta.name,
                    description: aStore.activeArchitecture.meta.description,
                } as ArchitectureMetaDescription,

            },
            info: {
                version: 0 as ArchitectureVersion, //TODO
            } as ArchitectureInfoDescription,

        };

        await fetch(`${BACKEND_API_BASE_URL}/architecture/${isNew ? 'create' : 'update'}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(
                isNew
                    ? { meta: architecture.data.meta, data: architecture.data.data, layout: architecture.data.layout }
                    : { id: aStore.activeArchitecture.id, object: architecture.data }

            )
        }).then((response) => response.json()).then((data: { id: string }) => {
            if (isNew) {
                aStore.availableArchitectures = [...(aStore.availableArchitectures ?? []), {
                    id: data.id,
                    meta: {
                        name: aStore.activeArchitecture?.meta.name ?? '',

                        description: aStore.activeArchitecture?.meta.description ?? '',
                    },
                    info: {
                        version: 0
                    }
                }];
            }
        });
    }


    const createNewArchitecture = async (name: string, description?: string): Promise<void> => {
        update((store) => {
            store.activeArchitecture = {
                meta: {
                    name: name,
                    description: description,
                },
                nodes: writable<Node[]>([]),
                edges: writable<Edge[]>([]),
                loading: false
            }
            return store;
        });
        saveActiveArchitecture(true);
    }

    const addNodeToActiveArchitecture = (node: Node): void => {
        update((store) => {
            store.activeArchitecture?.nodes.update((nodes) => {
                nodes.push(node);
                return nodes;
            });
            return store;
        });
    }

    const deleteNodeFromActiveArchitecture = (id: string): void => {
        update((store) => {
            store.activeArchitecture?.nodes.update((nodes) => {
                nodes = nodes.filter((node) => node.id !== id);
                return nodes;
            });
            return store;
        });
    }


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
        deleteNodeFromActiveArchitecture
    };
}

export const architectureStore = createArchitectureStore();