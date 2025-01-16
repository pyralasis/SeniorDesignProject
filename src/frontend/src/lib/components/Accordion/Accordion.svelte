<script lang="ts">
    import { setContext } from 'svelte';
    import { createAccordionStore } from './accordionStore';
    import { setParentStoreContext } from '$lib/utilities';
    import type { CustomAccordionStore } from './types';

    // -----------------------
    // Internal Properties
    // -----------------------
    const private_store: CustomAccordionStore = createAccordionStore() as CustomAccordionStore;
    setParentStoreContext(private_store);
    let hovered: boolean = false;

    // -----------------------
    // Internal Methods
    // -----------------------
    function handleMouseEnter(): void {
        hovered = true;
    }

    function handleMouseLeave(): void {
        hovered = false;
    }
</script>

<div class="accordion" class:accordion--hovered={hovered}>
    <!-- svelte-ignore a11y-no-static-element-interactions -->
    <div class="accordion__header" on:mouseenter={handleMouseEnter} on:mouseleave={handleMouseLeave}>
        <slot name="header"></slot>
    </div>
    <div class="accordion__body">
        <slot name="body"></slot>
    </div>
</div>

<style lang="scss">
    @import '../../../variables.css';
    .accordion {
        overflow: hidden;
        border-radius: var(--size-sm);
        outline: 1px solid var(--color-edge);
        transition: outline 0.2s ease;
        width: auto;
        box-sizing: border-box;

        &--hovered {
            outline: 1px solid var(--color-interactable-outline-hover);
        }
    }
</style>
