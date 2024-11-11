<script lang="ts">
    import { createEventDispatcher } from 'svelte';
    import { TextColorEnum, Text, TextSizeEnum } from '$lib/components';
    export let label;
    export let checked = false;

    let checkbox: HTMLElement;

    const dispatch = createEventDispatcher();
    function handleClick(event: MouseEvent) {
        event.stopPropagation();
        checked = !checked;
        dispatch('change', { value: checked });
        checkbox.focus();
    }

    $: checked;
</script>

<div class="checkbox">
    <!-- svelte-ignore a11y-click-events-have-key-events -->
    <!-- svelte-ignore a11y-no-static-element-interactions -->
    <div class="checkbox__inner" class:checkbox__inner--checked={checked} bind:this={checkbox} on:click={handleClick}>
        {#if checked}
            <svg width="8" height="7" viewBox="0 0 8 7" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path
                    d="M2.46971 5.65706L0.812892 3.72545C0.626679 3.50835 0.325873 3.50835 0.13966 3.72545C-0.0465533 3.94254 -0.0465533 4.29324 0.13966 4.51034L2.13548 6.83718C2.3217 7.05427 2.6225 7.05427 2.80871 6.83718L7.86034 0.947714C8.04655 0.730616 8.04655 0.37992 7.86034 0.162823C7.67413 -0.0542743 7.37332 -0.0542743 7.18711 0.162823L2.46971 5.65706Z"
                    fill="white"
                />
            </svg>
        {/if}
    </div>
    {#if label}
        <Text color={TextColorEnum.primary} size={TextSizeEnum.medium}>
            {label}
        </Text>
    {/if}
</div>

<style lang="scss">
    @import '../../../variables.css';
    .checkbox {
        display: flex;
        align-items: center;
        gap: 8px;
        width: fit-content;
        z-index: 2;

        &__inner {
            width: 13px;
            height: 13px;
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
            border: 2px solid var(--color-edge);
            border-radius: 4px;
            cursor: pointer;
            transition: all 0.3s ease;

            &:hover {
                border: 2px solid var(--color-interactable-outline-hover);
            }

            &--checked {
                background-color: var(--color-interactable-primary);
                border: 2px solid var(--color-interactable-outline-hover);

                &:hover {
                    background-color: var(--color-interactable-primary-hover);
                    border: 2px solid var(--color-interactable-primary-hover);
                }
            }

            &:focus {
                border: solid 2px var(--color-priamry);
            }

            &:focus-visible {
                border: solid 2px var(--color-priamry);
            }
        }

        &__label {
            font-weight: 500;
            color: var(--color-text);
            user-select: none;
        }

        &__check-mark {
            width: 5px;
            height: 5px;
            background-color: white;
            border-radius: 50%;
        }
    }
</style>
