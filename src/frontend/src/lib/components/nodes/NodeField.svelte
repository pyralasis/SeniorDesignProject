<script lang="ts">
    import { NodeFieldTypeEnum, type NodeFieldType } from './types/node-field.interface';
    import { Checkbox, TextInput, InputSeries } from 'kiwi-nl';

    export let type: NodeFieldType = NodeFieldTypeEnum.input;
    export let label: string = '';
    export let required: boolean = false;
    export let value: string = '';
    export let onChange: (value: string) => void = () => {};

    function updateValue(event: CustomEvent) {
        value = event.detail.value.toString();
        onChange(value);
    }
</script>

<div class="node-field">
    {#if type === NodeFieldTypeEnum.boolean}
        <Checkbox {label} on:change={updateValue} />
    {:else if type === NodeFieldTypeEnum.input}
        <TextInput {label} on:change={updateValue} />
    {:else if type === NodeFieldTypeEnum.series}
        <InputSeries {label} on:change={updateValue} />
    {/if}
</div>
