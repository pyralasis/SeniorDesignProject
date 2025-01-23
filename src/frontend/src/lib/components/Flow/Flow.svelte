<script lang="ts">
    import { writable, type Writable } from 'svelte/store';
    import { type Node, SvelteFlow, Controls, Background, MiniMap, useSvelteFlow, type NodeTypes } from '@xyflow/svelte';
    import { useDnD } from '$lib/utilities/DnDUtils';

    import BNode from '../nodes/BNode.svelte';
    import Sidebar from '$lib/components/Sidebar/Sidebar.svelte';
    import '@xyflow/svelte/dist/style.css';
    import { setContext } from 'svelte';
    import { NodeFieldTypeEnum, type NodeField } from '../nodes/types/node-field.interface';

    const nodes: Writable<Node[]> = writable([]);

    const edges = writable([]);
    const selectedNodeId: Writable<string> = writable('');
    setContext('selectedNodeId', selectedNodeId);

    const { screenToFlowPosition } = useSvelteFlow();
    const type = useDnD();

    const onDragOver = (event: DragEvent) => {
        event.preventDefault();

        if (event.dataTransfer) {
            event.dataTransfer.dropEffect = 'move';
        }
    };

    const onDrop = (event: DragEvent) => {
        event.preventDefault();

        if (!$type) {
            return;
        }

        const position = screenToFlowPosition({
            x: event.clientX,
            y: event.clientY,
        });

        const newNode = {
            id: `${Math.floor(Math.random() * 1000000)}`,
            type: 'testNode',
            data: {
                color: writable('#ff4000'),
                title: writable('Node'),
                fields: writable<NodeField[]>([
                    { label: 'Boolean', value: 'Value 1', type: NodeFieldTypeEnum.boolean, required: false },
                    { label: 'Serires', value: 'Value 2', type: NodeFieldTypeEnum.series, required: false },
                    { label: 'Input', value: 'Value 3', type: NodeFieldTypeEnum.input, required: false },
                ]),
            },
            position: { x: position.x, y: position.y },
        } satisfies Node;

        $nodes.push(newNode);
        $nodes = $nodes;
    };

    const nodeTypes: NodeTypes = {
        testNode: BNode,
    };
</script>

<main>
    <SvelteFlow {nodes} {edges} {nodeTypes} fitView on:dragover={onDragOver} on:drop={onDrop} on:click={() => selectedNodeId.set('')}>
        <Controls />
        <Background />
        <MiniMap />
    </SvelteFlow>
    <Sidebar />
</main>

<style>
    main {
        height: 50vh;
        display: flex;
        flex-direction: column-reverse;
    }
</style>
