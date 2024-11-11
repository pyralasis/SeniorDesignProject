<script lang="ts">
    import { getContext } from 'svelte';
    import type { CustomAccordionStore } from './types';
    import { getParentStore } from '$lib/utilities';

    // -----------------------
    // Internal Properties
    // -----------------------
    const accordionStore: CustomAccordionStore = getParentStore() as CustomAccordionStore;
    let body: HTMLElement;
    let bodyHeight: number;
    let open: boolean;

    accordionStore.subscribe((value) => {
        open = value.open ?? false;
    });

    // -----------------------
    // Lifecycle Hooks
    // -----------------------
    $: if ($accordionStore?.open && body) {
        bodyHeight = body.scrollHeight;
    } else {
        bodyHeight = 0;
    }

    $: if (body) {
        body.style.setProperty('--max-height', `${bodyHeight}px`);
    }
</script>

<div class="accordion-body" class:accordion-body--open={open} bind:this={body}>
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
        width: auto;
        box-sizing: border-box;

        &--open {
            max-height: var(--max-height);
            padding-top: var(--size-sm);
            padding-bottom: var(--size-sm);
        }
    }
</style>
