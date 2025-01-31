<script module>
</script>

<script lang="ts">
    import { writable, type Writable } from 'svelte/store';
    import { type Node, SvelteFlow, Controls, Background, MiniMap, useSvelteFlow, type NodeTypes, type Edge } from '@xyflow/svelte';
    import { useDnD } from '$lib/utilities/DnDUtils';

    import LayerNode from '../nodes/LayerNode.svelte';
    import Sidebar from '$lib/components/Sidebar/Sidebar.svelte';
    import '@xyflow/svelte/dist/style.css';
    import { setContext } from 'svelte';
    import { type Parameter, type ParameterValue } from '$lib/types/layer';
    import { Button } from 'kiwi-nl';

    export let nodes: Writable<Node[]>;
    export let edges: Writable<Edge[]>;
    export let onSave: () => void;

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
                color: writable<string>('#ff4000'),
                title: writable<string>('Node'),
                layer_id: writable<string>($dndContext.layerBlueprint.name),
                parameters: writable<{ parameter: Parameter<any>; value: ParameterValue<any> }[]>(
                    $dndContext.layerBlueprint.parameters.map(getParameterDefaultValue),
                ),
            },
            position: { x: position.x, y: position.y },
        } satisfies Node;

        nodes.update((nodes) => {
            nodes.push(newNode);
            return nodes;
        });
    };

    const nodeTypes: NodeTypes = {
        layer: LayerNode,
    };

    function handleSave() {
        onSave();
    }
</script>

<main>
    {#key nodes}
        <SvelteFlow {nodes} {edges} {nodeTypes} on:dragover={onDragOver} on:drop={onDrop}>
            <Background />
        </SvelteFlow>
    {/key}
    <Sidebar />
    <Button on:click={handleSave}>Save Node Architecture</Button>
</main>

<style>
    main {
        height: 75vh;
        display: flex;
        flex-direction: column-reverse;
    }
</style>
