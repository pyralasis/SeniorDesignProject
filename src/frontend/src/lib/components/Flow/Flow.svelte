<script module>
    export const nodes: Writable<Node[]> = writable([]);
</script>

<script lang="ts">
    import { writable, type Writable } from 'svelte/store';
    import { type Node, SvelteFlow, Controls, Background, MiniMap, useSvelteFlow, type NodeTypes, type Edge } from '@xyflow/svelte';
    import { useDnD, type DnDContext } from '$lib/utilities/DnDUtils';

    import LayerNode from '../nodes/LayerNode.svelte';
    import Sidebar from '$lib/components/Sidebar/Sidebar.svelte';
    import '@xyflow/svelte/dist/style.css';
    import { setContext } from 'svelte';
    import { type Parameter, type ParameterValue } from '$lib/types/layer';

    const edges: Writable<Edge[]> = writable([]);
    const selectedNodeId: Writable<string> = writable('');

    setContext('selectedNodeId', selectedNodeId);

    const { screenToFlowPosition } = useSvelteFlow();
    const dndContext = useDnD();

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
                color: writable('#ff4000'),
                title: writable('Node'),
                parameters: writable<{ parameter: Parameter<any>; value: ParameterValue<any> }[]>(
                    $dndContext.layerBlueprint.parameters.map(getParameterDefaultValue),
                ),
            },
            position: { x: position.x, y: position.y },
        } satisfies Node;

        $nodes.push(newNode);
        $nodes = $nodes;
    };

    const nodeTypes: NodeTypes = {
        layer: LayerNode,
    };
</script>

<main>
    <SvelteFlow {nodes} {edges} {nodeTypes} on:dragover={onDragOver} on:drop={onDrop}>
        <Controls />
        <Background />
        <MiniMap />
    </SvelteFlow>
    <Sidebar />
</main>

<style>
    main {
        height: 75vh;
        display: flex;
        flex-direction: column-reverse;
    }
</style>
