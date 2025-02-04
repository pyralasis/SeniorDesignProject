<script lang="ts">
    import { type Parameter, type ParameterType, ParameterTypeEnum, type ParameterValue } from '$lib/types/layer';
    import { Checkbox, TextInput, InputSeries } from 'kiwi-nl';

    export let parameter: Parameter<any>;
    export let value: ParameterValue<any>;
    export let onChange: (value: ParameterValue<any>) => void = () => {};

    function updateValue(event: CustomEvent, type: ParameterType) {
        value.type = type;
        onChange(value);
    }

    const inputStyle = {
        backgroundColor: '#000000',
        color: '#ffffff',
        border: '1px solid #ffffff',
        label: {
            color: '#ffffff',
        },
        hover: {
            backgroundColor: '#000000',
            color: '#ffffff',
            border: '1px solid #ffffff',
        },
        focus: {
            backgroundColor: '#000000',
            color: '#ffffff',
            border: '1px solid #ffffff',
        },
    };

    const checkboxStyle = {
        border: '2px solid #FFFFFF',
        borderRadius: '0px',
        hover: {
            backgroundColor: '#000000',
            border: '2px solid #CCCCCC',
        },
        checked: {
            backgroundColor: '#000000',
            border: '2px solid #FFFFFF',
            hover: {
                backgroundColor: '#111111',
                border: '2px solid #CCCCCC',
            },
        },
    };
</script>

<div class="node-field">
    {#if parameter.type === ParameterTypeEnum.Bool}
        <Checkbox
            style={checkboxStyle}
            label={parameter.name}
            bind:checked={value.value}
            on:change={(event) => updateValue(event, ParameterTypeEnum.Bool)}
        />
    {:else if parameter.type === ParameterTypeEnum.Int}
        <TextInput
            style={inputStyle}
            label={parameter.name}
            bind:value={value.value}
            on:change={(event) => updateValue(event, ParameterTypeEnum.Int)}
        />
    {:else if parameter.type === ParameterTypeEnum.Float}
        <TextInput style={inputStyle} label={parameter.name} on:change={(event) => updateValue(event, ParameterTypeEnum.Float)} />
    {:else if parameter.type === ParameterTypeEnum.String}
        <TextInput
            style={inputStyle}
            label={parameter.name}
            bind:value={value.value}
            on:change={(event) => updateValue(event, ParameterTypeEnum.String)}
        />
    {:else if parameter.type === ParameterTypeEnum.Size2D}
        <InputSeries label={parameter.name} on:change={(event) => updateValue(event, ParameterTypeEnum.Size2D)} />
    {/if}
</div>
