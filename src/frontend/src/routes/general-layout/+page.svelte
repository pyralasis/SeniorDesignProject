<script module>
    export type dummyData = { tabID: number; tabTitle: string };
    let test: dummyData[] = [
        { tabID: 1, tabTitle: 'A' },
        { tabID: 2, tabTitle: 'B' },
    ];
    export let dummyTabs = writable<dummyData[]>(test);
</script>

<script lang="ts">
    import { SvelteFlowProvider } from '@xyflow/svelte';
    import DnDProvider from '$lib/components/DnDProvider.svelte';

    import NodeEditor from '$lib/components/NodeEditor/NodeEditor.svelte';
    import { writable, type Writable } from 'svelte/store';
    import type { Edge, Node } from '@xyflow/svelte';
    import { architectureStore } from '$lib/stores/ArchitectureStore';

    architectureStore.createNewArchitecture('New Architecture');

    let architectureNodes: Writable<Node[]> = writable([]);
    let architectureEdges: Writable<Edge[]> = writable([]);

    architectureStore.subscribe((store) => {
        if (!store.activeArchitecture) {
            return;
        }
        architectureNodes = store.activeArchitecture.nodes;
        architectureEdges = store.activeArchitecture.edges;
    });

    function onSave() {
        architectureStore.saveActiveArchitecture();
    }

    let closeTab = (tabID: number) => {
        let mytabs = $dummyTabs;
        let findTabByID = (element: dummyData, id: number) => {
            return element.tabID == id;
        };
        mytabs.splice(
            mytabs.findIndex((element) => findTabByID(element, tabID)),
            1,
        );
        $dummyTabs = mytabs;
    };

    function openTab(newTab: dummyData) {
        let mytabs = $dummyTabs;
        mytabs.push(newTab);
        $dummyTabs = mytabs;
    }
</script>

<SvelteFlowProvider>
    <DnDProvider>
        <NodeEditor
            {onSave}
            onCreateNode={architectureStore.addNodeToActiveArchitecture}
            onDeleteNode={architectureStore.deleteNodeFromActiveArchitecture}
            nodes={architectureNodes}
            edges={architectureEdges}
        />
    </DnDProvider>
</SvelteFlowProvider>

<style>
    .wrapper {
        margin: 0 auto;
        width: 100%;
        height: 100%;
        display: grid;
        grid-template-columns: 12% 88%;
        /* grid-gap: 10px; */
        grid-template-rows: 100%;
    }

    h1 {
        color: white;
    }
</style>
