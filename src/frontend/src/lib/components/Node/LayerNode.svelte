<script lang="ts">
    import { type Writable, writable } from 'svelte/store';
    import { Handle, Position, type Edge, type NodeProps } from '@xyflow/svelte';
    import NodeField from './NodeParameter.svelte';
    import type { Parameter, ParameterValue } from '$lib/types/parameter';
    import Icon from '$lib/components/Icon/Icon.svelte';
    import { IconNameEnum } from '../Icon/types/icon-name.enum';

    type $$Props = NodeProps;

    export let data: $$Props['data'] = {};
    export let id: $$Props['id'] = '';
    export let selected: $$Props['selected'] = false;

    const color: Writable<string> = data?.color as Writable<string>;
    const title: Writable<string> = data?.title as Writable<string>;
    const layerType: Writable<string> = data?.layer_id as Writable<string>;
    const parameters: Writable<{ parameter: Parameter<any>; value: ParameterValue<any> }[]> = data?.parameters as Writable<
        { parameter: Parameter<any>; value: ParameterValue<any> }[]
    >;
    const expanded: Writable<boolean> = data?.expanded as Writable<boolean>;
    const leftConnected: Writable<boolean> = data?.leftConnected as Writable<boolean>;
    const rightConnected: Writable<boolean> = data?.rightConnected as Writable<boolean>;
    const rotationDegrees = writable(0);

    function handleToggleExpanded() {
        expanded.update((value) => !value);
        rotationDegrees.update((value) => (value === 0 ? 90 : 0));
    }

    function toggleConnection(side: 'left' | 'right', connected: boolean) {
        console.log(side, connected);
        if (side === 'left') {
            $leftConnected = connected;
        } else {
            $rightConnected = connected;
        }
    }

    function isValidConnection(connection: any) {
        console.log(connection);
        return true;
    }
</script>

<Handle
    type="target"
    position={Position.Left}
    style="
        background-color: {$leftConnected ? '#FFF' : '#000'};
        border-color: {$color + (selected ? 'bb' : '34')};
        border-radius: 0;
        height: 8px;
        width: 6px;
    "
    onconnect={() => toggleConnection('left', true)}
    ondisconnect={() => toggleConnection('left', false)}
/>
<Handle
    type="source"
    position={Position.Right}
    style="
    background-color: {$rightConnected ? '#FFF' : '#000'};
        border-color: {$color + (selected ? 'bb' : '34')};
        border-radius: 4px;
        height: 8px;
        width: 6px;
    "
    onconnect={() => toggleConnection('right', true)}
    ondisconnect={() => toggleConnection('right', false)}
/>
<!-- svelte-ignore a11y_click_events_have_key_events -->
<!-- svelte-ignore a11y_no_static_element_interactions -->
<div
    class="node"
    style="
        outline: {selected ? '1.5' : '1'}px solid {$color + (selected ? 'bb' : '34')};
        cursor: pointer;
        transition: outline 0.2s;
    "
>
    <!-- svelte-ignore a11y_click_events_have_key_events -->
    <!-- svelte-ignore a11y_no_static_element_interactions -->
    <div class="node__header" on:click={handleToggleExpanded}>
        <div class="node__header-chevron" style="transform: rotate({$rotationDegrees}deg); transition: transform 0.2s;">
            <Icon name={IconNameEnum.chevron_right} />
        </div>
        <div style="display: flex; flex-direction: row; gap: 10px;">
            <div class="node__title">{$title ? $title : 'Untitled Layer'} - {$layerType}</div>
        </div>
    </div>
    {#if $expanded}
        <div class="node__content" style="visibility: {$expanded ? 'visible' : 'hidden'}; transition: visibility 0.2s;">
            {#each $parameters as parameter}
                <NodeField parameter={parameter.parameter} value={parameter.value} />
            {/each}
            {#if $parameters.length === 0}
                <div class="node__content-empty">No parameters for this layer type</div>
            {/if}
        </div>
    {/if}
</div>

<style lang="scss">
    .node {
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        overflow: hidden;
        box-shadow: 0 3px 7px #78787843;
        width: 250px;
        background-color: #ffffff;
        transition: height 0.2s;

        &__header {
            padding: 4px;
            display: flex;
            align-items: center;
            cursor: pointer;
            color: #ffffff;
            background: #070707;
        }

        &__header-chevron {
            display: flex;
            justify-content: center;
            align-items: center;
        }

        &__header-actions {
            display: flex;
            flex-direction: row;
            gap: 10px;
            margin-left: auto;
            margin-right: 10px;
        }

        &__content {
            padding: 16px;
            display: flex;
            flex-direction: column;
            gap: 16px;
            cursor: default;
            border-top: 1px solid #ffffff;
            background-color: #070707;
        }

        &__title {
            font-size: 12px;
            font-weight: 600;
        }

        &__content-empty {
            font-size: 12px;
            color: #9f9f9f;
            width: 100%;
            text-align: center;
        }
    }

    .target-handle {
        border-radius: 0;
        height: 10px;
        width: 4px;
    }
</style>
