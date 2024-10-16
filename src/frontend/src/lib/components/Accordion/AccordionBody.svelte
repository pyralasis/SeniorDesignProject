<script lang="ts">
    import { getContext } from 'svelte';

    const accordionStore = getContext('accordionStore');
    let body: HTMLElement;
    let bodyHeight: number;

    $: if ($accordionStore?.isOpen && body) {
        bodyHeight = body.scrollHeight + 'px';
    } else {
        bodyHeight = '0px';
    }

    $: if (body) {
        body.style.setProperty('--max-height', bodyHeight);
    }
</script>

<div class="accordion-body" class:accordion-body-open={$accordionStore?.isOpen} bind:this={body}>
    <slot></slot>
</div>

<style>
    .accordion-body {
        overflow: hidden;
        max-height: 0;
        transition:
            max-height 0.3s ease-in-out,
            padding 0.3s ease-in-out;
        padding: 0 var(--size-sm);
    }

    .accordion-body-open {
        max-height: var(--max-height);
        padding-top: var(--size-sm);
        padding-bottom: var(--size-sm);
    }
</style>
