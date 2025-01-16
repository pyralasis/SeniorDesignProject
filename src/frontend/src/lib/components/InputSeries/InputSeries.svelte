<script lang="ts">
    import { createEventDispatcher } from 'svelte';
    import { InputSeriesTypeEnum, type InputSeriesType } from './types';
    import { Text, TextInput } from '$lib/components';
    // -----------------------
    // External Properties
    // -----------------------
    export let inputamount: number = 5;
    export let maxlength: number = 1;
    export let type: InputSeriesType = InputSeriesTypeEnum.alphanumeric;
    export let label: string;

    // -----------------------
    // Internal Properties
    // -----------------------
    let inputElements: HTMLInputElement[] = [];
    const dispatch = createEventDispatcher();

    // -----------------------
    // Internal Methods
    // -----------------------
    function handleKeyNavigation(event: KeyboardEvent, index: number): void {
        if (event.key === 'Enter') {
            if (index != inputElements.length - 1) {
                inputElements[index + 1].focus();
            } else {
                inputElements[index].blur();
            }
        }
    }

    function handleInput(event: Event, index: number): void {
        let targetValue = (event.target as HTMLInputElement).value;
        dispatch('change', { value: targetValue });

        if (type === InputSeriesTypeEnum.digit) {
            if (!/^\d+$/.test(targetValue)) {
                (event.target as HTMLInputElement).value = targetValue.slice(0, -1);
                return;
            }
        } else if (type === InputSeriesTypeEnum.character) {
            if (!/^[a-zA-Z]+$/.test(targetValue)) {
                (event.target as HTMLInputElement).value = targetValue.slice(0, -1);
                return;
            }
        } else if (type === InputSeriesTypeEnum.alphanumeric) {
            if (!/^[a-zA-Z0-9]+$/.test(targetValue)) {
                (event.target as HTMLInputElement).value = targetValue.slice(0, -1);
                return;
            }
        }

        if (targetValue.length > maxlength) {
            (event.target as HTMLInputElement).value = (event as InputEvent).data ?? '';
        }
        if (targetValue.length >= maxlength) {
            if (index != inputElements.length - 1) {
                inputElements[index + 1].focus();
            } else {
                inputElements[index].blur();
            }
        }
    }
</script>

<div class="input-series">
    <div class="input-series__header">
        <Text>{label}</Text>
    </div>
    <div class="input-series__container">
        {#each Array(inputamount) as _, index}
            <div class="input-series__entryarea">
                <input
                    class="input-series__input"
                    type="text"
                    bind:this={inputElements[index]}
                    on:keydown={(event) => handleKeyNavigation(event, index)}
                    on:input={(event) => handleInput(event, index)}
                    on:change={() => dispatch('change', { value: inputElements.map((input) => input.value) })}
                />
            </div>
        {/each}
    </div>
</div>

<style lang="scss">
    @import '../../../variables.css';

    .input-series {
        display: flex;
        flex-direction: column;
        gap: var(--size-xs);
        align-items: flex-start;

        &__container {
            display: flex;
            gap: var(--size-xs);
        }

        &__entryarea {
            height: 35px;
            line-height: 35px;
        }

        &__input {
            width: 35px;
            box-sizing: border-box;
            font-size: 16px;
            color: var(--color-text-primary);
            height: 35px;
            border-radius: var(--size-xs);
            outline: 1px solid var(--color-edge-dark);
            background: transparent;
            transition: 0.1s ease-in-out;
            z-index: 1111;
            border: none;
            text-align: center;

            &:hover {
                outline: 2px solid var(--color-edge-dark);
            }

            &:focus {
                outline: 2px solid var(--color-primary);
            }
        }
    }
</style>
