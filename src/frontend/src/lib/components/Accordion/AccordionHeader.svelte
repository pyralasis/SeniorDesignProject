<script lang="ts">
    import { getContext } from 'svelte';
    import type { AccordionStore } from './types';

    // -----------------------
    // Internal Properties
    // -----------------------
    const accordionStore: AccordionStore = getContext('accordionStore');
    let rotateDegrees: number = 0;

    // -----------------------
    // Internal Methods
    // -----------------------
    function handleClick(): void {
        accordionStore.toggle();
    }
    // -----------------------
    // Lifecycle Hooks
    // -----------------------
    $: rotateDegrees = $accordionStore?.isOpen ? 180 : 0;
</script>

<!-- svelte-ignore a11y-click-events-have-key-events -->
<!-- svelte-ignore a11y-no-static-element-interactions -->
<div class="accordion-header" class:accordion-header--open={$accordionStore?.isOpen} on:click={handleClick}>
    <div class="accordion-header__title">
        <slot></slot>
    </div>
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

        &:hover {
            background-color: var(--color-surface-dark);
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

        &--open {
            box-shadow: 0px 2px 2px 0px rgba(0, 0, 0, 0.1);
        }
    }
</style>
