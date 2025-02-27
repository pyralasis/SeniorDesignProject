<script lang="ts">
    import { NodeTypeEnum, type NodeType } from '$lib/types/node-type.enum';
    import { getContext } from 'svelte';
    import { writable, type Writable } from 'svelte/store';
    import Icon from '../Icon/Icon.svelte';
    import { IconNameEnum } from '../Icon/types/icon-name.enum';
    import { SoundUtility } from '$lib/utilities/sound.utility';
    import type { DnDContext, NodeBlueprint } from '$lib/utilities/DnDUtils';

    export let node: DnDContext;
    export let onDragStart: (event: DragEvent, nodeType: NodeType, nodeBlueprint: NodeBlueprint) => void = () => {};

    let xColor: Writable<string> = getContext('xColor');
    let hovered: Writable<boolean> = writable(false);
    let showParameterCount: boolean = node.type === NodeTypeEnum.Layer;

    function handleMouseEnter() {
        hovered.update((value) => (value = true));
    }

    function handleMouseLeave() {
        hovered.update((value) => (value = false));
    }

    function handleClick() {
        SoundUtility.playGrab(0.2);
    }
</script>

<!-- svelte-ignore a11y_no_static_element_interactions -->
<!-- svelte-ignore a11y_click_events_have_key_events -->
<div
    on:dragstart={(e) => onDragStart(e, node.type, node.nodeBlueprint)}
    on:mouseenter={handleMouseEnter}
    on:mouseleave={handleMouseLeave}
    on:mousedown={handleClick}
    draggable={true}
    class="input-node node"
    style="
        border-color: {$hovered ? $xColor + '88' : '#eaeaea'};
    "
>
    <div class="node__title">
        <Icon name={IconNameEnum.plus} />
        {node.nodeBlueprint.name}
    </div>
    {#if showParameterCount}
        <div class="node__params">
            {node.nodeBlueprint.parameters.length} parameters
        </div>
    {/if}
</div>

<style lang="scss">
    .node {
        margin: 0.5rem;
        padding: 12px 16px;
        font-weight: 600;
        cursor: grab;
        width: 170px;
        min-height: 40px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        transition: all 0.2s ease;
        background-color: #111111;
        border: 1px solid #ffffff;

        &__title {
            font-size: 14px;
            color: #ffffff;
            display: flex;
            align-items: center;
            justify-content: flex-start;
            gap: 8px;
        }

        &__params {
            font-size: 12px;
            color: #ffffff;
            font-weight: 600;
            margin-left: 26px;
        }

        &:hover {
            z-index: 10;
            transform: translateY(-2px);
        }

        &:active {
            cursor: grabbing;
            transform: translateY(0);
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        }
    }
</style>
