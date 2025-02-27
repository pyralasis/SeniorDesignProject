<script lang="ts">
    import { useDnD, type DnDContext, type NodeBlueprint } from '../../utilities/DnDUtils';
    import SidebarLayer from './SidebarNode.svelte';
    import { type NodeType } from '$lib/types/node-type.enum';

    const dndContext = useDnD();

    export let expanded: boolean = true;
    export let nodes: DnDContext[] = [];

    const onDragStart = (event: DragEvent, nodeType: NodeType, nodeBlueprint: NodeBlueprint) => {
        if (!event.dataTransfer) {
            return null;
        }
        if (dndContext) {
            dndContext.set({ type: nodeType, nodeBlueprint: nodeBlueprint });
        }
        event.dataTransfer.effectAllowed = 'move';
    };
</script>

<div class="sidebar" style="width: {expanded ? 'fit-content' : '0px'}; opacity: {expanded ? 1 : 0};">
    <!-- <p class="sidebar__subheader">Drag and drop to add a node</p> -->
    <div class="sidebar__nodes-container">
        {#each Object.entries(nodes.reduce((acc, node) => {
                    if (!acc[node.type]) acc[node.type] = [];
                    acc[node.type].push(node);
                    return acc;
                }, {} as Record<string, DnDContext[]>)) as [type, typeNodes]}
            <div class="sidebar__type-section">
                <h4 class="sidebar__type-header">{type.charAt(0).toUpperCase() + type.slice(1)}s</h4>
                {#each typeNodes as node}
                    <SidebarLayer {node} {onDragStart} />
                {/each}
            </div>
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
        border-right: 1px solid #ffffff;
        padding: 16px 8px 0 8px;
        background-color: #111111;

        &__nodes-container {
            position: relative;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding-top: 20px;
            overflow-y: auto;
            max-height: 100%;
        }

        // &__header {
        //     font-size: 24px;
        //     font-weight: 600;
        //     color: #ffffff;
        //     margin-bottom: 0;
        // }

        // &__subheader {
        //     font-size: 14px;
        //     font-weight: 600;
        //     color: #ffffff;
        // }

        &__type-header {
            color: #ffffff;
            font-size: 16px;
            margin: 0 8px;
            padding: 8px 0;
            border-bottom: 1px solid #ffffff;
        }
    }
</style>
