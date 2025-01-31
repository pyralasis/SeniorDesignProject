<script lang="ts">
    import { type Parameter, type ParameterType, ParameterTypeEnum, type ParameterValue } from '$lib/types/layer';
    import { Checkbox, TextInput, InputSeries } from 'kiwi-nl';

    export let parameter: Parameter<any>;
    export let value: ParameterValue<any>;
    export let onChange: (value: ParameterValue<any>) => void = () => {};

    function updateValue(event: CustomEvent, type: ParameterType) {
        value.value = event.detail.value.toString();
        value.type = type;
        onChange(value);
    }
</script>

<div class="node-field">
    {#if parameter.type === ParameterTypeEnum.Bool}
        <Checkbox label={parameter.name} on:change={(event) => updateValue(event, ParameterTypeEnum.Bool)} />
    {:else if parameter.type === ParameterTypeEnum.Int}
        <TextInput label={parameter.name} on:change={(event) => updateValue(event, ParameterTypeEnum.Int)} />
    {:else if parameter.type === ParameterTypeEnum.Float}
        <TextInput label={parameter.name} on:change={(event) => updateValue(event, ParameterTypeEnum.Float)} />
    {:else if parameter.type === ParameterTypeEnum.String}
        <TextInput label={parameter.name} on:change={(event) => updateValue(event, ParameterTypeEnum.String)} />
    {:else if parameter.type === ParameterTypeEnum.Size2D}
        <InputSeries label={parameter.name} on:change={(event) => updateValue(event, ParameterTypeEnum.Size2D)} />
    {/if}
</div>
