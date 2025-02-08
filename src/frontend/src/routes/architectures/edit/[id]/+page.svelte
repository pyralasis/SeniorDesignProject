<script lang="ts">
    import { SvelteFlowProvider, type Edge, type Node } from '@xyflow/svelte';
    import DnDProvider from '$lib/components/DnDProvider.svelte';
    import NodeEditor from '$lib/components/NodeEditor/NodeEditor.svelte';
    import { writable, type Writable } from 'svelte/store';
    import { architectureStore } from '$lib/stores/ArchitectureStore';
    import Spinner from '$lib/components/Spinner/Spinner.svelte';
    import { onMount } from 'svelte';
    import { page } from '$app/state';

    let nodes: Writable<Node[]>;
    let edges: Writable<Edge[]>;

    $: id = page.params.id;

    architectureStore.subscribe((store) => {
        if (!store.activeArchitecture) {
            return;
        }
        nodes = store?.activeArchitecture?.nodes;
        edges = store?.activeArchitecture?.edges;
    });

    function onSave() {
        architectureStore.saveActiveArchitecture();
    }

    onMount(async () => {
        await architectureStore.loadArchitectureById(id);
    });
</script>

<button on:click={onSave}>Save</button>

<SvelteFlowProvider>
    <DnDProvider>
        {#if $architectureStore.activeArchitecture?.loading}
            <div class="spinner-container">
                <Spinner />
            </div>
        {:else if !$architectureStore.activeArchitecture?.loading && nodes && edges}
            <NodeEditor
                {onSave}
                onCreateNode={architectureStore.addNodeToActiveArchitecture}
                onDeleteNode={architectureStore.deleteNodeFromActiveArchitecture}
                {nodes}
                {edges}
            />
        {:else}
            <div class="spinner-container">
                <Spinner />
            </div>
        {/if}
    </DnDProvider>
</SvelteFlowProvider>

<style>
    .spinner-container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100%;
    }
</style>
