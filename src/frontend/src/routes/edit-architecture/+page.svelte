<script lang="ts">
    import DnDProvider from "$lib/components/DnDProvider.svelte";
    import Flow from "$lib/components/NodeEditor/NodeEditor.svelte";
    import NavBar from "$lib/components/General/NavBar.svelte";
    import { SvelteFlowProvider} from "@xyflow/svelte";
    import { Header } from "kiwi-nl";
    import { writable, type Writable } from "svelte/store";
    import { architectureStore } from "$lib/stores/ArchitectureStore";
    import { onMount } from "svelte";
    import { page } from '$app/state';
    import type { ArchitectureId } from "$lib/types/architecture";
    import type { Edge, Node } from '@xyflow/svelte';
    
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
    onMount(async () => {
        // uncomment this once the new endpoint for architecture and layout are working.
        // await architectureStore.loadArchitectureById($architectureStore.architectureIds[0]);
	});
    let id: ArchitectureId | null = page.url.searchParams.get('id');

    let onSave = () => {
        console.log(id);
        architectureStore.saveActiveArchitecture(id as string);
    }
</script>

<div class="wrapper">
    <div class="nav-bar">
        <NavBar></NavBar>
    </div>
    <main class="main">
        <div class="main__header">
            <Header>Editing Architecture: TITLE</Header>
        </div>
        <SvelteFlowProvider>
            <DnDProvider>
                <Flow
                    {onSave}
                    onCreateNode={architectureStore.addNodeToActiveArchitecture}
                    onDeleteNode={architectureStore.deleteNodeFromActiveArchitecture}
                    nodes={architectureNodes}
                    edges={architectureEdges}
                />
            </DnDProvider>
        </SvelteFlowProvider>

    </main>
</div>

<style lang="scss">
    .wrapper {
        margin: 0 auto;
        width: 100%;
        height: 100%;
        display: grid;
        grid-template-columns: 12% 88%;
        /* grid-gap: 10px; */
        grid-template-rows: 100%;
    }
    .main {
        background-color: white;
        padding: 1em 2em;
        display: flex;
        flex-direction: column;
        justify-content: center;
        max-height: 100vh;
        overflow-y: scroll;
        &__header {
            display: flex;
            justify-content: center;
            padding: 50px;
        }
    }
</style>
