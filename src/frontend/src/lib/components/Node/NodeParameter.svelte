<script lang="ts">
    import { type Parameter, type ParameterType, ParameterTypeEnum, type ParameterValue } from '$lib/types/parameter';
    import { StylingUtility } from '$lib/utilities/styling.utility';
    import { Checkbox, TextInput, InputSeries } from 'kiwi-nl';

    export let parameter: Parameter<any>;
    export let value: ParameterValue<any>;
    export let onChange: (value: ParameterValue<any>) => void = () => {};

    function updateValue(event: CustomEvent, type: ParameterType) {
        console.log(event.detail);
        value.type = type;
        value.val = event.detail.value;
    }
    const initialValue = value.val;
</script>

<div class="node-field">
    {#if parameter.type === ParameterTypeEnum.Bool}
        <Checkbox
            style={StylingUtility.checkbox}
            label={parameter.name}
            bind:checked={value.val}
            on:change={(event) => updateValue(event, ParameterTypeEnum.Bool)}
        />
    {:else if parameter.type === ParameterTypeEnum.Int}
        <TextInput
            style={StylingUtility.textInput}
            label={parameter.name}
            bind:value={value.val}
            on:change={(event) => updateValue(event, ParameterTypeEnum.Int)}
        />
    {:else if parameter.type === ParameterTypeEnum.Float}
        <TextInput
            style={StylingUtility.textInput}
            label={parameter.name}
            on:change={(event) => updateValue(event, ParameterTypeEnum.Float)}
        />
    {:else if parameter.type === ParameterTypeEnum.String}
        <TextInput
            style={StylingUtility.textInput}
            label={parameter.name}
            bind:value={value.val}
            on:change={(event) => updateValue(event, ParameterTypeEnum.String)}
        />
    {:else if parameter.type === ParameterTypeEnum.Size2D}
        <InputSeries
            style={StylingUtility.inputSeries}
            label={parameter.name}
            maxlength={2}
            inputamount={2}
            value={value.val}
            on:change={(event) => updateValue(event, ParameterTypeEnum.Size2D)}
        />
    {/if}
</div>
