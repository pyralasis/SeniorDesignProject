<script lang="ts">
    import type { Layer } from '$lib/types/layer';
    import { useDnD, type DnDContext } from '../../utilities/DnDUtils';
    import SidebarLayer from './SidebarNode.svelte';
    import { onMount } from 'svelte';
    import { BackendApi } from '$lib/utilities/api.utilities';
    import { type NodeType } from '$lib/types/node-type.enum';

    const dndContext = useDnD();
    let layers: Layer<any>[] = [];
    export let expanded: boolean = true;

    const onDragStart = (event: DragEvent, nodeType: NodeType, layerBlueprint: Layer<any>) => {
        if (!event.dataTransfer) {
            return null;
        }
        if (dndContext) {
            dndContext.set({ type: nodeType, layerBlueprint: layerBlueprint });
        }
        event.dataTransfer.effectAllowed = 'move';
    };

    // -------------------------------
    // Lifecycle Hooks
    // -------------------------------
    onMount(() => {
        BackendApi.getAvailableLayers().then((response) => {
            layers = response;
        });
    });
</script>

<div class="sidebar" style="width: {expanded ? 'fit-content' : '0px'}; opacity: {expanded ? 1 : 0};">
    <h3 class="sidebar__header">Available Layers</h3>
    <p class="sidebar__subheader">Drag and drop to add a layer to the architecture</p>
    <div class="sidebar__nodes-container">
        {#each layers as layer}
            <SidebarLayer {layer} {onDragStart} />
        {/each}
    </div>
</div>

<style lang="scss">
    .sidebar {
        width: fit-content;
        font-size: 12px;
        display: flex;
        flex-direction: column;
        justify-content: start;
        align-items: center;
        height: 100%;
        border-right: 2px solid #ffffff;
        padding: 16px 8px 0 8px;
        background-color: #000000;

        &__nodes-container {
            position: relative;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding-top: 20px;
        }

        &__header {
            font-size: 24px;
            font-weight: 600;
            color: #ffffff;
            margin-bottom: 0;
        }

        &__subheader {
            font-size: 10px;
            font-weight: 400;
            color: #ffffff;
            text-align: center;
        }
    }
</style>
