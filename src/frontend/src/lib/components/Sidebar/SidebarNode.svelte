<script lang="ts">
    import { type Layer } from '$lib/types/layer';
    import { NodeTypeEnum, type NodeType } from '$lib/types/node-type.enum';
    import { getContext } from 'svelte';
    import { writable, type Writable } from 'svelte/store';

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
        {layer.name}
    </div>
    <div class="node__params">
        {layer.parameters.length} parameters
    </div>
</div>

<style lang="scss">
    .node {
        border-radius: 8px;
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
        background-color: #ffffff;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        border: 1px solid;

        &__title {
            font-size: 14px;
            color: #727272;
        }

        &__params {
            font-size: 12px;
            color: #a8a8a8;
            font-weight: 600;
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
