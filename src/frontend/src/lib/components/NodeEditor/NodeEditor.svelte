<script module>
</script>

<script lang="ts">
    import { writable, type Writable } from 'svelte/store';
    import { type Node, SvelteFlow, Controls, Background, MiniMap, useSvelteFlow, type NodeTypes, type Edge } from '@xyflow/svelte';
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
    const { fitView } = useSvelteFlow();

    export let nodes: Writable<Node[]>;
    export let edges: Writable<Edge[]>;
    export let nodeblueprints: DnDContext[];

    export let onDeleteNode: (nodeId: string) => void;
    export let onCreateNode: (node: Node) => void;
    export let onSave: () => void;

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

        const newNode = {
            id: `${Math.floor(Math.random() * 1000000)}`,
            type: $dndContext?.type,
            data: {
                color: writable<string>($xColor),
                title: writable<string>('Untitled Node'),
                name: writable<string>($dndContext.nodeBlueprint.name),
                layer_id: writable<string>($dndContext.nodeBlueprint.id),
                parameters: writable<{ parameter: Parameter<any>; value: ParameterValue<any> }[]>(
                    $dndContext.nodeBlueprint.parameters.map(getParameterDefaultValue),
                ),
                expanded: writable<boolean>(false),
            },
            dragHandle: '.node__header',
            position: { x: position.x, y: position.y },
        } satisfies Node;

        onCreateNode(newNode);
    };

    const nodeTypes: NodeTypes = {
        layer: LayerNode,
        source: SourceNode,
        transform: TransformNode,
    };

    function onDelete() {
        onDeleteNode(selectedNode?.id ?? '');
    }

    function onClearNodes() {
        nodes.update((nodes) => (nodes = []));
    }

    $: selectedNode = $nodes?.find((node) => node.selected);
    $: selectedNodeTitle = selectedNode?.data.title as Writable<string> | undefined;
    $: selectedNodeColor = selectedNode?.data.color as Writable<string> | undefined;
</script>

<div class="node-editor">
    <NodeEditorActions {selectedNodeTitle} {selectedNodeColor} {onDelete} {onClearNodes} />
    <div class="node-editor__content">
        <div class="node-editor__sidebar">
            <Sidebar nodes={nodeblueprints} expanded={$sidebarExpanded} />
        </div>
        <div class="node-editor__flow">
            <SvelteFlow {nodes} {edges} {nodeTypes} on:dragover={onDragOver} on:drop={onDrop}>
                <Background bgColor="#111111" patternColor="#FFFFFF" />
            </SvelteFlow>
        </div>
    </div>
</div>

<style lang="scss">
    .node-editor {
        display: flex;
        flex-direction: column;
        overflow: hidden;
        background-color: #111111;
        height: 100%;

        &__content {
            display: flex;
            flex-direction: row;
            height: calc(100% + 30px);
        }

        &__flow {
            width: 100%;
            height: 100%;
        }

        &__sidebar {
            width: fit-content;
        }
    }
</style>
