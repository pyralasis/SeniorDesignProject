<script lang="ts">
    import { type Layer } from '$lib/types/layer';
    import { NodeTypeEnum, type NodeType } from '$lib/types/node-type.enum';
    import { getContext } from 'svelte';
    import { writable, type Writable } from 'svelte/store';
    import Icon from '../Icon/Icon.svelte';
    import { IconNameEnum } from '../Icon/types/icon-name.enum';

    export let layer: Layer<any> = {
        id: '',
        inputs: [],
        name: 'Node Name',
        parameters: [],
    };
    export let onDragStart: (event: DragEvent, nodeType: NodeType, layerBlueprint: Layer<any>) => void = () => {};

    let xColor: Writable<string> = getContext('xColor');
    let hovered: Writable<boolean> = writable(false);

    function handleMouseEnter() {
        hovered.update((value) => (value = true));
    }

    function handleMouseLeave() {
        hovered.update((value) => (value = false));
    }
</script>

<!-- svelte-ignore a11y_no_static_element_interactions -->
<div
    on:dragstart={(e) => onDragStart(e, NodeTypeEnum.Layer, layer)}
    on:mouseenter={handleMouseEnter}
    on:mouseleave={handleMouseLeave}
    draggable={true}
    class="input-node node"
    style="
        border-color: {$hovered ? $xColor + '88' : '#eaeaea'};
    "
>
    <div class="node__title">
        <Icon name={IconNameEnum.plus} />
        {layer.name}
    </div>
    <div class="node__params">
        {layer.parameters.length} parameters
    </div>
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
        background-color: #000000;
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
