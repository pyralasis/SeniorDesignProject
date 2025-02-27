<script lang="ts">
    import { type Writable, writable } from 'svelte/store';
    import { Handle, Position, type NodeProps } from '@xyflow/svelte';
    import NodeField from './NodeParameter.svelte';
    import type { Parameter, ParameterValue } from '$lib/types/parameter';
    import Icon from '$lib/components/Icon/Icon.svelte';
    import { IconNameEnum } from '../Icon/types/icon-name.enum';
    import type { TransformType } from '$lib/types/transform';

    type $$Props = NodeProps;

    export let data: $$Props['data'] = {};
    export let id: $$Props['id'] = '';
    export let selected: $$Props['selected'] = false;

    const color: Writable<string> = data?.color as Writable<string>;
    const name: Writable<string> = data?.name as Writable<string>;
</script>

<Handle
    type="target"
    position={Position.Left}
    style="
        border-color: {$color + (selected ? 'bb' : '34')};
        border-radius: 0;
        height: 8px;
        width: 6px;
    "
/>
<Handle
    type="source"
    position={Position.Right}
    style="
        border-color: {$color + (selected ? 'bb' : '34')};
        border-radius: 4px;
        height: 8px;
        width: 6px;
    "
/>
<!-- svelte-ignore a11y_click_events_have_key_events -->
<!-- svelte-ignore a11y_no_static_element_interactions -->
<div
    class="transform-node node__header"
    style="
        outline: {selected ? '1.5' : '1'}px solid {$color + (selected ? 'bb' : '34')};
        cursor: pointer;
        transition: outline 0.2s;
    "
>
    <!-- svelte-ignore a11y_click_events_have_key_events -->
    <!-- svelte-ignore a11y_no_static_element_interactions -->
    <div class="transform-node__header">
        <div class="transform-node__title">Transform</div>
        <div class="transform-node__sub-title">{$name}</div>
    </div>
</div>

<style lang="scss">
    .transform-node {
        display: flex;
        flex-direction: column;
        overflow: hidden;
        box-shadow: 0 3px 7px #78787843;
        width: 250px;
        transition: height 0.2s;

        &__header {
            display: flex;
            flex-direction: column;
            gap: 4px;
            align-items: center;
            justify-content: center;
            cursor: grab;
            color: #ffffff;
            background: #070707;
            height: 45px;

            &:active {
                cursor: grabbing;
            }
        }

        &__title {
            font-size: 12px;
            font-weight: 600;
        }
    }
</style>
