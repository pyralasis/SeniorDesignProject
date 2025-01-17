<script lang="ts">
    import { type Writable, writable } from 'svelte/store';
    import { Handle, Position, type NodeProps } from '@xyflow/svelte';
    import { Accordion, AccordionBody, AccordionHeader, Text, TextInput } from 'kiwi-nl';
    import { type NodeField } from './types/node-field.interface';
    import { getContext } from 'svelte';

    type $$Props = NodeProps;

    export let data: $$Props['data'];
    export let id: $$Props['id'];

    const color: Writable<string> = data?.color as Writable<string>;
    const title: Writable<string> = data?.title as Writable<string>;
    const fields: Writable<NodeField[]> = data?.fields as Writable<NodeField[]>;
    const selectedNodeId: Writable<string> = getContext('selectedNodeId');

    let selected = false;
    const expanded = writable(true);
    const collapsedHeight = 40;

    function handleToggleExpanded() {
        expanded.update((value) => !value);
    }

    function setSelected() {
        selectedNodeId.set(id);
    }

    $: selected = $selectedNodeId === id;
</script>

<Handle type="target" position={Position.Left} />
<div class="node" class:node--selected={selected} style="height: {$expanded ? 'auto' : collapsedHeight + 'px'}" on:click={setSelected}>
    <!-- svelte-ignore a11y_click_events_have_key_events -->
    <!-- svelte-ignore a11y_no_static_element_interactions -->
    <div class="node__header" style="background-color: {$color};" on:click={handleToggleExpanded}>
        <div class="node__title">{$title} {id}</div>
    </div>
    <div class="node__content">
        <Text>Im a little boy</Text>
    </div>
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
        width: 200px;
        background-color: #282828;

        &--selected {
            outline: 1px solid #ff7e54;
        }
    }
</style>
