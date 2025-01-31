<script lang="ts">
    import { type Layer } from '$lib/types/layer';
    import { NodeTypeEnum, type NodeType } from '$lib/types/node-type.enum';

    export let layer: Layer<any> = {
        id: '',
        inputs: [],
        name: 'Node Name',
        parameters: [],
    };
    export let onDragStart: (event: DragEvent, nodeType: NodeType, layerBlueprint: Layer<any>) => void = () => {};
</script>

<!-- svelte-ignore a11y-no-static-element-interactions -->
<div on:dragstart={(e) => onDragStart(e, NodeTypeEnum.Layer, layer)} draggable={true} class="input-node node">{layer.name}</div>

<style lang="scss">
    .node {
        margin: 0.5rem;
        border: 1px solid #111;
        padding: 0.5rem 1rem;
        font-weight: 700;
        border-radius: 3px;
        cursor: grab;
        width: 5%;
        height: 10%;
        text-align: center;
        min-height: 40px;
        display: flex;
        justify-content: center;
        align-items: center;
    }
</style>
