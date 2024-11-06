<script lang="ts">
    import { getContext } from 'svelte';
    import type { AccordionStore } from './types';

    // -----------------------
    // Internal Properties
    // -----------------------
    const accordionStore: AccordionStore = getContext('accordionStore');
    let body: HTMLElement;
    let bodyHeight: number;

    // -----------------------
    // Lifecycle Hooks
    // -----------------------
    $: if ($accordionStore?.isOpen && body) {
        bodyHeight = body.scrollHeight;
    } else {
        bodyHeight = 0;
    }

    $: if (body) {
        body.style.setProperty('--max-height', `${bodyHeight}px`);
    }
</script>

<div class="accordion-body" class:accordion-body--open={$accordionStore?.isOpen} bind:this={body}>
    <slot></slot>
</div>

<style lang="scss">
    .accordion-body {
        overflow: hidden;
        max-height: 0;
        transition:
            max-height 0.3s ease-in-out,
            padding 0.3s ease-in-out;
        padding: 0 var(--size-sm);

        &--open {
            max-height: var(--max-height);
            padding-top: var(--size-sm);
            padding-bottom: var(--size-sm);
        }
    }
</style>
