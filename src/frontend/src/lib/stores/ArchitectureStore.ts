import { type ArchitectureStore, type ArchitectureStoreProps } from "./types/architecture-store.interface";
import { BACKEND_API_BASE_URL } from "$lib/utilities/api.constants";
import { BackendApi } from "$lib/utilities/api.utilities";
import { get, writable, type Writable } from "svelte/store";
import type { NetworkArchitectureDescription, ArchitectureId, NetworkLayerDescription, NetworkLayoutDescription, InputLayerDescription, LayoutId } from "$lib/types/architecture";
import type { Node, Edge } from "@xyflow/svelte";
import type { Parameter, ParameterValue } from "$lib/types/layer";
import type { AvailableArchitecturesResponse, NodeArchitecture } from "./types/architecture-store.interface";

function getLayerParametersByLayerId(layerId: string): Promise<any> {
    return BackendApi.getLayerById(layerId).then((layer) => {
        return layer.parameters;
    });
}

function findParameterById(parameters: any[], id: string): Parameter<any> {
    return parameters.find((parameter) => parameter.id === id);
}

function parseLayersIntoNodesAndEdges(layers: any[], layout: any): { nodes: Node[], edges: Edge[] } {
    let nodes: Node[] = [];
    let edges: Edge[] = layout.edges.map((edge: any) => { edge as Edge });

    layers.map(async (layer: any) => {
        const layerParameters = await getLayerParametersByLayerId(layer.id);
        nodes.push({
            id: layer.id,
            type: 'layer',
            data: {
                color: writable<string>(layout.nodes[layer.id].metadata.color),
                title: writable<string>(layout.nodes[layer.id].metadata.title),
                layer_id: writable<string>(layer.layer_id),
                parameters: writable<{ parameter: Parameter<any>; value: ParameterValue<any> }[]>(
                    Object.entries(layer.param_values).map(([key, value]) => {
                        let parameterTemplate = findParameterById(layerParameters, key);
                        return (
                            {
                                parameter: parameterTemplate,
                                value: value as ParameterValue<any>
                            });
                    })
                )
            },
            position: { x: layout.x, y: layout.y }
        } as Node);
    });

    return { nodes, edges };
}

const createArchitectureStore = (): ArchitectureStore => {
    const { subscribe, set, update } = writable<ArchitectureStoreProps>({
        architectureIds: [],
        activeArchitecture: undefined
    });

    const getAvailableArchitectures = (): void => {
        fetch(`${BACKEND_API_BASE_URL}/architecture/available`, {
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

    const loadArchitectureById = (id: ArchitectureId): void => {
        fetch(`${BACKEND_API_BASE_URL}/architecture/load`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ id: id })

        })
            .then(response => response.json())
            .then(data => {
                update((store) => {
                    const architecture = data.architecture;
                    const layout = data.layout
                    const { nodes, edges } = parseLayersIntoNodesAndEdges(architecture.description.layers, layout);
                    store.activeArchitecture = {
                        id: architecture.id,
                        fileName: architecture.file_name,
                        name: architecture.description.name,
                        nodes: writable<Node[]>(nodes),
                        edges: writable<Edge[]>(edges)
                    }
                    return store;
                });
            });
    }

    const clearActiveArchitecture = (): void => {
        update((store) => {
            store.activeArchitecture = undefined
            return store;
        });
    }

    const deleteArchitecture = (id: ArchitectureId): void => {
        fetch(`${BACKEND_API_BASE_URL}/architecture/delete`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ id: id })
        })
        getAvailableArchitectures();
    }

    const saveActiveArchitecture = (isNew: boolean = false): void => {
        let activeArchitecture: NodeArchitecture | undefined;
        let nodes: Node[] = [];
        let edges: Edge[] = [];
        subscribe((store) => {
            activeArchitecture = store.activeArchitecture as NodeArchitecture;
            nodes = get(activeArchitecture?.nodes ?? writable<Node[]>([]));
            edges = get(activeArchitecture?.edges ?? writable<Edge[]>([]));


        });
        if (activeArchitecture === undefined) {
            return;
        };
        let layout = {
            nodes: nodes.map((node) => {
                let color: string = get(node.data.color as Writable<string>);
                let title: string = get(node.data.title as Writable<string>);
                return {
                    x: node.position.x,
                    y: node.position.y,
                    metadata: {
                        color: color,
                        title: title,
                    }
                }
            }),
            edges: edges as any[]
        } as NetworkLayoutDescription;

        let architecture = {
            id: activeArchitecture.id as ArchitectureId,
            name: activeArchitecture.name,
            version: 0, //TODO: Implement versioning
            inputs: [] as InputLayerDescription[], //TODO: Implement input layers from the edges
            layers: nodes.map((node) => {
                let parameters: { parameter: Parameter<any>; value: ParameterValue<any> }[] = get(node.data.parameters as Writable<{ parameter: Parameter<any>; value: ParameterValue<any> }[]>);
                return {
                    id: parseInt(node.id, 10),
                    layer_id: node.data.layer_id,
                    input: [],
                    param_values:
                        Object.fromEntries(parameters.map(({ parameter, value }) => [parameter.id, value]))
                } as NetworkLayerDescription
            }) as NetworkLayerDescription[],
            layout: layout
        } as NetworkArchitectureDescription;

        console.log(architecture);

        fetch(`${BACKEND_API_BASE_URL}/architecture/${isNew ? 'create' : 'update'}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ architecture: architecture })
        })
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
                fileName: id + '.json',
                name: name,
                nodes: writable<Node[]>([]),
                edges: writable<Edge[]>([])
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