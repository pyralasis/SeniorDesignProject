<script lang="ts">
    import { writable, type Writable } from 'svelte/store';
    import { type Node, SvelteFlow, Controls, Background, MiniMap, useSvelteFlow, type NodeTypes } from '@xyflow/svelte';
    import { useDnD } from '$lib/utilities/DnDUtils';

    import BNode from '../nodes/BNode.svelte';
    import Sidebar from '$lib/components/Sidebar/Sidebar.svelte';
    import '@xyflow/svelte/dist/style.css';
    import { setContext } from 'svelte';

    const nodes: Writable<Node[]> = writable([
        {
            id: `${Math.random()}`,
            type: 'testNode',
            data: {
                color: writable('#ff4000'),
                title: writable('Node'),
                fields: writable([{ label: 'Field 1' }, { label: 'Field 2' }]),
            },
            position: { x: 0, y: 0 },
        },
    ]);

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
            id: `${Math.random()}`,
            type: 'testNode',
            data: { color: writable('#ff4000'), title: writable('Node') },
            position: { x: 0, y: 0 },
        } satisfies Node;

        $nodes.push(newNode);
        $nodes = $nodes;
    };

    const nodeTypes: NodeTypes = {
        testNode: BNode,
    };
</script>

<main>
    <SvelteFlow {nodes} {edges} {nodeTypes} fitView on:dragover={onDragOver} on:drop={onDrop}>
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
