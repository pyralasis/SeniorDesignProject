import { BACKEND_API_BASE_URL } from "$lib/utilities/api.constants";
import { BackendApi } from "$lib/utilities/api.utilities";
import { get, writable, type Writable } from "svelte/store";
import type { NetworkLayoutDescription } from "$lib/types/layout";
import type { Node, Edge } from "@xyflow/svelte";
import type { Parameter, ParameterValue } from "$lib/types/parameter";
import type { AvailablePipelinesResponse, LoadPipelineResponse, PipelineStore, PipelineStoreProps } from "./types/pipeline-store.interface";
import type { PipelineId, NetworkPipelineDescription, PipelineConfig, PipelineMetaDescription, PipelineVersion, PipelineInfoDescription, PipelineElement, InstanceId } from "$lib/types/pipeline";
import type { TransformId } from "$lib/types/transform";
import type { SourceId } from "$lib/types/source";

function getTransformParametersByTransformId(transformId: TransformId): Promise<Parameter<any>[]> {
    return BackendApi.getTransformById(transformId).then((layer) => {
        return layer.parameters;
    });
}

function getSourceParametersBySourceId(sourceId: SourceId): Promise<Parameter<any>[]> {
    return BackendApi.getSourceById(sourceId).then((source) => {
        return source.parameters;
    });
}

function findParameterById(parameters: any[], id: string): Parameter<any> {
    return parameters.find((parameter) => parameter.id === id);
}

async function parseLayersIntoNodesAndEdges(elements: PipelineElement[], layout: any): Promise<{ nodes: Node[], edges: Edge[] }> {
    let nodes: Node[] = [];
    let edges: Edge[] = layout.edges.map((edge: any) => edge as Edge);

    await Promise.all(elements.map(async (element: PipelineElement) => {
        let elementParameters: Parameter<any>[] = [];
        if (element.type === 'source') {
            elementParameters = await getSourceParametersBySourceId(element.src_id);
        } else {
            elementParameters = await getTransformParametersByTransformId(element.transform_id);
        }
        nodes.push({
            id: element.instance_id.toString(),
            type: element.type,
            data: {
                color: writable<string>(layout.nodes[element.instance_id]?.metadata.color ?? '#FFFFFF'),
                title: writable<string>(layout.nodes[element.instance_id]?.metadata.title ?? 'Untitled Layer'),
                name: writable<string>(layout.nodes[element.instance_id]?.metadata.name ?? ''),
                ...(element.type === 'source' ? { src_id: element.src_id } : { transform_id: element.transform_id }),
                parameters: writable<{ parameter: Parameter<any>; value: ParameterValue<any> }[]>(
                    Object.entries(element.param_values).map(([key, value]) => {
                        let parameterTemplate = findParameterById(elementParameters, key);
                        return ({
                            parameter: parameterTemplate,
                            value: value as ParameterValue<any>
                        });
                    })
                ),
                expanded: writable<boolean>(false),
            },
            position: { x: layout.nodes[element.instance_id]?.x ?? 0, y: layout.nodes[element.instance_id]?.y ?? 0 },
            dragHandle: '.node__header',
        } satisfies Node);

    }));


    return { nodes, edges };
}

const createPipelineStore = (): PipelineStore => {
    const { subscribe, set, update } = writable<PipelineStoreProps>({
        availablePipelines: undefined,
        activePipeline: undefined
    });

    const getAvailablePipelines = async (): Promise<void> => {
        await new Promise(resolve => setTimeout(resolve, 2000));
        await fetch(`${BACKEND_API_BASE_URL}/pipeline/available`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        })
            .then(response => response.json())
            .then(data => {
                let response = data as AvailablePipelinesResponse;
                update((store) => {
                    store.availablePipelines = response.available.map((pip) => {
                        return {
                            id: pip.id,
                            meta: {
                                name: pip.meta.name,
                                description: pip.meta.description,
                                last_modified: pip.meta.last_modified,
                                created_at: pip.meta.created_at,
                            },
                            info: {
                                version: pip.info.version,
                            }
                        };
                    });
                    return store;
                });
            });
    }

    const loadPipelineById = async (id: PipelineId): Promise<void> => {
        try {
            update(store => ({ ...store, activePipeline: undefined, loading: true }));

            const response = await fetch(`${BACKEND_API_BASE_URL}/pipeline/load?${new URLSearchParams({ id: id.toString() }).toString()}`);
            const data = (await response.json() as LoadPipelineResponse).object;
            const pipData = data.data.data;
            const layoutData = data.data.layout;

            const { nodes, edges } = await parseLayersIntoNodesAndEdges(
                pipData.elements,
                layoutData
            );
            update(store => ({
                ...store,
                activePipeline: {
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
                    loading: false

                }

            }));
        } catch (error) {
            console.error('Error loading pipeline:', error);
            update(store => ({
                ...store,
                activePipeline: undefined,
                loading: false
            }));
        }
    }

    const clearActivePipeline = (): void => {
        update((store) => {
            store.activePipeline = undefined
            return store;
        });
    }

    const deletePipeline = async (id: PipelineId): Promise<void> => {
        await fetch(`${BACKEND_API_BASE_URL}/pipeline/delete`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ id: id })
        })
        getAvailablePipelines();
    }

    const saveActivePipeline = async (isNew: boolean = false): Promise<void> => {
        const pStore = get(pipelineStore);
        if (!pStore.activePipeline) {
            return;
        }
        const nodes = get(pStore.activePipeline.nodes);
        const edges = get(pStore.activePipeline.edges);
        const pipeline: NetworkPipelineDescription = {
            id: pStore.activePipeline.id as PipelineId ?? -1,
            data: {
                data: {
                    elements: [],
                    value_output: -1,
                    label_output: -1,
                } as PipelineConfig,
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
                                    name: get(node.data.name as Writable<string>),
                                }
                            }
                        ])
                    ),
                    edges
                } as NetworkLayoutDescription,
                meta: {
                    name: pStore.activePipeline.meta.name,
                    description: pStore.activePipeline.meta.description,
                    created_at: pStore.activePipeline.meta.created_at,
                    last_modified: new Date().toISOString(),
                } as PipelineMetaDescription,

            },
            info: {
                version: pStore.activePipeline?.meta.version ?? 0 as PipelineVersion, //TODO
            } as PipelineInfoDescription,

        };

        await fetch(`${BACKEND_API_BASE_URL}/pipeline/${isNew ? 'create' : 'update'}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(
                isNew
                    ? { meta: pipeline.data.meta, data: pipeline.data.data, layout: pipeline.data.layout }
                    : { id: pStore.activePipeline.id, object: pipeline.data }

            )
        }).then((response) => response.json()).then((data: { id: string }) => {
            if (isNew) {
                getAvailablePipelines();
            }
        });
    }


    const createNewPipeline = async (name: string, description?: string): Promise<void> => {
        update((store) => {
            store.activePipeline = {
                meta: {
                    name: name,
                    description: description,
                    created_at: new Date().toISOString(),
                    last_modified: new Date().toISOString(),
                    version: 0
                },
                nodes: writable<Node[]>([]),
                edges: writable<Edge[]>([]),
                loading: false
            }
            return store;
        });
        saveActivePipeline(true);
    }

    const addNodeToActivePipeline = (node: Node): void => {
        update((store) => {
            store.activePipeline?.nodes.update((nodes) => {
                nodes.push(node);
                return nodes;
            });
            return store;
        });
    }

    const deleteNodeFromActivePipeline = (id: string): void => {
        update((store) => {
            store.activePipeline?.nodes.update((nodes) => {
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
        getAvailablePipelines,
        loadPipelineById,
        clearActivePipeline,
        deletePipeline,
        saveActivePipeline,
        createNewPipeline,
        addNodeToActivePipeline,
        deleteNodeFromActivePipeline
    };
}

export const pipelineStore = createPipelineStore();