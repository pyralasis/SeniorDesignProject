import { BACKEND_API_BASE_URL } from "$lib/utilities/api.constants";
import { BackendApi } from "$lib/utilities/api.utilities";
import { get, writable, type Writable } from "svelte/store";
import type { NetworkLayoutDescription } from "$lib/types/layout";
import type { Node, Edge } from "@xyflow/svelte";
import type { Parameter, ParameterValue } from "$lib/types/parameter";
import type {
    AvailablePipelinesResponse,
    LoadPipelineResponse,
    PipelineStore,
    PipelineStoreProps,
} from "./types/pipeline-store.interface";
import type {
    PipelineId,
    NetworkPipelineDescription,
    PipelineConfig,
    PipelineMetaDescription,
    PipelineVersion,
    PipelineInfoDescription,
    PipelineElement,
    InstanceId,
} from "$lib/types/pipeline";
import type { TransformConfig, TransformId } from "$lib/types/transform";
import type { SourceConfig, SourceId } from "$lib/types/source";
import { NodeTypeEnum } from "$lib/types/node-type.enum";
import { PipelineStatusEnum } from "$lib/stores/types/pipeline-store.interface";
import { HandleStatusEnum } from "$lib/components/Node/handle-status.enum";

function getTransformParametersByTransformId(transformId: TransformId): Promise<Parameter<any>[]> {
    return BackendApi.getAvailableTransforms().then((transforms) => {
        const transform = transforms.find((t) => t.id === transformId);
        console.log("Transform found: ", transform);
        return transform?.parameters || [];
    });
}

async function getSourceParametersBySourceId(sourceId: SourceId): Promise<Parameter<any>[]> {
    return BackendApi.getAvailableSources().then((sources) => {
        const source = sources.find((s) => s.id === sourceId);
        return source?.parameters || [];
    });
}

function findParameterById(parameters: any[], id: string): Parameter<any> {
    return parameters.find((parameter) => parameter.id === id);
}

function parseElements(nodes: Node[], edges: Edge[]): PipelineElement[] {
    return nodes.map((node) => {
        const parameters = get(node.data.parameters as Writable<{ parameter: Parameter<any>; value: ParameterValue<any> }[]>);
        if (node.type === "source") {
            return {
                type: NodeTypeEnum.Source,
                src_id: node.data.src_id,
                instance_id: parseInt(node.id),
                param_values: parameters.map(({ parameter, value }) => [parameter.id, value]),
            } as SourceConfig;
        } else if (node.type === "transform") {
            return {
                type: NodeTypeEnum.Transform,
                transform_id: node.data.transform_id,
                instance_id: parseInt(node.id),
                param_values: parameters.map(({ parameter, value }) => [parameter.id, value]),
                input: edges.find((edge) => edge.target === node.id)?.source ?? -1,
            } as TransformConfig;
        }
        return undefined;
    }).filter((element): element is PipelineElement => element !== undefined);
}

async function parseLayersIntoNodesAndEdges(elements: PipelineElement[], layout: any, labelOutput: number, valueOutput: number): Promise<{ nodes: Node[]; edges: Edge[] }> {
    let nodes: Node[] = [];
    let edges: Edge[] = layout.edges.map((edge: any) => edge as Edge);

    await Promise.all(
        elements.map(async (element: PipelineElement) => {
            let elementParameters: Parameter<any>[] = [];
            if (element.type === "source") {
                elementParameters = await getSourceParametersBySourceId(element.src_id);
            } else {
                elementParameters = await getTransformParametersByTransformId(element.transform_id);
            }

            nodes.push({
                id: element.instance_id.toString(),
                type: element.type,
                data: {
                    color: writable<string>(layout.nodes[element.instance_id]?.metadata.color ?? "#FFFFFF"),
                    title: writable<string>(layout.nodes[element.instance_id]?.metadata.title ?? "Untitled Layer"),
                    name: writable<string>(layout.nodes[element.instance_id]?.metadata.name ?? ""),
                    leftConnected: writable<boolean>(layout.nodes[element.instance_id]?.metadata.leftConnected ?? false),
                    rightConnected: writable<boolean>(layout.nodes[element.instance_id]?.metadata.rightConnected ?? false),
                    maxInputSize: writable<number>(layout.nodes[element.instance_id]?.metatdata?.maxInputSize ?? 0),
                    minInputSize: writable<number>(layout.nodes[element.instance_id]?.metadata?.minInputSize ?? 0),
                    ...(element.type === "source" ? { src_id: element.src_id } : { transform_id: element.transform_id }),
                    parameters: writable<{ parameter: Parameter<any>; value: ParameterValue<any> }[]>(
                        element.param_values.map(([key, value]) => {
                            let parameterTemplate = findParameterById(elementParameters, key);
                            return {
                                parameter: parameterTemplate,
                                value: value as ParameterValue<any>,
                            };
                        })
                    ),
                    expanded: writable<boolean>(false),
                },
                position: { x: layout.nodes[element.instance_id]?.x ?? 0, y: layout.nodes[element.instance_id]?.y ?? 0 },
                dragHandle: ".node__header",
            } satisfies Node);
            if (labelOutput > 0) {
                nodes.push({
                    id: '71',
                    type: 'labelsOutput',
                    data: {
                        leftConnected: writable<boolean>(layout.nodes['71']?.metadata.leftConnected ?? false),
                        leftStatus: writable<string>(layout.nodes['71']?.metadata.leftStatus ?? HandleStatusEnum.default),
                    },
                    position: { x: layout.nodes['71']?.x ?? 0, y: layout.nodes['71']?.y ?? 0 },
                    dragHandle: '.node__header',
                } satisfies Node);
            }
            if (valueOutput > 0) {
                nodes.push({
                    id: '70',
                    type: 'valuesOutput',
                    data: {
                        leftConnected: writable<boolean>(layout.nodes['70']?.metadata.leftConnected ?? false),
                        leftStatus: writable<string>(layout.nodes['70']?.metadata.leftStatus ?? HandleStatusEnum.default),
                    },
                    position: { x: layout.nodes['70']?.x ?? 0, y: layout.nodes['70']?.y ?? 0 },
                    dragHandle: '.node__header',
                } satisfies Node);
            }
        })
    );

    return { nodes, edges };
}

const createPipelineStore = (): PipelineStore => {
    const { subscribe, set, update } = writable<PipelineStoreProps>({
        availablePipelines: undefined,
        activePipeline: undefined,
        isSaved: true,
        saveStatus: PipelineStatusEnum.Success,
    });
    const updateSaveStatus = (saved: boolean, status: PipelineStatusEnum): void => {
        update((state) => {
            if (state.isSaved === saved && state.saveStatus === status) return state;
            return {
                ...state,
                isSaved: saved,
                saveStatus: status,
            };
        });
    };

    const getAvailablePipelines = async (): Promise<void> => {
        await fetch(`${BACKEND_API_BASE_URL}/pipeline/available`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            },
        })
            .then((response) => response.json())
            .then((data) => {
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
                            },
                        };
                    });
                    return store;
                });
            });
    };

    const loadPipelineById = async (id: PipelineId): Promise<void> => {
        try {
            update((store) => ({ ...store, activePipeline: undefined, loading: true }));

            const response = await fetch(
                `${BACKEND_API_BASE_URL}/pipeline/load?${new URLSearchParams({ id: id.toString() }).toString()}`
            );
            const data = ((await response.json()) as LoadPipelineResponse).object;
            const pipData = data.content.data;
            const layoutData = data.content.layout;
            const { nodes, edges } = await parseLayersIntoNodesAndEdges(pipData.elements, layoutData, pipData.label_output, pipData.value_output);
            update((store) => ({
                ...store,
                activePipeline: {
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
            console.error("Error loading pipeline:", error);
            update((store) => ({
                ...store,
                activePipeline: undefined,
                loading: false,
            }));
        }
    };

    const clearActivePipeline = (): void => {
        update((store) => {
            store.activePipeline = undefined;
            updatePipelineSaveStatus();
            return store;
        });
    };

    const deletePipeline = async (id: PipelineId): Promise<void> => {
        await fetch(`${BACKEND_API_BASE_URL}/pipeline/delete`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ id: id }),
        });
        getAvailablePipelines();
    };

    const saveActivePipeline = async (isNew: boolean = false): Promise<boolean> => {
        const pStore = get(pipelineStore);
        if (!pStore.activePipeline) {
            return false; // Return false if no active pipeline exists
        }

        const nodes = get(pStore.activePipeline.nodes);
        const edges = get(pStore.activePipeline.edges);
        const valueOutputNode = nodes.find((node) => node.id === "70");
        const labelOutputNode = nodes.find((node) => node.id === "71");

        const pipeline: NetworkPipelineDescription = {
            id: (pStore.activePipeline.id as PipelineId) ?? -1,
            content: {
                data: {
                    elements: parseElements(nodes, edges),
                    value_output: valueOutputNode ? parseInt(edges.filter((edge) => edge.target === valueOutputNode.id)[0]?.source ?? 0) as InstanceId : -1,
                    label_output: labelOutputNode ? parseInt(edges.filter((edge) => edge.target === labelOutputNode.id)[0]?.source ?? 0) as InstanceId : -1,
                } as PipelineConfig,
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
                                    name: get(node.data.name as Writable<string>),
                                    expanded: get(node.data.expanded as Writable<boolean>),
                                    leftConnected: get(node.data.leftConnected as Writable<boolean>),
                                    rightConnected: get(node.data.rightConnected as Writable<boolean>),
                                    maxInputSize: get(node.data.maxInputSize as Writable<number>),
                                    minInputSize: get(node.data.minInputSize as Writable<number>),
                                },
                            },
                        ])
                    ),
                    edges,
                } as NetworkLayoutDescription,
                meta: {
                    name: pStore.activePipeline.meta.name,
                    description: pStore.activePipeline.meta.description,
                    created_at: pStore.activePipeline.meta.created_at,
                    last_modified: new Date().toISOString(),
                } as PipelineMetaDescription,
            },
            info: {
                version: pStore.activePipeline?.meta.version ?? (0 as PipelineVersion), // TODO: Handle versioning properly
            } as PipelineInfoDescription,
        };

        try {
            const response = await fetch(`${BACKEND_API_BASE_URL}/pipeline/${isNew ? "create" : "update"}`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(
                    isNew
                        ? { meta: pipeline.content.meta, data: pipeline.content.data, layout: pipeline.content.layout }
                        : { id: pStore.activePipeline.id, object: pipeline.content }
                ),
            });

            if (!response.ok) throw new Error(`Server Error: ${response.status}`);

            const data: { id: string } = await response.json();

            if (isNew) {
                getAvailablePipelines(); // Fetch latest pipelines if newly created
            }

            return true;
        } catch (error) {
            console.error("Save failed:", error);
            return false;
        }
    };

    const createNewPipeline = async (name: string, description?: string): Promise<void> => {
        update((store) => {
            store.activePipeline = {
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
        saveActivePipeline(true);
    };

    const addNodeToActivePipeline = (node: Node): void => {
        update((store) => {
            store.activePipeline?.nodes.update((nodes) => {
                nodes.push(node);
                return nodes;
            });
            updatePipelineSaveStatus();
            return store;
        });
    };

    const deleteNodeFromActivePipeline = (id: string | null): void => {
        update((store) => {
            if (!store.activePipeline || !store.activePipeline.nodes) {
                console.log("No active pipeline or nodes - Deletion blocked");
                return store;
            }

            let currentNodes = get(store.activePipeline.nodes);

            if (!id) {
                console.log("No node selected for deletion");
                return store;
            }

            if (!currentNodes.some((node) => node.id === id)) {
                console.log(`Node with id ${id} does not exist - No changes made`);
                return store;
            }

            console.log("Node found, deleting...");
            store.activePipeline.nodes.update((nodes) => {
                return nodes.filter((node) => node.id !== id);
            });

            console.log("Updates Save Status");
            updatePipelineSaveStatus();

            return store;
        });
    };
    const updatePipelineSaveStatus = async (): Promise<void> => {
        try {
            console.log("updatePipelineSaveStatus called");

            updateSaveStatus(false, PipelineStatusEnum.Saving);
            console.log("Status set to Saving...");

            const success = await saveActivePipeline();

            if (success) {
                setTimeout(() => {
                    console.log("Save successful - updating UI state");
                    updateSaveStatus(true, PipelineStatusEnum.Success);
                }, 500);
            } else {
                console.log("Save failed - updating UI state");
                updateSaveStatus(false, PipelineStatusEnum.Failed);
            }
        } catch (error) {
            console.error("Save error:", error);
            updateSaveStatus(false, PipelineStatusEnum.Failed);
        }
    };
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
        deleteNodeFromActivePipeline,
        updateSaveStatus,
        updatePipelineSaveStatus,
    };
};

export const pipelineStore = createPipelineStore();
