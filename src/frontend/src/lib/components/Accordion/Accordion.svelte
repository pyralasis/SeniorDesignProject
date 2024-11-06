<script lang="ts">
    import { setContext } from 'svelte';
    import { createAccordionStore } from './accordionStore';
    import type { AccordionStore } from './types';

    // -----------------------
    // Internal Properties
    // -----------------------
    const accordionStore: AccordionStore = createAccordionStore();

    // -----------------------
    // Lifecycle Hooks
    // -----------------------
    setContext('accordionStore', accordionStore);
</script>

<div class="accordion">
    <div class="accordion__header">
        <slot name="header"></slot>
    </div>
    <div class="accordion__body">
        <slot name="body"></slot>
    </div>
</div>

<style lang="scss">
    .accordion {
        overflow: hidden;
        border-radius: var(--size-sm);
        border: 1px solid var(--color-edge);
    }
</style>
