<script module>
</script>

<script lang="ts">
    import { writable, type Writable } from 'svelte/store';
    import { type Node, SvelteFlow, Controls, Background, MiniMap, useSvelteFlow, type NodeTypes, type Edge } from '@xyflow/svelte';
    import { useDnD } from '$lib/utilities/DnDUtils';

    import LayerNode from '../nodes/LayerNode.svelte';
    import Sidebar from '$lib/components/Sidebar/Sidebar.svelte';
    import '@xyflow/svelte/dist/style.css';
    import { type Parameter, type ParameterValue } from '$lib/types/layer';
    import NodeEditorActions from './NodeEditorActions.svelte';
    import { setContext } from 'svelte';

    export let nodes: Writable<Node[]>;
    export let edges: Writable<Edge[]>;
    export let onDeleteNode: (nodeId: string) => void;
    export let onCreateNode: (node: Node) => void;
    export let onSave: () => void;

    const { screenToFlowPosition } = useSvelteFlow();
    const dndContext = useDnD();
    let selectedNodeTitle: Writable<string> | undefined;
    let sidebarExpanded: Writable<boolean> = writable(true);

    const xColor = writable<string>('#ff4000');
    setContext('xColor', xColor);
    setContext('sidebarExpanded', sidebarExpanded);

    function getParameterDefaultValue(parameter: Parameter<any>): { parameter: Parameter<any>; value: ParameterValue<any> } {
        return {
            parameter,
            value: {
                type: parameter.type,
                value: parameter.default,
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
                layer_id: writable<string>($dndContext.layerBlueprint.name),
                parameters: writable<{ parameter: Parameter<any>; value: ParameterValue<any> }[]>(
                    $dndContext.layerBlueprint.parameters.map(getParameterDefaultValue),
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
    };

    function onDelete() {
        onDeleteNode(selectedNode?.id ?? '');
    }

    function onClearNodes() {
        nodes.update((nodes) => (nodes = []));
    }

    $: selectedNode = $nodes.find((node) => node.selected);
    $: selectedNodeTitle = selectedNode?.data.title as Writable<string> | undefined;
    $: selectedNodeColor = selectedNode?.data.color as Writable<string> | undefined;
</script>

<div class="node-editor">
    <NodeEditorActions {selectedNodeTitle} {selectedNodeColor} {onDelete} {onClearNodes} />
    <div class="node-editor__content">
        <div class="node-editor__sidebar">
            <Sidebar expanded={$sidebarExpanded} />
        </div>
        <div class="node-editor__flow">
            <SvelteFlow {nodes} {edges} {nodeTypes} on:dragover={onDragOver} on:drop={onDrop}>
                <Background />
            </SvelteFlow>
        </div>
    </div>
</div>

<style lang="scss">
    .node-editor {
        display: flex;
        flex-direction: column;
        overflow: hidden;

        &__content {
            display: flex;
            flex-direction: row;
        }

        &__flow {
            width: 100%;
            height: 700px;
        }

        &__sidebar {
            width: fit-content;
        }
    }
</style>
