<script lang="ts">
    import { useDnD, type DnDContext, type NodeBlueprint } from '../../utilities/DnDUtils';
    import SidebarLayer from './SidebarNode.svelte';
    import { type NodeType } from '$lib/types/node-type.enum';
    import { writable } from 'svelte/store';
    const dndContext = useDnD();

    export let expanded: boolean = true;
    export let nodes: DnDContext[] = [];

    const activeTool = writable<string>('drag');

    const switchTool = (tool: string) => {
        activeTool.set(tool);
    };

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
    <div class="sidebar__nodes-container">
        {#each Object.entries(nodes.reduce((acc, node) => {
                    if (!acc[node.type]) acc[node.type] = [];
                    acc[node.type].push(node);
                    return acc;
                }, {} as Record<string, DnDContext[]>)) as [type, typeNodes]}
            <div class="sidebar__section">
                <h4 class="sidebar__section-header">{type.charAt(0).toUpperCase() + type.slice(1)}s</h4>
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
        box-sizing: border-box;
        border-right: 1px solid #ffffff;
        padding: 16px 8px 0 8px;
        background-color: #111111;
        position: relative;
        &__nodes-container {
            position: relative;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding-top: 10px;
            overflow-y: scroll;
            scrollbar-width: thin;
            scrollbar-color: #ffffff transparent;
            max-height: 100%;
            box-sizing: border-box;
        }

        &__section {
            width: 220px;
            padding: 10px;
            border-radius: 6px;
            margin-bottom: 12px;
            display: flex;
            flex-direction: column;
        }

        &__section-header {
            font-size: 14px;
            font-weight: bold;
            color: white;
            margin-bottom: 8px;
            border-bottom: 1px solid white;
            padding-bottom: 5px;
        }

        &__button-group {
            display: flex;
            flex-direction: row;
            gap: 8px;
        }

        &__button {
            background-color: transparent;
            border: 1px solid white;
            padding: 6px;
            cursor: pointer;
            transition: background 0.3s ease;
            color: white;
            gap: 8px;
            width: 50px;
            font-size: 3px;
        }

        &__button:hover {
            background-color: #444;
        }

        &__button.active {
            border: 2px solid #00b0ff;
        }

        .sidebar__button span {
            opacity: 0;
            visibility: hidden;
            transition:
                opacity 0.3s ease,
                visibility 0.3s ease;
        }

        .sidebar__button:hover span {
            opacity: 1;
            visibility: visible;
        }
    }
</style>
