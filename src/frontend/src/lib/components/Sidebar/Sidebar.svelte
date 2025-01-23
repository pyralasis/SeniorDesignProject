<script lang="ts">
    import type { Layer } from '$lib/types/layer';
    import { useDnD, type DnDContext } from '../../utilities/DnDUtils';
    import SidebarLayer from './SidebarNode.svelte';
    import { onMount } from 'svelte';
    import { BackendApi } from '$lib/utilities/api.utilities';
    import { NodeTypeEnum, type NodeType } from '$lib/types/node-type.enum';
    import TestNode from '../nodes/TestNode.svelte';

    const dndContext = useDnD();
    let layers: Layer<any>[] = [];

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

<div>
    <div class="nodes-container">
        {#each layers as layer}
            <SidebarLayer {layer} {onDragStart} />
        {/each}
    </div>
</div>

<style lang="scss">
    aside {
        width: 100%;
        background: #f4f4f4;
        font-size: 12px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }

    .label {
        margin: 1rem 0;
        font-size: 0.9rem;
    }

    .nodes-container {
        display: flex;
        align-items: center;
        justify-content: center;
    }
</style>
