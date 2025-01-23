<script lang="ts">
    import { type Writable, writable } from 'svelte/store';
    import { Handle, Position, type NodeProps } from '@xyflow/svelte';
    import NodeField from './NodeParameter.svelte';
    import { getContext } from 'svelte';
    import type { Parameter, ParameterValue } from '$lib/types/layer';

    type $$Props = NodeProps;

    export let data: $$Props['data'];
    export let id: $$Props['id'];

    const color: Writable<string> = data?.color as Writable<string>;
    const title: Writable<string> = data?.title as Writable<string>;
    const parameters: Writable<{ parameter: Parameter<any>; value: ParameterValue<any> }[]> = data?.parameters as Writable<
        { parameter: Parameter<any>; value: ParameterValue<any> }[]
    >;
    const selectedNodeId: Writable<string> = getContext('selectedNodeId');

    let selected = false;
    const expanded = writable(true);
    const rotationDegrees = writable(0);

    function handleToggleExpanded() {
        expanded.update((value) => !value);
        rotationDegrees.update((value) => (value === 0 ? 180 : 0));
    }

    function setSelected() {
        selectedNodeId.set(id);
    }

    function updateValue(value: ParameterValue<any>) {
        console.log(value);
    }

    $: selected = $selectedNodeId === id;
</script>

<Handle type="target" position={Position.Left} />
<!-- svelte-ignore a11y_click_events_have_key_events -->
<!-- svelte-ignore a11y_no_static_element_interactions -->
<div class="node" style="outline: 1px solid {selected ? $color : 'transparent'}" on:click={setSelected}>
    <!-- svelte-ignore a11y_click_events_have_key_events -->
    <!-- svelte-ignore a11y_no_static_element_interactions -->
    <div class="node__header" style="background-color: {$color};" on:click={handleToggleExpanded}>
        <div class="node__title">{$title} {id}</div>
        <div style="transform: rotate({$rotationDegrees}deg); transition: transform 0.3s;">&#9660;</div>
    </div>
    {#if $expanded}
        <div class="node__content">
            {#each $parameters as parameter, index}
                <NodeField parameter={parameter.parameter} value={parameter.value} onChange={updateValue} />
            {/each}
        </div>
    {/if}
</div>
<Handle type="source" position={Position.Right} />

<style lang="scss">
    .node {
        display: flex;
        flex-direction: column;
        justify-content: space-between;

        border-radius: 4px;
        overflow: hidden;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        width: 500px;
        background-color: #ffffff;
        transition: height 0.2s;

        &__header {
            padding: 8px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            cursor: pointer;
            font-weight: bold;
        }

        &__content {
            padding: 16px;
            display: flex;
            flex-direction: column;
            gap: 16px;
        }
    }
</style>
