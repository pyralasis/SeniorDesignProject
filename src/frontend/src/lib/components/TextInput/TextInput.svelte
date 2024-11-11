<script lang="ts">
    import { createEventDispatcher, type EventDispatcher } from 'svelte';

    // -----------------------
    // External Properties
    // -----------------------
    export let label: string = '';
    export let placeholder: string = '';
    export let value: string = '';

    // -----------------------
    // Internal Events
    // -----------------------
    const dispatch: EventDispatcher<any> = createEventDispatcher();

    // -----------------------
    // Internal Methods
    // -----------------------
    function handleChange(event: Event): void {
        let targetValue = (event.target as HTMLInputElement).value;
        dispatch('change', { value: targetValue });
    }
</script>

<div class="text-input__container">
    <div class="text-input__entryarea">
        <input class="text-input__input" type="text" required {placeholder} bind:value on:change={handleChange} />
        <div class="text-input__labelline">
            {label}
        </div>
    </div>
</div>

<style lang="scss">
    @import '../../../variables.css';

    .text-input {
        &__container {
            width: auto;
            box-sizing: border-box;
        }

        &__entryarea {
            position: relative;
            height: 35px;
            line-height: 35px;
        }

        &__input {
            position: absolute;
            width: 100%;
            box-sizing: border-box;
            font-size: 16px;
            color: var(--color-text-primary);
            padding: 0 30px;
            height: 35px;
            border-radius: var(--size-xs);
            outline: 1px solid var(--color-edge-dark);
            background: transparent;
            transition: 0.1s ease-in-out;
            z-index: 500;
            border: none;

            &:hover {
                outline: 2px solid var(--color-edge-dark);
            }

            &:focus + .text-input__labelline,
            &:valid + .text-input__labelline {
                height: 25px;
                line-height: 25px;
                transform: translate(0, -14px) scale(0.9);
                padding: 0 8px;
                z-index: 500;
            }

            &:focus + .text-input__labelline {
                color: var(--color-primary-dark);
            }

            &:focus {
                outline: 2px solid var(--color-primary);
            }
        }

        &__labelline {
            position: absolute;
            font-size: 14px;
            color: var(--color-text-light);
            padding: 0 8px;
            background-color: var(--color-surface);
            transition: 0.1s ease-in-out;
            width: fit-content;
            margin-left: 20px;
        }
    }
</style>
