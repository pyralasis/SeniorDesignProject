<script lang="ts">
    import { writable, get, type Writable } from 'svelte/store';
    import { type Node, SvelteFlow, Background, useSvelteFlow, type NodeTypes, type Edge, type Connection } from '@xyflow/svelte';
    import { useDnD, type DnDContext } from '$lib/utilities/DnDUtils';
    import LayerNode from '../Node/LayerNode.svelte';
    import Sidebar from '$lib/components/Sidebar/Sidebar.svelte';
    import '@xyflow/svelte/dist/style.css';
    import { type Parameter, type ParameterValue } from '$lib/types/parameter';
    import NodeEditorActions from './NodeEditorActions.svelte';
    import { setContext } from 'svelte';
    import { SoundUtility } from '$lib/utilities/sound.utility';
    import SourceNode from '../Node/SourceNode.svelte';
    import TransformNode from '../Node/TransformNode.svelte';

    import InputNode from '../Node/InputNode.svelte';
    import OutputNode from '../Node/OutputNode.svelte';
    import ButtonEdge from '../Edge/ButtonEdge.svelte';
    import { type LayerInput, type LayerBlueprint, type TensorSize } from '$lib/types/layer';
    import { type HandleStatus, HandleStatusEnum } from '../Node/handle-status.enum';
    import ValuesOutputNode from '../Node/ValuesOutputNode.svelte';
    import LabelsOutputNode from '../Node/LabelsOutputNode.svelte';

    export let nodes: Writable<Node[]>;
    export let edges: Writable<Edge[]>;
    export let nodeblueprints: DnDContext[];
    export let nodeNameEditor: boolean = true;

    export let onDeleteNode: (nodeId: string) => void;
    export let onCreateNode: (node: Node) => void;
    export let onChange: () => void;
    export let onSave: () => void;
    export let onConnect: (connection: Connection) => void = () => {};
    export let onNodeOrEdgeDelete: () => void = () => {};
    export let runConnectionValidation: () => void = () => {};

    const { screenToFlowPosition } = useSvelteFlow();
    const dndContext = useDnD();
    let selectedNodeTitle: Writable<string> | undefined;
    let sidebarExpanded: Writable<boolean> = writable(true);

    const xColor = writable<string>('#FFFFFF');
    setContext('xColor', xColor);
    setContext('sidebarExpanded', sidebarExpanded);

    function getParameterDefaultValue(parameter: Parameter<any>): { parameter: Parameter<any>; value: ParameterValue<any> } {
        return {
            parameter,
            value: {
                type: parameter.type,
                val: parameter.default,
            },
        };
    }

    const onDragOver = (event: DragEvent) => {
        event.preventDefault();

        if (event.dataTransfer) {
            event.dataTransfer.dropEffect = 'move';
        }
    };

    const onDrop = (event: DragEvent) => {
        event.preventDefault();
        SoundUtility.playDrop(0.02);

        if (!$dndContext?.type) {
            return;
        }

        const position = screenToFlowPosition({
            x: event.clientX,
            y: event.clientY,
        });

        let newNode: Node;

        if ($dndContext?.type === 'layer') {
            newNode = {
                id: `${Math.floor(Math.random() * 1000000)}`,
                type: $dndContext?.type,
                data: {
                    color: writable<string>($xColor),
                    title: writable<string>('Untitled Node'),
                    name: writable<string>($dndContext.nodeBlueprint.name),
                    layer_id: $dndContext.nodeBlueprint.id,
                    parameters: writable<{ parameter: Parameter<any>; value: ParameterValue<any> }[]>(
                        $dndContext.nodeBlueprint.parameters.map(getParameterDefaultValue),
                    ),
                    expanded: writable<boolean>(false),
                    leftConnected: writable<boolean>(false),
                    rightConnected: writable<boolean>(false),
                    leftStatus: writable<HandleStatus>(HandleStatusEnum.default),
                    rightStatus: writable<HandleStatus>(HandleStatusEnum.default),
                    inputs: writable<LayerInput[]>(($dndContext.nodeBlueprint as LayerBlueprint<any>).inputs),
                    outputSize: writable<TensorSize>([]),
                },
                dragHandle: '.node__header',
                position: { x: position.x, y: position.y },
            } satisfies Node;
        } else if ($dndContext?.type === 'source' || $dndContext?.type === 'transform') {
            newNode = {
                id: `${Math.floor(Math.random() * 1000000)}`,
                type: $dndContext?.type,
                data: {
                    color: writable<string>($xColor),
                    title: writable<string>('Untitled Node'),
                    name: writable<string>($dndContext.nodeBlueprint.name),
                    ...($dndContext?.type === 'source' ? { src_id: $dndContext.nodeBlueprint.id } : {}),
                    ...($dndContext?.type === 'transform' ? { transform_id: $dndContext.nodeBlueprint.id } : {}),
                    parameters: writable<{ parameter: Parameter<any>; value: ParameterValue<any> }[]>(
                        $dndContext.nodeBlueprint.parameters.map(getParameterDefaultValue),
                    ),
                    expanded: writable<boolean>(false),
                    leftConnected: writable<boolean>(false),
                    rightConnected: writable<boolean>(false),
                },
                dragHandle: '.node__header',
                position: { x: position.x, y: position.y },
            } satisfies Node;
        } else if ($dndContext?.type === 'input') {
            if ($nodes.some((node) => node.type === 'input')) {
                alert('Only one input node is allowed.');
                return;
            }
            newNode = {
                id: `${Math.floor(Math.random() * 1000000)}`,
                type: 'input',
                data: {
                    color: writable<string>($xColor),
                    expanded: writable<boolean>(false),
                    rightConnected: writable<boolean>(false),
                    rightStatus: writable<HandleStatus>(HandleStatusEnum.default),
                    outputSize: writable<TensorSize>([0, 0]),
                },
                dragHandle: '.node__header',
                position: { x: position.x, y: position.y },
            } satisfies Node;
        } else if ($dndContext?.type === 'output') {
            if ($nodes.some((node) => node.type === 'output')) {
                alert('Only one output node is allowed.');
                return;
            }
            newNode = {
                id: `69`,
                type: 'output',
                data: {
                    color: writable<string>($xColor),
                    expanded: writable<boolean>(false),
                    leftConnected: writable<boolean>(false),
                    leftStatus: writable<HandleStatus>(HandleStatusEnum.default),
                },
                dragHandle: '.node__header',
                position: { x: position.x, y: position.y },
            } satisfies Node;
        } else if ($dndContext?.type === 'valuesOutput') {
            if ($nodes.some((node) => node.type === 'valuesOutput')) {
                alert('Only one label output node is allowed.');
                return;
            }
            newNode = {
                id: '70',
                type: 'valuesOutput',
                data: {
                    color: writable<string>($xColor),
                    expanded: writable<boolean>(false),
                    leftConnected: writable<boolean>(false),
                    leftStatus: writable<HandleStatus>(HandleStatusEnum.default),
                },
                dragHandle: '.node__header',
                position: { x: position.x, y: position.y },
            } satisfies Node;
        } else if ($dndContext?.type === 'labelsOutput') {
            if ($nodes.some((node) => node.type === 'labels-output')) {
                alert('Only one label output node is allowed.');
                return;
            }
            newNode = {
                id: '71',
                type: 'labelsOutput',
                data: {
                    color: writable<string>($xColor),
                    expanded: writable<boolean>(false),
                    leftConnected: writable<boolean>(false),
                    leftStatus: writable<HandleStatus>(HandleStatusEnum.default),
                },
                dragHandle: '.node__header',
                position: { x: position.x, y: position.y },
            } satisfies Node;
        } else {
            return;
        }

        onCreateNode(newNode);
    };

    const nodeTypes: NodeTypes = {
        layer: LayerNode,
        source: SourceNode,
        transform: TransformNode,
        input: InputNode,
        output: OutputNode,
        valuesOutput: ValuesOutputNode,
        labelsOutput: LabelsOutputNode,
    };

    const edgeTypes = {
        button: ButtonEdge,
    };

    function onDelete() {
        onDeleteNode(selectedNode?.id ?? '');
    }

    function onClearNodes() {
        if (get(nodes).length === 0) {
            return;
        }
        onSave();
        nodes.update((nodes) => (nodes = []));
    }

    $: selectedNode = $nodes?.find((node) => node.selected);
    $: selectedNodeTitle = selectedNode?.data.title as Writable<string> | undefined;
    $: selectedNodeColor = selectedNode?.data.color as Writable<string> | undefined;
</script>

<div class="node-editor">
    <NodeEditorActions {selectedNodeTitle} {selectedNodeColor} {onDelete} {onClearNodes} {onChange} {onSave} {nodeNameEditor} />
    <div class="node-editor__content">
        <div class="node-editor__sidebar">
            <Sidebar nodes={nodeblueprints} expanded={$sidebarExpanded} />
        </div>
        <div class="node-editor__flow">
            <SvelteFlow
                {nodes}
                {edges}
                {nodeTypes}
                {edgeTypes}
                fitView
                on:dragover={onDragOver}
                on:drop={onDrop}
                on:nodedragstart={onChange}
                onconnect={onConnect}
                ondelete={onNodeOrEdgeDelete}
            >
                <Background bgColor="#111111" patternColor="#FFFFFF" />
            </SvelteFlow>
        </div>
    </div>
</div>

<style lang="scss">
    .node-editor {
        display: flex;
        flex-direction: column;
        background-color: #111111;
        border-bottom: 1px solid #ffffff;
        height: 75%;

        &__content {
            display: flex;
            flex-direction: row;
            height: 100%;
            box-sizing: border-box;
        }

        &__flow {
            width: 100%;
            height: 100%;
            box-sizing: border-box;
        }
    }

    :global(.svelte-flow__node) {
        width: fit-content;
        padding: 0;
    }
</style>
