<script lang="ts">
    import { getContext } from 'svelte';
    import type { CustomAccordionStore } from './types';
    import { getParentStore } from '$lib/utilities';
    import { Text } from '$lib/components';

    // -----------------------
    // Internal Properties
    // -----------------------
    const accordionStore: CustomAccordionStore = getParentStore() as CustomAccordionStore;
    let rotateDegrees: number = 0;
    let open: boolean;
    accordionStore.subscribe((value) => {
        open = value.open ?? false;
        rotateDegrees = open ? 180 : 0;
    });

    // -----------------------
    // Internal Methods
    // -----------------------
    function handleClick(): void {
        accordionStore.toggle();
    }
</script>

<!-- svelte-ignore a11y-click-events-have-key-events -->
<!-- svelte-ignore a11y-no-static-element-interactions -->
<div class="accordion-header" class:accordion-header--open={open} on:click={handleClick}>
    <Text>
        <slot></slot>
    </Text>
    <div class="accordion-header__chevron">
        <svg
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
            style="transform: rotate({rotateDegrees}deg); transition: transform 0.3s ease;"
        >
            <polyline points="6 9 12 15 18 9"></polyline>
        </svg>
    </div>
</div>

<style lang="scss">
    @import '../../../variables.css';
    .accordion-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: var(--size-sm);
        cursor: pointer;
        transition: background-color 0.3s ease;
        width: auto;
        box-sizing: border-box;

        &:hover {
            background-color: var(--color-interactable-secondary-hover);
        }

        &__title {
            font-size: 16px;
            font-weight: 600;
        }

        &__chevron {
            height: 24px;
            width: 24px;
            transition: transform 0.3s ease;
            color: #787878;
        }
    }
</style>
