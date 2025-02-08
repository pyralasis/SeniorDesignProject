import { type ArchitectureStore, type ArchitectureStoreProps } from "./types/architecture-store.interface";
import { BACKEND_API_BASE_URL } from "$lib/utilities/api.constants";
import { BackendApi } from "$lib/utilities/api.utilities";
import { get, writable, type Writable } from "svelte/store";
import type { NetworkArchitectureDescription, ArchitectureId, NetworkLayerDescription, NetworkLayoutDescription, InputLayerDescription, LayoutId } from "$lib/types/architecture";
import type { Node, Edge } from "@xyflow/svelte";
import type { Parameter, ParameterValue } from "$lib/types/layer";
import type { ArchitectureData, AvailableArchitecturesResponse, LoadArchitectureResponse, NodeArchitecture } from "./types/architecture-store.interface";

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
                color: writable<string>(layout.nodes[layer.instance_id].metadata.color),
                title: writable<string>(layout.nodes[layer.instance_id].metadata.title),
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
            position: { x: layout.nodes[layer.instance_id].x, y: layout.nodes[layer.instance_id].y },
            dragHandle: '.node__header',
        } satisfies Node);
    }));

    return { nodes, edges };
}

const createArchitectureStore = (): ArchitectureStore => {
    const { subscribe, set, update } = writable<ArchitectureStoreProps>({
        architectureIds: [],
        activeArchitecture: undefined
    });

    const getAvailableArchitectures = async (): Promise<void> => {
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
                    store.architectureIds = response.available;
                    return store;
                });
            });
    }

    const loadArchitectureById = async (id: ArchitectureId): Promise<void> => {
        try {
            update(store => ({ ...store, activeArchitecture: undefined, loading: true }));

            const archResponse = await fetch(`${BACKEND_API_BASE_URL}/architecture/load?${new URLSearchParams({ id }).toString()}`);
            const archData = await archResponse.json() as LoadArchitectureResponse;

            const layoutResponse = await fetch(
                `${BACKEND_API_BASE_URL}/layout/load?${new URLSearchParams({
                    id: archData.data.data.layout_file
                }).toString()}`
            );
            const layoutData = await layoutResponse.json();

            const { nodes, edges } = await parseLayersIntoNodesAndEdges(
                archData.data.data.layers,
                layoutData.data.data
            );
            update(store => ({
                ...store,
                activeArchitecture: {
                    id: archData.data.id,
                    name: archData.data.data.name,
                    layout_file: archData.data.data.layout_file,
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
        const activeArchitecture = get(architectureStore).activeArchitecture;
        if (!activeArchitecture) {
            return;
        }

        const nodes = get(activeArchitecture.nodes);
        const edges = get(activeArchitecture.edges);
        const architecture: NetworkArchitectureDescription = {
            id: activeArchitecture.id,
            name: activeArchitecture.name,
            version: 0, //TODO
            inputs: [], //TODO
            output: 0, //TODO
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
            layout_file: activeArchitecture.layout_file,
        };


        const layout = {
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
        };

        await fetch(`${BACKEND_API_BASE_URL}/architecture/${isNew ? 'create' : 'update'}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(
                isNew
                    ? { data: architecture }
                    : { id: activeArchitecture.id, data: architecture }
            )
        });

        await fetch(`${BACKEND_API_BASE_URL}/layout/${isNew ? 'create' : 'update'}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                id: activeArchitecture.layout_file,
                data: layout
            })
        });
    }


    const createNewArchitecture = (name: string): void => {
        let id: ArchitectureId = Math.random().toString(36).substring(7);
        let existingIds: ArchitectureId[] = [];

        subscribe((store) => {
            existingIds = store.architectureIds;
        });

        while (existingIds.includes(id)) {
            id = Math.random().toString(36).substring(7);
        }

        update((store) => {
            store.architectureIds.push(id);
            store.activeArchitecture = {
                id: id,
                name: name,
                nodes: writable<Node[]>([]),
                edges: writable<Edge[]>([]),
                layout_file: id,
                loading: false
            }
            return store;
        });
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